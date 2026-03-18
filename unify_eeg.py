import mne
import os
import numpy as np
import glob

def unify_common_channels_only(input_dir, output_dir, file_pattern="*.set"):
    os.makedirs(output_dir, exist_ok=True)

    # Get all files
    input_files = glob.glob(os.path.join(input_dir, file_pattern))
    if not input_files:
        raise ValueError(f"No files matching {file_pattern} found in folder {input_dir}")

    print(f"Found {len(input_files)} files for unification")

    # 1. Analyze channels of all files
    all_channels = []
    raw_list = []

    for f in input_files:
        try:
            raw = mne.io.read_raw_eeglab(f, preload=True, verbose='error')
            raw_list.append(raw)
            all_channels.append(set(raw.ch_names))
            print(f" {os.path.basename(f)}: {len(raw.ch_names)} channels")
        except Exception as e:
            print(f" Failed to load: {os.path.basename(f)}")
            continue

    if len(raw_list) < 2:
        raise ValueError("At least 2 valid files are required")

    # 2. Calculate common channels
    common_channels = set.intersection(*all_channels)

    print(f"\nCommon Channel Analysis:")
    print(f"Number of files: {len(raw_list)}")
    print(f"Number of common channels: {len(common_channels)}")
    print(f"Common channel list: {sorted(common_channels)}")

    # 3. Calculate channel retention rate for each file
    print(f"\nChannel Retention Rate Analysis:")
    retention_rates = []
    for i, (raw, filename) in enumerate(zip(raw_list, input_files)):
        original_count = len(raw.ch_names)
        retained_count = len(set(raw.ch_names) & common_channels)
        retention_rate = retained_count / original_count * 100

        retention_rates.append(retention_rate)
        print(f"{os.path.basename(filename)}: {original_count} → {retained_count} channels ({retention_rate:.1f}%)")

    avg_retention = np.mean(retention_rates)
    print(f"\nAverage channel retention rate: {avg_retention:.1f}%")

    # 4. Confirm whether to continue
    if len(common_channels) == 0:
        print(" Error: No common channels, cannot perform unification")
        return

    if avg_retention < 50:
        print(" Warning: Low channel retention rate, may lose important data")
        response = input("Continue? (y/n): ")
        if response.lower() != 'y':
            print("Operation cancelled")
            return

    # 5. Execute unification processing
    print(f"\nStarting unification processing...")
    success_count = 0

    for i, (raw, input_file) in enumerate(zip(raw_list, input_files)):
        try:
            # Create data copy
            raw_unified = raw.copy()

            # Retain only common channels
            available_common = list(set(raw_unified.ch_names) & common_channels)
            if available_common:
                raw_unified.pick_channels(available_common)

                # Save file
                output_filename = f"unified_{os.path.basename(input_file)}"
                output_path = os.path.join(output_dir, output_filename)

                mne.export.export_raw(output_path, raw_unified, fmt='eeglab', overwrite=True)

                success_count += 1
                print(f" {os.path.basename(input_file)} → {output_filename} ({len(available_common)} channels)")
            else:
                print(f" {os.path.basename(input_file)}: No common channels available")

        except Exception as e:
            print(f" {os.path.basename(input_file)} processing failed: {str(e)}")

    # 6. Generate processing report
    generate_simple_report(input_files, common_channels, retention_rates, output_dir)

    print(f"\nProcessing complete: {success_count}/{len(raw_list)} files successfully unified")
    print(f"Output directory: {output_dir}")

def generate_simple_report(input_files, common_channels, retention_rates, output_dir):
    """Generate simple processing report"""

    report_content = f"""
EEG Data Unification Processing Report
======================================

Number of input files: {len(input_files)}
Number of common channels: {len(common_channels)}

Common channel list:
{', '.join(sorted(common_channels))}

File processing details:
"""

    for i, filename in enumerate(input_files):
        report_content += f"\n- {os.path.basename(filename)}: Retention rate {retention_rates[i]:.1f}%"

    report_content += f"\n\nAverage channel retention rate: {np.mean(retention_rates):.1f}%"
    report_content += f"\nMinimum channel retention rate: {np.min(retention_rates):.1f}%"
    report_content += f"\nMaximum channel retention rate: {np.max(retention_rates):.1f}%"

    # Save report
    report_path = os.path.join(output_dir, "unification_report.txt")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)

    print(f"Processing report saved: {report_path}")

def verify_unification_results(original_dir, unified_dir):
    print("\nVerifying unification results...")

    original_files = glob.glob(os.path.join(original_dir, "*.set"))
    unified_files = glob.glob(os.path.join(unified_dir, "unified_*.set"))

    if len(original_files) != len(unified_files):
        print(" File count mismatch")
        return

    # Check if all unified files have the same channels
    unified_channels = []
    for u_file in unified_files:
        try:
            raw = mne.io.read_raw_eeglab(u_file, preload=False, verbose='error')
            unified_channels.append(set(raw.ch_names))
        except:
            continue

    if unified_channels:
        common_unified = set.intersection(*unified_channels)
        print(f"Common channels after unification: {len(common_unified)}")
        print(f"Channel list: {sorted(common_unified)}")

        # Check if all files have consistent channels
        all_same = all(ch_set == common_unified for ch_set in unified_channels)
        if all_same:
            print(" All files have completely consistent channels")
        else:
            print(" Channel differences still exist between files")

if __name__ == "__main__":
    # Configure paths
    input_dir = r""   
    output_dir = r""

    print("Starting unification processing that only retains common channels...")
    unify_common_channels_only(input_dir, output_dir)

    # Optional: Verify results
    verify_unification_results(input_dir, output_dir)

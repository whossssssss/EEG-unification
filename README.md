# EEG Unification Tool

##  Introduction

When conducting multi-subject EEG data analysis, it's common to encounter inconsistencies in electrode channels across different subjects. This tool automatically identifies common channels across multiple EEG files and retains only these common channels, ensuring all files have identical channel configurations for subsequent batch analysis and processing.

###  Key Features

-  **Precise Identification**: Automatically finds common channels across multiple .set files
-  **Minimal Intervention**: Retains only common channels while preserving original data to the greatest extent
-  **Comprehensive Reports**: Generates detailed processing reports including channel retention rates
-  **Result Validation**: Provides validation functionality to ensure correct unification
-  **Batch Processing**: Supports batch processing of multiple files
-  **Safety Mechanism**: Issues warnings when channel retention rates are too low

##  Installation

### Requirements
- Python 3.7 or higher
- pip package manager

##  Quick Start

### Basic Usage

```python
# Set input and output paths
input_dir = "./data/raw_eeg"      # Raw data folder
output_dir = "./data/unified_eeg" # Output folder

# Execute unification processing
unify_common_channels_only(
    input_dir=input_dir,
    output_dir=output_dir,
    file_pattern="*.set"  # Can be modified for other file formats
)
```

##  Output Example

### Console Output
```
Found 5 files for unification
 subject1.set: 32 channels
 subject2.set: 30 channels
 subject3.set: 32 channels
 subject4.set: 28 channels
 subject5.set: 32 channels

Common Channel Analysis:
Number of files: 5
Number of common channels: 26
Common channel list: ['Fz', 'Cz', 'Pz', 'F3', 'F4', ...]

Channel Retention Rate Analysis:
subject1.set: 32 → 26 channels (81.2%)
subject2.set: 30 → 26 channels (86.7%)
subject3.set: 32 → 26 channels (81.2%)
subject4.set: 28 → 26 channels (92.9%)
subject5.set: 32 → 26 channels (81.2%)

Average channel retention rate: 84.6%
```

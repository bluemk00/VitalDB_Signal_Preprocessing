#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2024 Kyoungsuk Park

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Description:
    This script extracts clean physiological signal segments (ABP, PPG, ECG) from raw data,
    processes valid ranges based on precomputed indices, applies stringent signal quality checks,
    and saves the cleaned segments for further analysis.

    Features:
    - Identifies valid overlapping segments using precomputed valid indices.
    - Applies signal quality validation via `remove_bad_signals` to ensure segment cleanliness.
    - Extracts overlapping 60-second segments with a 10-second overlap.
    - Saves processed and cleaned segments for each case as .npy files.

    Input:
    - Directory containing raw .npy files with signal data (ABP, PPG, ECG).
    - Directory containing .npy files with precomputed valid indices.

    Output:
    - Directory containing .npy files with processed and cleaned signal segments.

    Usage:
    - Configure the `source_dir`, `index_dir`, and `output_dir` paths.
    - Adjust constants like sampling rate (`fs`) and segment/overlap lengths as needed.
    - Run the script using Python 3.

    Example:
    ```bash
    python extract_clean_segments.py
    ```
"""

import os
import numpy as np
from functions import is_clean_segment  # Import signal validation function

# Directories
source_dir = './Data/VitalDB/raw/'  # Directory containing raw signal .npy files
index_dir = './Data/VitalDB/valid_index/'  # Directory containing valid indices for each case
output_dir = './Data/VitalDB/processed/'  # Directory to save processed segments
os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists

# Constants
fs = 100  # Sampling rate in Hz
intv = fs * 60  # Segment length (60 seconds)
ovlp = fs * 10  # Overlapping length (10 seconds)

if __name__ == "__main__":
    # Get the list of raw data files and index files
    raw_files = {filename for filename in os.listdir(source_dir) if filename.endswith('.npy')}
    index_files = {filename for filename in os.listdir(index_dir) if filename.endswith('.npy')}

    # Find the intersection of file names
    rawdata_list = sorted(raw_files & index_files)  # Sorted list of common file names

    if not rawdata_list:
        print("No matching files found between raw signals and valid indices.")
    else:
        print(f"Found {len(rawdata_list)} matching files.")

    # Process each file in the intersection
    for file_name in rawdata_list:
        case_id = int(file_name[:4])  # Extract case ID from the file name

        # Load raw signal data and valid indices
        data = np.load(os.path.join(source_dir, file_name), allow_pickle=True)
        valid_indices = np.load(os.path.join(index_dir, file_name), allow_pickle=True)

        # Initialize segment lists
        abp_segments = []
        ppg_segments = []
        ecg_segments = []

        # Process each valid range in valid indices
        for start_idx, end_idx in valid_indices:
            segment_length = end_idx - start_idx

            # Process overlapping segments within the valid range
            for j in range(0, max(1, (segment_length - ovlp) // (intv - ovlp))):
                seg_start = start_idx + j * (intv - ovlp)  # Start of the segment
                seg_end = seg_start + intv  # End of the segment

                # Ensure the segment doesn't exceed the valid range
                if seg_end > end_idx:
                    break

                # Extract overlapping segment
                abp_seg = data.item()['ABP'][seg_start:seg_end]
                ppg_seg = data.item()['PPG'][seg_start:seg_end]
                ecg_seg = data.item()['ECG'][seg_start:seg_end]

                # Skip if the segment is shorter than the required length
                if len(abp_seg) < intv or len(ppg_seg) < intv or len(ecg_seg) < intv:
                    continue

                # Validate the segment
                decision = is_clean_segment(abp_seg, ppg_seg, ecg_seg, intv, fs)
                if decision == 1:
                    abp_segments.append(abp_seg)
                    ppg_segments.append(ppg_seg)
                    ecg_segments.append(ecg_seg)

        # Save the processed segments if any valid segments exist
        if abp_segments and ppg_segments and ecg_segments:
            save_path = os.path.join(output_dir, file_name)  # Save path for processed segments
            np.save(save_path, {
                "ABP": np.array(abp_segments),
                "PPG": np.array(ppg_segments),
                "ECG": np.array(ecg_segments)
            })
            print(f"Processed {file_name}: Saved to {save_path}")

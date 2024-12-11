#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2024 [Your Name]

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
    This script processes physiological signals (ABP, PPG, ECG) stored in .npy files,
    identifies valid chunks based on predefined criteria, and saves the valid indices
    for each case as .npy files.

    Features:
    - Validates ABP, PPG, and ECG signals using configurable lower and upper bounds.
    - Extracts overlapping valid chunks across all three signals.
    - Ensures chunks meet a minimum duration requirement, including a buffer margin.
    - Saves the valid indices for each case in the specified output directory.

    Input:
    - Directory containing .npy files with signal data (e.g., ABP, PPG, ECG).

    Output:
    - Directory containing .npy files with valid indices for each case.
      Each file contains a list of tuples representing the start and end indices
      of valid overlapping chunks.

    Usage:
    - Set the input directory (`npy_dir`) containing the raw .npy files.
    - Set the output directory (`index_dir`) where the valid index files will be saved.
    - Configure signal validation parameters (bounds, duration, buffer, etc.).
    - Run the script using Python 3.

    Example:
    ```bash
    python extract_valid_chunks.py
    ```
"""

import os
import numpy as np
from functions import process_signals

# Parameters for directories
npy_dir = './Data/VitalDB/raw/'  # Directory containing .npy files with signal data
index_dir = './Data/VitalDB/valid_index/'  # Directory to save valid index .npy files

# Parameters for signal validation
abp_bounds = (20, 200)  # ABP valid range
ppg_bounds = (5, 95)    # PPG valid range
ecg_bounds = (-1, 2)    # ECG valid range
min_duration = 60       # Minimum valid duration in seconds
buffer_seconds = 5      # Buffer duration in seconds
sampling_rate = 100     # Sampling rate in Hz

if __name__ == "__main__":
    # Create the output directory if it doesn't exist
    os.makedirs(index_dir, exist_ok=True)

    # List of all .npy files in the input directory
    npys = [filename for filename in os.listdir(npy_dir) if filename.endswith('.npy')]

    # Process each .npy file
    for i, caseid_npy in enumerate(npys):
        # Load the signal data
        tmp = np.load(f'{npy_dir}{caseid_npy}', allow_pickle=True)
        signals = tmp.item()

        # Extract individual signals
        abp = signals['ABP']
        ppg = signals['PPG']
        ecg = signals['ECG']

        # Process signals to get valid overlapping chunks
        overlapping_chunks = process_signals(
            abp, ppg, ecg,
            abp_bounds, ppg_bounds, ecg_bounds,
            min_duration, buffer_seconds, sampling_rate
        )

        # Save the valid indices for this caseid only if valid chunks are found
        if overlapping_chunks:
            np.save(f'{index_dir}{caseid_npy}', overlapping_chunks)
            print(f"Processed {caseid_npy}: Found {len(overlapping_chunks)} valid chunks.")
        else:
            print(f"Processed {caseid_npy}: No valid chunks found.")

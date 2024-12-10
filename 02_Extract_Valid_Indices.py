#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Kyoungsuk Park
Date: 2024-12-10
Description: 
    This script processes physiological signals (ABP, PPG, ECG) stored in .npy files,
    identifies valid segments based on predefined criteria, and saves the valid indices
    for each case as .npy files.

    Features:
    - Validates ABP, PPG, and ECG signals using configurable lower and upper bounds.
    - Extracts overlapping valid segments across all three signals.
    - Ensures segments meet a minimum duration requirement, including a buffer margin.
    - Saves the valid indices for each case in the specified output directory.

    Input:
    - Directory containing .npy files with signal data (e.g., ABP, PPG, ECG).

    Output:
    - Directory containing .npy files with valid indices for each case.
      Each file contains a list of tuples representing the start and end indices
      of valid overlapping segments.

    Usage:
    - Set the input directory (`npy_dir`) containing the raw .npy files.
    - Set the output directory (`index_dir`) where the valid index files will be saved.
    - Configure signal validation parameters (bounds, duration, buffer, etc.).
    - Run the script using Python 3.

    Example:
    ```
    npy_dir = './Data/VitalDB/raw/'
    index_dir = './Data/VitalDB/valid_index/'
    python extract_valid_indices.py
    ```
"""

import os
import numpy as np
from functions import process_signals

# Directories
npy_dir = './Data/VitalDB/raw/'  # Directory containing .npy files with signal data
index_dir = './Data/VitalDB/valid_index/'  # Directory to save valid index .npy files
os.makedirs(index_dir, exist_ok=True)  # Create the output directory if it doesn't exist

# List of all .npy files in the input directory
npys = [filename for filename in os.listdir(npy_dir) if filename.endswith('.npy')]

# Parameters for signal validation
abp_bounds = (20, 200)  # ABP valid range
ppg_bounds = (5, 95)    # PPG valid range
ecg_bounds = (-2, 2)    # ECG valid range
min_duration = 60       # Minimum valid duration in seconds
buffer_seconds = 5      # Buffer duration in seconds
sampling_rate = 100     # Sampling rate in Hz

# Process each .npy file
for i, caseid_npy in enumerate(npys):
    # Load the signal data
    tmp = np.load(f'{npy_dir}{caseid_npy}', allow_pickle=True)
    signals = tmp.item()
    
    # Extract individual signals
    abp = signals['ABP']
    ppg = signals['PPG']
    ecg = signals['ECG']
    
    # Process signals to get valid overlapping segments
    overlapping_segments = process_signals(
        abp, ppg, ecg,
        abp_bounds, ppg_bounds, ecg_bounds,
        min_duration, buffer_seconds, sampling_rate
    )
    
    # Save the valid indices for this caseid
    np.save(f'{index_dir}{caseid_npy}', overlapping_segments)

    print(f"Processed {caseid_npy}: Found {len(overlapping_segments)} valid segments.")

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
    This script extracts specific physiological signals (ART, PPG, ECG) from VitalDB cases,
    resamples them at a user-defined sampling rate (default: 100Hz) for multimodal analysis,
    and saves the data as NumPy files.

    Signals processed:
    - ART (Arterial Blood Pressure): Captures continuous blood pressure waveform.
    - PPG (Photoplethysmogram): Measures blood volume changes for heart rate variability analysis.
    - ECG (Electrocardiogram): Records electrical activity of the heart, focusing on QRS complexes.

    Why a unified sampling rate?
    - A consistent sampling rate ensures alignment across modalities for synchronized analysis.
    - 100Hz (default): Balances sufficient detail for ART, PPG, and ECG signals with computational efficiency.
    - ART: Typically requires 20-40Hz for waveform details; 100Hz is more than adequate.
    - PPG: Effective range is 0.5-5Hz; 100Hz improves precision for heart rate variability.
    - ECG: Standard analysis needs 128Hz or higher, but 100Hz remains practical for most purposes.

    Case ID and Clinical Information:
    - Each `caseid` serves as the key in the `Clinical_Information.csv` file, enabling linkage between signal data and clinical metadata.

    Prerequisite:
    - Install the `vitaldb` library before running this script.
      Installation command: pip install vitaldb
    - Install tqdm for progress bar visualization.
      Installation command: pip install tqdm

    Usage:
    - Ensure you have VitalDB and tqdm installed in your environment.
    - Configure the `save_dir` to your desired location for saving the output files.
    - Adjust the `sampling_rate` parameter if needed (default is 100Hz).
    - Run the script using Python 3.
"""

import os
import numpy as np
import vitaldb
from tqdm import tqdm  # For progress bar visualization

# Parameters for signal extraction
signals = ['ART', 'PLETH', 'ECG_II']  # List of signal types to be extracted
sampling_rate = 100  # Sampling rate in Hz
save_dir = './Data/VitalDB/raw/'  # Directory to save the extracted data

if __name__ == "__main__":
    # Create the output directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)

    # Find case IDs that include the specified signals
    caseids = vitaldb.find_cases(signals)
    print(f"Total number of case IDs containing the specified signals: {len(caseids)}")

    # Loop through each case ID and process the data with a progress bar
    for caseid in tqdm(caseids, desc="Processing Cases", unit="case"):
        # Load the case data with the specified signals and the user-defined sampling rate
        vals = vitaldb.load_case(caseid, signals, 1 / sampling_rate)
        
        # Format the caseid as a 4-digit zero-padded string
        formatted_caseid = f"{int(caseid):04d}"
        
        # Save the extracted signals (ART, PPG, ECG) into a NumPy file
        np.save(f"{save_dir}{formatted_caseid}.npy", {'ABP': vals[:, 0], 'PPG': vals[:, 1], 'ECG': vals[:, 2]})

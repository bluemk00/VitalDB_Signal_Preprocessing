#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: functions.py
Author: Kyoungsuk Park
Date: 2024-12-10
Description:
    This module contains utility functions for processing physiological signals, 
    including signal validation, chunk extraction, overlap detection, and bad signal detection.

    Current Functions:
    - generate_valid_index_sequence: Generates a binary sequence representing valid indices (1 for valid, 0 for invalid).
    - find_continuous_chunks: Identifies continuous valid chunks based on binary index sequences.
    - process_signals: Finds overlapping valid chunks across multiple signals.
    - is_clean_segment: Validates individual 60-second signal segments based on peak characteristics and consistency.

    Usage:
    Import this module into your main script or notebook to use its functions.
    Example:
        from functions import (
            generate_valid_index_sequence, 
            find_continuous_chunks, 
            process_signals,
            is_clean_segment
        )
"""

# Imports
import numpy as np
from sklearn.preprocessing import minmax_scale
import heartpy as hp

def generate_valid_index_sequence(signal, lower_bound, upper_bound):
    """
    Generate a binary sequence representing valid indices (1 for valid, 0 for invalid),
    considering NaN values as invalid.

    Parameters:
        signal (np.array): Input signal array.
        lower_bound (float): Minimum valid value for the signal.
        upper_bound (float): Maximum valid value for the signal.

    Returns:
        np.array: Binary sequence with 1 for valid and 0 for invalid indices.

    Example:
        signal = np.array([np.nan, 50, 120, np.nan, 30, 250, 10, 80])
        valid_indices = generate_valid_index_sequence(signal, 20, 200)
        print(valid_indices)  # Output: [0 1 1 0 1 0 0 1]
    """
    valid_indices = np.where(np.isnan(signal), 0, 1)
    valid_indices = np.where((signal >= lower_bound) & (signal <= upper_bound), valid_indices, 0)
    return valid_indices

def find_continuous_chunks(index_sequence, min_duration, sampling_rate):
    """
    Identify continuous chunks of 1's in a binary index sequence.

    Parameters:
        index_sequence (np.array): Binary sequence (1 for valid, 0 for invalid).
        min_duration (int): Minimum duration for a valid chunk in seconds.
        sampling_rate (int): Sampling rate in Hz.

    Returns:
        List of tuples: Start and end indices of valid continuous chunks.

    Example:
        index_sequence = np.array([0, 1, 1, 0, 1, 1, 1, 0])
        chunks = find_continuous_chunks(index_sequence, 2, 1)
        print(chunks)  # Output: [(1, 3), (4, 7)]
    """
    min_points = min_duration * sampling_rate
    chunks = []
    start_idx = None

    for i, value in enumerate(index_sequence):
        if value == 1:
            if start_idx is None:
                start_idx = i
        else:
            if start_idx is not None:
                if i - start_idx >= min_points:
                    chunks.append((start_idx, i))
                start_idx = None

    if start_idx is not None and len(index_sequence) - start_idx >= min_points:
        chunks.append((start_idx, len(index_sequence)))

    return chunks

def process_signals(abp, ppg, ecg, abp_bounds, ppg_bounds, ecg_bounds, min_duration, buffer_seconds, sampling_rate):
    """
    Process ABP, PPG, and ECG signals to find overlapping valid chunks.

    Parameters:
        abp (np.array): ABP signal array.
        ppg (np.array): PPG signal array.
        ecg (np.array): ECG signal array.
        abp_bounds (tuple): (lower_bound, upper_bound) for ABP signal.
        ppg_bounds (tuple): (lower_bound, upper_bound) for PPG signal.
        ecg_bounds (tuple): (lower_bound, upper_bound) for ECG signal.
        min_duration (int): Minimum duration of valid chunks in seconds.
        buffer_seconds (int): Buffer duration to account for extra margins (in seconds).
        sampling_rate (int): Sampling rate in Hz.

    Returns:
        List of tuples: Start and end indices of overlapping valid chunks (buffers removed).
    """
    abp_indices = generate_valid_index_sequence(abp, *abp_bounds)
    ppg_indices = generate_valid_index_sequence(ppg, *ppg_bounds)
    ecg_indices = generate_valid_index_sequence(ecg, *ecg_bounds)
    combined_indices = abp_indices * ppg_indices * ecg_indices
    total_min_duration = min_duration + 2 * buffer_seconds
    overlapping_chunks = find_continuous_chunks(combined_indices, total_min_duration, sampling_rate)
    buffer_size = buffer_seconds * sampling_rate
    trimmed_chunks = [
        (start + buffer_size, end - buffer_size)
        for start, end in overlapping_chunks
        if (end - start) > 2 * buffer_size
    ]
    return trimmed_chunks

def is_clean_segment(abp, ppg, ecg, sig_length, fs=100):
    """
    Validate 60-second signal segments (PPG, ABP, ECG) based on peak characteristics and consistency.

    Parameters:
        abp (np.array): Arterial Blood Pressure signal.
        ppg (np.array): Photoplethysmogram signal.
        ecg (np.array): Electrocardiogram signal.
        sig_length (int): Total length of the segment in points (e.g., 60s * fs).
        fs (int): Sampling frequency in Hz (default is 100 Hz).

    Returns:
        int: 1 if the signal segment passes validation criteria, 0 otherwise.

    Validation Steps:
        1. Check for NaN values in the signals.
        2. Normalize signals to the range [0, 1].
        3. Detect peaks in each signal using the `heartpy` library.
        4. Validate peak distances, amplitudes, and counts against predefined thresholds.
        5. Ensure amplitude differences between consecutive peaks are within acceptable limits.
        6. Perform additional consistency checks to ensure signal variability.

    Example:
        decision = remove_bad_signals(abp, ppg, ecg, sig_length=6000, fs=100)
        if decision == 1:
            print("This segment is clean.")
        else:
            print("This segment is NOT clean.")
    """

    # Check for NaN values in signals
    if np.any(np.isnan(ppg)) or np.any(np.isnan(abp)) or np.any(np.isnan(ecg)):
        return 0

    # Normalize signals to [0, 1]
    PPG = minmax_scale(ppg)
    ABP = minmax_scale(abp)
    ECG = minmax_scale(ecg)

    # Helper function to validate peaks
    def validate_peaks(signal, fs, min_peaks, max_std_dist, max_std_peak):
        try:
            wd, _ = hp.process(signal, sample_rate=fs)
            peaks = wd['peaklist']
            peak_dist = np.diff(peaks)
            std_peak_dist = np.std(peak_dist)
            std_peaks = np.std(signal[peaks])
            num_peaks = len(peaks)

            # Validation conditions
            if std_peak_dist > max_std_dist or std_peaks > max_std_peak or num_peaks < min_peaks:
                return 0, peaks, peak_dist
            return 1, peaks, peak_dist
        except Exception:
            return 0, [], []

    # Validate PPG signal
    min_peaks_ppg = int(sig_length / (fs * 2))
    valid_ppg, pks_ppg, dist_ppg = validate_peaks(PPG, fs, min_peaks_ppg, max_std_dist=10, max_std_peak=0.2)
    if not valid_ppg:
        return 0

    # Ensure PPG peaks are within reasonable range
    if (pks_ppg[0] > 1.5 * np.mean(dist_ppg)) or (sig_length - pks_ppg[-1] > 1.5 * np.mean(dist_ppg)):
        return 0

    # Validate ABP signal
    min_peaks_abp = int(sig_length / (fs * 2))
    valid_abp, pks_abp, dist_abp = validate_peaks(ABP, fs, min_peaks_abp, max_std_dist=5, max_std_peak=0.15)
    if not valid_abp:
        return 0

    # Ensure ABP peaks are within reasonable range
    if (pks_abp[0] > 1.6 * np.mean(dist_abp)) or (sig_length - pks_abp[-1] > 1.6 * np.mean(dist_abp)):
        return 0

    # Validate ECG signal
    min_peaks_ecg = int(sig_length / (fs * 2))
    valid_ecg, pks_ecg, dist_ecg = validate_peaks(ECG, fs, min_peaks_ecg, max_std_dist=20, max_std_peak=0.6)
    if not valid_ecg:
        return 0

    # Ensure peak differences are reasonable for ECG
    if ((pks_ecg[0] > 1.5 * np.mean(dist_ecg)) or (sig_length - pks_ecg[-1] > 1.5 * np.mean(dist_ecg))):
        return 0

    # Check amplitude differences for consecutive peaks
    peak_diff_ecg = [np.abs(ECG[pks_ecg[i+1]] - ECG[pks_ecg[i]]) for i in range(len(pks_ecg) - 1)]

    if peak_diff_ecg and np.max(peak_diff_ecg) > 0.6:
        return 0

    # Additional ECG consistency checks
    low_diff_threshold = 0.01
    left_ecg_check = np.sum(np.abs(np.diff(ECG[:len(ECG)//2])) < low_diff_threshold)
    right_ecg_check = np.sum(np.abs(np.diff(ECG[len(ECG)//2:])) < low_diff_threshold)

    if left_ecg_check < 2 or right_ecg_check < 2:
        return 0

    return 1

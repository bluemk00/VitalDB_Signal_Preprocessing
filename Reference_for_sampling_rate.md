# **Guidelines for Selecting Sampling Rates in Physiological Signal Analysis**

This document focuses on determining appropriate sampling rates for analyzing physiological signals such as PPG, ECG, and ABP. It highlights the influence of signal characteristics and analysis objectives on sampling frequency decisions and provides recommendations based on reference settings and practical considerations.

---

## **Reference Settings for Apple's Experiment**

The following settings are derived from Apple's experimental configuration for processing PPG and ECG signals (not multimodal). These parameters serve as a benchmark for specific signal analysis use cases:

### **PPG (Photoplethysmogram)**
- **Segment Length**: 60 seconds
- **Downsampling**: 64Hz
- **Data Points**: 3840 per segment
- **Filtering**: Bandpass filter (0.5Hz–5Hz)

### **ECG (Electrocardiogram)**
- **Segment Length**: 30 seconds
- **Downsampling**: 128Hz
- **Data Points**: 3840 per segment
- **Filtering**: Bandpass filter (0.5Hz–40Hz)

---

## **Signal-Specific Considerations**

### **Nyquist Theorem**
- The sampling rate should be at least twice the highest frequency component of interest to avoid aliasing.

### **PPG**
- **Frequency Range**: 0.4–5Hz
- **Minimum Sampling Rate**: 10Hz
- **Key Analysis**: Heart rate variability, respiratory-related variations.

### **ECG**
- **Frequency Range**: 0.5–40Hz
- **Minimum Sampling Rate**: 80Hz
- **Key Analysis**: QRS complex analysis, arrhythmia detection.

### **ABP (Arterial Blood Pressure)**
- **Frequency Range**: 0.5–20Hz
- **Minimum Sampling Rate**: 40Hz
- **Key Analysis**: Blood pressure variability, waveform dynamics.

---

## **Sampling Rate Considerations**

### **Common Sampling Frequencies**
| Sampling Rate | Application                                       |
|---------------|---------------------------------------------------|
| **10–20Hz**   | Slow physiological trends (e.g., mean blood pressure) |
| **32Hz**      | Low-frequency analysis (e.g., long-term heart rate trends) |
| **64Hz**      | Standard for PPG and ABP signals, heart rate, and variability analysis |
| **128Hz**     | Common for ECG analysis, precise heart rate monitoring |
| **256Hz+**    | High-frequency ECG analysis, QRS complex and arrhythmia detection |

---

## **Suitability of 100Hz Sampling Rate**

### **Broad Compatibility Across Signals**
- **PPG and ABP**:
  - Exceeds the Nyquist requirement for PPG (0.4–5Hz) and ABP (0.5–20Hz).
  - Provides sufficient detail for heart rate variability and blood pressure waveform analysis.
- **ECG**:
  - While 128Hz is often used for precise QRS complex analysis, 100Hz is adequate for standard rhythm and waveform monitoring.

### **Multimodal Synchronization**
- A unified 100Hz sampling rate facilitates synchronization across modalities, ensuring alignment without requiring interpolation.

### **Efficiency**
- Balances data resolution, storage needs, and computational load, making it a practical choice for large-scale datasets like VitalDB.

---

Author: **K. Park**  
Date: **2024-12-11**  

This guide aims to assist researchers and practitioners in setting up and analyzing physiological signal data, providing practical recommendations and reference configurations for diverse applications.

---

**References**
1. Abbaspourazad, Salar, et al. "Large-scale training of foundation models for wearable biosignals." arXiv preprint arXiv:2312.05409 (2023).
2. Ismail, Shahid, Usman Akram, and Imran Siddiqi. "Heart rate tracking in photoplethysmography signals affected by motion artifacts: A review." EURASIP Journal on Advances in Signal Processing 2021.1 (2021): 5.
3. Kligfield, Paul, et al. "Recommendations for the standardization and interpretation of the electrocardiogram: part I: the electrocardiogram and its technology: a scientific statement from the American Heart Association Electrocardiography and Arrhythmias Committee, Council on Clinical Cardiology; the American College of Cardiology Foundation; and the Heart Rhythm Society endorsed by the International Society for Computerized Electrocardiology." Circulation 115.10 (2007): 1306-1324.

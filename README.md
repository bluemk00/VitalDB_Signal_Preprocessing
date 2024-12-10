# VitalDB Signal Extraction and Clinical Data Matching

This repository contains two Python scripts for processing physiological signal data and clinical information from the VitalDB dataset. The scripts facilitate multimodal analysis by extracting and resampling physiological signals and matching diagnostic labels (`dx`) with standardized ICD-10 codes.

---

## **Scripts**

### 1. **`01_VitalDB_Signal_Extraction_Script.py`**
#### **Purpose**
- Extracts physiological signals (`ART`, `PPG`, and `ECG`) from VitalDB cases.
- Resamples the signals at a user-defined sampling rate (default: 100Hz).
- Saves the processed data as NumPy files for further analysis.

#### **Features**
- Progress bar visualization using `tqdm`.
- Default sampling rate is 100Hz, ensuring consistent resolution across modalities for multimodal analysis.
- Supports linking signal data with clinical metadata using `caseid` as a key.

#### **Usage**
1. Install dependencies:
   ```bash
   pip install vitaldb tqdm
   ```
2. Run the script:
   ```bash
   python 01_VitalDB_Signal_Extraction_Script.py
   ```

#### **Inputs**
- `Clinical_Information.csv`: Contains clinical metadata for linking.
- Signal data from VitalDB.

#### **Outputs**
- NumPy files for each case (`caseid`), containing the extracted and resampled signals:
  - `ABP` (Arterial Blood Pressure)
  - `PPG` (Photoplethysmogram)
  - `ECG` (Electrocardiogram)

---

### 2. **`02_Match_Clinical_Information_with_ICD10_Codes.py`**
#### **Purpose**
- Processes clinical data from `Clinical_Information.csv`.
- Matches non-standard diagnostic labels (`dx`) with standardized ICD-10 codes using a predefined mapping file.
- Outputs a merged file containing the original clinical data with corresponding ICD-10 codes.

#### **Features**
- Left joins clinical information with ICD-10 mappings based on the `dx` column.
- Outputs a comprehensive clinical file (`Clinical_Information_with_icd10.csv`) for downstream analysis.

#### **Usage**
1. Ensure the input files (`Clinical_Information.csv` and `vitaldb_dx_icd10_match.csv`) are available in the working directory.
2. Run the script:
   ```bash
   python 02_Match_Clinical_Information_with_ICD10_Codes.py
   ```

#### **Inputs**
- `Clinical_Information.csv`: Contains raw clinical metadata.
- `vitaldb_dx_icd10_match.csv`: Provides mappings between diagnostic labels (`dx`) and ICD-10 codes.

#### **Outputs**
- `Clinical_Information_with_icd10.csv`: Merged file containing clinical data and ICD-10 codes.

---

## **File Structure**
```
├── 01_VitalDB_Signal_Extraction_Script.py
├── 02_Match_Clinical_Information_with_ICD10_Codes.py
├── Clinical_Information.csv
├── vitaldb_dx_icd10_match.csv
├── VitalDB_raw/          # Directory for extracted NumPy files
├── Clinical_Information_with_icd10.csv
└── README.md
```

---

## **Dependencies**
- **Python 3.6+**
- **Required Libraries**:
  - `numpy`
  - `pandas`
  - `vitaldb`
  - `tqdm`

---

## **Contact**
Author: **Kyoungsuk Park**  
Date: **2024-12-10**  
Feel free to contact me for questions or support.
```

---

### **Highlights**
- The README is structured to clearly describe the purpose, usage, inputs, and outputs of both scripts.
- Includes installation instructions and file structure for easier understanding.
- Provides contact information and dependencies for replicability.

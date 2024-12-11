# VitalDB Signal Preprocessing

This repository contains four Python scripts for processing physiological signal data and clinical information from the VitalDB dataset. The scripts cover various stages of data preprocessing, including clinical data mapping, signal extraction, validation, and cleaning. These steps ensure high-quality multimodal datasets for further analysis, facilitating seamless integration between physiological signals and clinical metadata.

---

## **Scripts**

### **`00_Match_Clinical_Information_with_ICD10_Codes.py`**
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
   python 00_Match_Clinical_Information_with_ICD10_Codes.py
   ```

#### **Inputs**
- `Clinical_Information.csv`: Contains raw clinical metadata.
- `vitaldb_dx_icd10_match.csv`: Provides mappings between diagnostic labels (`dx`) and ICD-10 codes.

#### **Outputs**
- `Clinical_Information_with_icd10.csv`: Merged file containing clinical data and ICD-10 codes.

---

### **`01_VitalDB_Signal_Extraction_Script.py`**
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
- Signal data from VitalDB.

#### **Outputs**
- NumPy files for each case (`caseid`), containing the extracted and resampled signals:
  - `ABP` (Arterial Blood Pressure)
  - `PPG` (Photoplethysmogram)
  - `ECG` (Electrocardiogram)

---

### **`02_Extract_Valid_Indices.py`**
#### **Purpose**
- Processes extracted physiological signals (`ABP`, `PPG`, `ECG`) to identify valid overlapping chunks.
- Validates each signal using predefined bounds and extracts chunks that meet minimum duration and overlap criteria.
- Saves the valid indices for each case as `.npy` files.

#### **Features**
- Validates signals based on configurable lower and upper bounds.
- Identifies overlapping valid chunks across all three signals.
- Ensures chunks meet a minimum duration requirement, including a buffer margin.
- Saves valid indices for each case in the specified output directory.

#### **Usage**
1. Ensure the extracted signal data (`.npy` files) is stored in the input directory (`npy_dir`).
2. Run the script:
   ```bash
   python 02_Extract_Valid_Indices.py
   ```

#### **Inputs**
- `.npy` files containing extracted signal data for each case.

#### **Outputs**
- `.npy` files containing valid indices for each case in the output directory:
  - Each file contains a list of tuples representing the start and end indices of valid overlapping chunks.

---

### **`03_Extract_Clean_Segments.py`**
#### **Purpose**
- Extracts clean physiological signal segments (`ABP`, `PPG`, `ECG`) based on precomputed valid indices.
- Applies stringent signal quality checks to ensure the cleanliness of each segment.
- Saves cleaned signal segments for further analysis.

#### **Features**
- Identifies valid overlapping segments using precomputed valid indices.
- Applies signal quality validation via `is_clean_segment` to ensure segment cleanliness.
- Extracts overlapping 60-second segments with a 10-second overlap.
- Saves processed and cleaned segments for each case as `.npy` files.

#### **Usage**
1. Ensure the input signal data (`.npy` files) and valid indices (`.npy` files) are available.
2. Run the script:
   ```bash
   python 03_Extract_Clean_Segments.py
   ```

#### **Inputs**
- `.npy` files containing raw signal data (`ABP`, `PPG`, `ECG`).
- `.npy` files containing precomputed valid indices.

#### **Outputs**
- `.npy` files containing processed and cleaned signal segments:
  - Each file contains cleaned segments for `ABP`, `PPG`, and `ECG`.

---

## **File Structure**
```
├── 00_Match_Clinical_Information_with_ICD10_Codes.py
├── 01_VitalDB_Signal_Extraction_Script.py
├── 02_Extract_Valid_Indices.py
├── 03_Extract_Clean_Segments.py
├── Clinical_Information.csv
├── vitaldb_dx_icd10_match.csv
├── Data/
|   └── VitalDB/
|       ├── raw/          # Directory for extracted signal NumPy files
|       ├── valid_index/  # Directory for valid index NumPy files
|       └── processed/    # Directory for processed and cleaned signal segments
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
  - `heartpy`
  - `scikit-learn`

---

## Contact

If you have any questions, feel free to reach out:

- Email: [bluemk00@gmail.com](mailto:bluemk00@gmail.com)
- GitHub: [bluemk00](https://github.com/bluemk00)

---

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE.txt) file for details.

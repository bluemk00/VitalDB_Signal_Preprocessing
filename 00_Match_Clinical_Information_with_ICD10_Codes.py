#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Kyoungsuk Park
Date: 2024-12-10
Description:
    This script processes clinical data from `Clinical_Information.csv` and matches the `dx` column
    (diagnostic labels) with standardized ICD-10 codes provided in `vitaldb_dx_icd10_match.csv`.
    The output is a merged file, `Clinical_Information_with_icd10.csv`, which includes the original
    clinical data along with the corresponding ICD-10 codes.

    File sources:
    - `Clinical_Information.csv`: From VitalDB, containing raw clinical data.
    - `vitaldb_dx_icd10_match.csv`: Created by K. Park on 2024-09-05, providing mappings between
      non-standard diagnostic labels (`dx`) and the most similar ICD-10 codes.

    Key column:
    - `dx`: Used to merge clinical information with ICD-10 mappings.

    Output:
    - `Clinical_Information_with_icd10.csv`: The final file containing clinical data with ICD-10 codes.
"""

import numpy as np  # Import NumPy for numerical operations
import pandas as pd  # Import pandas for data manipulation
import os  # Import os for file path management

# Define the base directory where the input files are located
path_dir = './'

# Load clinical information data
df1 = pd.read_csv(path_dir + 'Clinical_Information.csv')  # Load Clinical_Information.csv into a DataFrame

# Load ICD-10 mapping data
df2 = pd.read_csv(path_dir + 'vitaldb_dx_icd10_match.csv')  # Load vitaldb_dx_icd10_match.csv into a DataFrame

# Merge the two DataFrames on the `dx` column
df3 = pd.merge(df1, df2, how='left', on='dx')  # Perform a left join on the `dx` column

# Save the merged DataFrame to a new CSV file
df3.to_csv(path_dir + 'Clinical_Information_with_icd10.csv', index=False)  # Save output without the index column

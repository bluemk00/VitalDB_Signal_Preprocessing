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

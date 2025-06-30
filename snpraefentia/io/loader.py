# Copyright 2025 SNPraefentia Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Data loading module.

This module handles the loading and preprocessing of input data for
the SNPraefentia analysis pipeline.
"""

import pandas as pd
import logging
import os

logger = logging.getLogger(__name__)


def validate_columns(df):
    """Validate that the DataFrame has all required columns with correct names.
    
    Args:
        df: DataFrame to validate
        
    Raises:
        ValueError: If required columns are missing or have incorrect names
    """
    required_columns = ['Evidence', 'Amino_Acid_Position', 'Effect', 'Gene']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        error_msg = (
            #f"Input file is missing required columns or has incorrect column names.\n"
            f"Missing/Incorrect columns: {'  '.join(missing_columns)}\n"
            f"Required column headers must be exactly: {'  '.join(required_columns)}"
        )
        raise ValueError(error_msg)

def load_data(file_path):
    """Load SNP data from a file.
    
    Supports CSV (.csv), TSV (.tsv, .txt), and Excel (.xlsx, .xls) formats.
    
    Args:
        file_path: Path to input file
        
    Returns:
        DataFrame with SNP data
    """
    file_ext = os.path.splitext(file_path)[1].lower()
    
    logger.debug(f"Loading data from {file_path} (format: {file_ext})")
    
    if file_ext in ['.xlsx', '.xls']:
        df = pd.read_excel(file_path)
    elif file_ext == '.csv':
        df = pd.read_csv(file_path)
    elif file_ext in ['.tsv', '.txt']:
        df = pd.read_csv(file_path, sep='\t')
    else:
        raise ValueError(f"Unsupported file format: {file_ext}. Supported formats: .csv, .tsv, .txt, .xlsx, .xls")
        
    # Validate column names
    validate_columns(df)
    
    logger.info(f"Loaded {len(df)} SNPs from {file_path}")
    return df
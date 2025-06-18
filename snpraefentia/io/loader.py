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

def load_data(file_path):
    """Load SNP data from a file.
    
    Supports CSV (.csv), TSV (.tsv, .txt), and Excel (.xlsx, .xls) formats.
    
    Args:
        file_path: Path to input file
        
    Returns:
        DataFrame with SNP data
    """
    try:
        file_ext = os.path.splitext(file_path)[1].lower()
        
        logger.debug(f"Loading data from {file_path} (format: {file_ext})")
        
        if file_ext in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        elif file_ext == '.csv':
            df = pd.read_csv(file_path)
        elif file_ext in ['.tsv', '.txt']:
            df = pd.read_csv(file_path, sep='\t')
        else:
            raise ValueError(f"Unsupported file format: {file_ext}. Supported formats: .xlsx, .xls, .csv, .tsv, .txt")
        
        logger.info(f"Loaded {len(df)} SNPs from {file_path}")
        return df
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise ValueError(f"Could not load data from {file_path}: {str(e)}")
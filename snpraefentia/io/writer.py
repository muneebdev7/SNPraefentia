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
"""Data writing module.

This module handles the output and formatting of results from
the SNPraefentia analysis pipeline.
"""

import logging
import os

logger = logging.getLogger(__name__)

def save_data(df, file_path):
    """Save processed SNP data to a file.
    
    Supports CSV (.csv), TSV (.tsv, .txt), and Excel (.xlsx, .xls) formats.
    
    Args:
        df: DataFrame with processed SNP data
        file_path: Path to save output file
    """
    try:
        file_ext = os.path.splitext(file_path)[1].lower()
        
        logger.debug(f"Saving data to {file_path} (format: {file_ext})")
        
        if file_ext in ['.xlsx', '.xls']:
            df.to_excel(file_path, index=False)
        elif file_ext == '.csv':
            df.to_csv(file_path, index=False)
        elif file_ext in ['.tsv', '.txt']:
            df.to_csv(file_path, sep='\t', index=False)
        else:
            # Default to CSV if extension not recognized
            logger.warning(f"Unrecognized file extension: {file_ext}. Defaulting to CSV format.")
            df.to_csv(file_path, index=False)
            
        logger.info(f"Saved {len(df)} SNPs to {file_path}")
    except Exception as e:
        logger.error(f"Error saving data: {str(e)}")
        raise ValueError(f"Could not save data to {file_path}: {str(e)}")
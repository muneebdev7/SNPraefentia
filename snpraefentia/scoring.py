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
#
# PATENT NOTICE: This file contains patent-protected SNP scoring algorithms.
# The scoring methodologies and algorithms implemented in this module are
# protected by patent rights owned by the SNPraefentia Authors.
# A separate patent license may be required for any use of these algorithms.
"""Scoring functions for SNPraefentia.

This module implements the proprietary scoring algorithms used to prioritize
SNPs based on various features and characteristics analyzed by the package.
The scoring methodologies used here are patent-protected.
"""

import logging

logger = logging.getLogger(__name__)

def calculate_priority_score(df):
    """Calculate the final priority score for each SNP.
    
    Args:
        df: DataFrame with processed SNP data
        
    Returns:
        Series of priority scores
    """
    try:
        # Ensure domain position is numeric
        df['Domain_Position_Match'] = df['Domain_Position_Match'].fillna(0).astype(float)
        
        # Fill missing AA impact scores with 0
        df['Amino_Acid_Impact_Score'] = df['Amino_Acid_Impact_Score'].fillna(0)
        
        # Calculate score with fixed weights
        # Depth has highest weight (2.0) as it's a direct measure of evidence
        # AA impact and domain position have equal weights (1.0)
        score = (
            2.0 * df['Normalized_Depth'] + 
            1.0 * df['Amino_Acid_Impact_Score'] +
            1.0 * df['Domain_Position_Match']
        ) / 7
        
        logger.debug(f"Calculated priority scores (min={score.min()}, max={score.max()}, mean={score.mean()})")
        return score
        
    except Exception as e:
        logger.error(f"Error calculating priority score: {str(e)}")
        # Return zeros as fallback
        return [0] * len(df)
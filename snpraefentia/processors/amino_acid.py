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
# PATENT NOTICE: This software includes patent-protected methodologies.
"""Amino acid processing module.

This module handles amino acid change analysis and impact calculations
as part of the SNPraefentia analysis pipeline.
"""

import re
import logging
from ..db.aa_properties import AA_PROPERTIES

logger = logging.getLogger(__name__)

def extract_aa_change(effect_str):
    """Extract amino acid changes from EFFECT column.
    
    Args:
        effect_str: String containing effect information
        
    Returns:
        Amino acid change string (e.g., "AlaGly")
    """
    try:
        match = re.search(r'p\.([A-Z][a-z]{2}\d+[A-Z][a-z]{2})', str(effect_str))
        return match.group(1) if match else None
    except Exception as e:
        logger.debug(f"Could not extract AA change: {str(e)}")
        return None

def compute_aa_impact(row):
    """Calculate amino acid impact score.
    
    Args:
        row: DataFrame row containing AA_Change
        
    Returns:
        Impact score as a float
    """
    aa_change = row.get('AA_Change')
    if not isinstance(aa_change, str) or len(aa_change) < 6:
        return 0
    
    try:
        ref, mut = aa_change[:3], aa_change[-3:]
        
        if ref in AA_PROPERTIES and mut in AA_PROPERTIES:
            weight_diff = abs(AA_PROPERTIES[ref]['weight'] - AA_PROPERTIES[mut]['weight']) / 130
            hydro_diff = abs(AA_PROPERTIES[ref]['hydrophobicity'] - AA_PROPERTIES[mut]['hydrophobicity']) / 9
            polarity_change = int(AA_PROPERTIES[ref]['polarity'] != AA_PROPERTIES[mut]['polarity'])
            charge_change = int(AA_PROPERTIES[ref]['charge'] != AA_PROPERTIES[mut]['charge'])
            
            return round(weight_diff + hydro_diff + polarity_change + charge_change, 3)
    except Exception as e:
        logger.debug(f"Error computing AA impact: {str(e)}")
    
    return 0
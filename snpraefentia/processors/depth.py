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
"""Depth analysis module.

This module handles the processing and normalization of sequencing depth
data as part of the SNPraefentia analysis pipeline.
"""

import re
import logging
import numpy as np

logger = logging.getLogger(__name__)

def extract_depth(evidence):
    """Extract maximum depth from EVIDENCE column.
    
    Args:
        evidence: String containing depth information
        
    Returns:
        Maximum depth as an integer
    """
    try:
        matches = re.findall(r'\b([AGCT]):(\d+)', str(evidence))
        depths = [int(depth) for base, depth in matches]
        return max(depths) if depths else 0
    except Exception as e:
        logger.warning(f"Error extracting depth: {str(e)}")
        return 0

def normalize_depth(depth_series):
    """Normalize depth values to range [0, 1].
    
    Args:
        depth_series: Series of depth values
        
    Returns:
        Series of normalized depth values
    """
    min_depth = depth_series.min()
    max_depth = depth_series.max()
    
    if max_depth == min_depth:
        return np.ones(len(depth_series))
        
    return (depth_series - min_depth) / (max_depth - min_depth)
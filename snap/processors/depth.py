"""Depth processing functions for SNAP."""

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
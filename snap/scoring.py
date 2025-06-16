"""Scoring functions for SNAP."""

import logging

logger = logging.getLogger(__name__)

def calculate_priority_score(df, depth_weight=2.0, aa_weight=1.0, domain_weight=1.0):
    """Calculate the final priority score for each SNP.
    
    Args:
        df: DataFrame with processed SNP data
        depth_weight: Weight for normalized depth in priority score
        aa_weight: Weight for amino acid impact in priority score
        domain_weight: Weight for domain position in priority score
        
    Returns:
        Series of priority scores
    """
    try:
        # Ensure domain position is numeric
        df['Domain_Position_Match'] = df['Domain_Position_Match'].fillna(0).astype(float)
        
        # Fill missing AA impact scores with 0
        df['AA_Impact_Score'] = df['AA_Impact_Score'].fillna(0)
        
        # Calculate score
        #total_weight = depth_weight + aa_weight + domain_weight
        
        score = (
            depth_weight * df['Normalized_Depth'] + 
            aa_weight * df['AA_Impact_Score'] + 
            domain_weight * df['Domain_Position_Match']
        ) / 7
        
        logger.debug(f"Calculated priority scores (min={score.min()}, max={score.max()}, mean={score.mean()})")
        return score
        
    except Exception as e:
        logger.error(f"Error calculating priority score: {str(e)}")
        # Return zeros as fallback
        return [0] * len(df)
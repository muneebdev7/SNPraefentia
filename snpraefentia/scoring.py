"""Scoring functions for SNPraefentia."""

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
        df['AA_Impact_Score'] = df['AA_Impact_Score'].fillna(0)
        
        # Calculate score with fixed weights
        # Depth has highest weight (2.0) as it's a direct measure of evidence
        # AA impact and domain position have equal weights (1.0)
        score = (
            2.0 * df['Normalized_Depth'] + 
            1.0 * df['AA_Impact_Score'] +
            1.0 * df['Domain_Position_Match']
        ) / 7
        
        logger.debug(f"Calculated priority scores (min={score.min()}, max={score.max()}, mean={score.mean()})")
        return score
        
    except Exception as e:
        logger.error(f"Error calculating priority score: {str(e)}")
        # Return zeros as fallback
        return [0] * len(df)
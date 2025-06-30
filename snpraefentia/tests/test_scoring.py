"""Tests for SNPraefentia scoring functions."""

import unittest
import pandas as pd
from snpraefentia.scoring import calculate_priority_score

class TestScoring(unittest.TestCase):
    """Test scoring functions."""
    
    def setUp(self):
        """Set up test data."""
        self.test_df = pd.DataFrame({
            'Normalized_Depth': [0.2, 0.5, 0.8],
            'Amino_Acid_Impact_Score': [0.3, 0.6, 0.9],
            'Domain_Position_Match': [0, 1, 1]
        })
        
    def test_calculate_priority_score(self):
        """Test calculating the priority score."""
        # Test with default weights
        scores = calculate_priority_score(self.test_df)
        
        # Check length
        self.assertEqual(len(scores), 3)
        
        # Check bounds
        self.assertTrue(all(0 <= score <= 1 for score in scores))
        
        # Check relative order
        self.assertLess(scores[0], scores[1])
        self.assertLess(scores[1], scores[2])
        
        # Test with missing values
        df_with_na = self.test_df.copy()
        df_with_na.loc[1, 'Amino_Acid_Impact_Score'] = None
        scores_with_na = calculate_priority_score(df_with_na)
        
        # Should still calculate without errors
        self.assertEqual(len(scores_with_na), 3)

if __name__ == '__main__':
    unittest.main()
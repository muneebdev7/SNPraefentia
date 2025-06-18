"""Tests for the core SNPraefentia functionality."""

import unittest
import pandas as pd
from snpraefentia.core import SNPAnalyst

class TestSNPAnalyst(unittest.TestCase):
    """Test the SNPAnalyst class."""
    
    def setUp(self):
        """Set up test data."""
        self.analyst = SNPAnalyst()
        
        # Create a minimal test dataframe
        self.test_df = pd.DataFrame({
            'EVIDENCE': ['A:10 C:5', 'G:20 T:8', 'T:30 A:15'],
            'EFFECT': ['p.Ala123Gly', 'p.Trp456Leu', 'missense_variant'],
            'GENE': ['geneA', 'geneB', 'geneC'],
            'AA_POS': ['123/500', '456/300', '789/400']
        })
        
    def test_process_dataframe(self):
        """Test processing a dataframe."""
        species = "Escherichia coli"
        result = self.analyst.process_dataframe(self.test_df, species)
        
        # Check that all expected columns are present
        expected_columns = [
            'Bacterial_Species', 'TAX_ID', 'Max_Depth', 'Normalized_Depth',
            'AA_Change', 'AA_Impact_Score', 'Total_AA', 'Mutated_AA',
            'Final_Priority_Score', 'Final_Priority_Score_Percent'
        ]
        
        for col in expected_columns:
            self.assertIn(col, result.columns)
            
        # Check that bacterial species was added correctly
        self.assertEqual(result['Bacterial_Species'].iloc[0], species)
        
        # Check that depth was extracted correctly
        self.assertEqual(result['Max_Depth'].iloc[0], 10)
        self.assertEqual(result['Max_Depth'].iloc[1], 20)
        self.assertEqual(result['Max_Depth'].iloc[2], 30)
        
        # Check that AA change was extracted correctly
        self.assertEqual(result['AA_Change'].iloc[0], 'Ala123Gly')
        
        # Check that final score is between 0 and 1
        self.assertTrue(all(0 <= score <= 1 for score in result['Final_Priority_Score']))

if __name__ == '__main__':
    unittest.main()
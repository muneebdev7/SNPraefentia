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
            'Evidence': ['A:10 C:5', 'G:20 T:8', 'T:30 A:15'],
            'Effect': ['p.Ala123Gly', 'p.Trp456Leu', 'missense_variant'],
            'Gene': ['geneA', 'geneB', 'geneC'],
            'Amino_Acid_Position': ['123/500', '456/300', '789/400']
        })
        
    def test_process_dataframe(self):
        """Test processing a dataframe."""
        specie = "Escherichia coli"
        result = self.analyst.process_dataframe(self.test_df, specie)
        
        # Check that all expected columns are present
        expected_columns = [
            'Bacterial_Specie', 'Taxonomic_ID', 'Depth', 'Normalized_Depth',
            'AA_Change', 'Amino_Acid_Impact_Score', 'Total_Protein_Length', 'Mutated_AA',
            'Final_Priority_Score', 'Final_Priority_Score (%)'
        ]
        
        for col in expected_columns:
            self.assertIn(col, result.columns)
            
        # Check that bacterial specie was added correctly
        self.assertEqual(result['Bacterial_Specie'].iloc[0], specie)
        
        # Check that depth was extracted correctly
        self.assertEqual(result['Depth'].iloc[0], 10)
        self.assertEqual(result['Depth'].iloc[1], 20)
        self.assertEqual(result['Depth'].iloc[2], 30)
        
        # Check that AA change was extracted correctly
        self.assertEqual(result['AA_Change'].iloc[0], 'Ala123Gly')
        
        # Check that final score is between 0 and 1
        self.assertTrue(all(0 <= score <= 1 for score in result['Final_Priority_Score']))

if __name__ == '__main__':
    unittest.main()
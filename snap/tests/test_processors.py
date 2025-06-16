"""Tests for SNAP processors."""

import unittest
from snap.processors.depth import extract_depth, normalize_depth
from snap.processors.amino_acid import extract_aa_change, compute_aa_impact
import pandas as pd
import numpy as np

class TestDepthProcessor(unittest.TestCase):
    """Test depth processing functions."""
    
    def test_extract_depth(self):
        """Test extracting depth from evidence string."""
        self.assertEqual(extract_depth('A:10 C:5'), 10)
        self.assertEqual(extract_depth('G:20 T:8'), 20)
        self.assertEqual(extract_depth('T:30 A:15'), 30)
        self.assertEqual(extract_depth('Invalid'), 0)
        
    def test_normalize_depth(self):
        """Test depth normalization."""
        depths = pd.Series([10, 20, 30, 40, 50])
        normalized = normalize_depth(depths)
        
        # Check bounds
        self.assertAlmostEqual(normalized.min(), 0.0)
        self.assertAlmostEqual(normalized.max(), 1.0)
        
        # Check specific values
        self.assertAlmostEqual(normalized[0], 0.0)
        self.assertAlmostEqual(normalized[2], 0.5)
        self.assertAlmostEqual(normalized[4], 1.0)
        
        # Test with constant values
        constant_depths = pd.Series([10, 10, 10])
        constant_normalized = normalize_depth(constant_depths)
        self.assertTrue(np.all(constant_normalized == 1.0))

class TestAminoAcidProcessor(unittest.TestCase):
    """Test amino acid processing functions."""
    
    def test_extract_aa_change(self):
        """Test extracting amino acid change from effect string."""
        self.assertEqual(extract_aa_change('p.Ala123Gly'), 'Ala123Gly')
        self.assertEqual(extract_aa_change('missense_variant p.Trp456Leu'), 'Trp456Leu')
        self.assertIsNone(extract_aa_change('synonymous_variant'))
        self.assertIsNone(extract_aa_change(''))
        
    def test_compute_aa_impact(self):
        """Test computing amino acid impact score."""
        # Ala to Gly: small physicochemical change
        row_small_change = {'AA_Change': 'Ala123Gly'}
        score_small = compute_aa_impact(row_small_change)
        
        # Arg to Trp: large physicochemical change
        row_large_change = {'AA_Change': 'Arg456Trp'}
        score_large = compute_aa_impact(row_large_change)
        
        # Invalid input
        row_invalid = {'AA_Change': None}
        score_invalid = compute_aa_impact(row_invalid)
        
        # Check scores
        self.assertGreater(score_large, score_small)
        self.assertEqual(score_invalid, 0)

if __name__ == '__main__':
    unittest.main()
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
"""Amino acid properties database.

This module contains reference data for amino acid properties used in
the SNPraefentia analysis pipeline.
"""

# Amino acid properties
AA_PROPERTIES = {
    'Ala': {'weight': 89.1, 'polarity': 'nonpolar', 'charge': 'neutral', 'hydrophobicity': 1.8},
    'Arg': {'weight': 174.2, 'polarity': 'polar', 'charge': 'positive', 'hydrophobicity': -4.5},
    'Asn': {'weight': 132.1, 'polarity': 'polar', 'charge': 'neutral', 'hydrophobicity': -3.5},
    'Asp': {'weight': 133.1, 'polarity': 'polar', 'charge': 'negative', 'hydrophobicity': -3.5},
    'Cys': {'weight': 121.2, 'polarity': 'nonpolar', 'charge': 'neutral', 'hydrophobicity': 2.5},
    'Glu': {'weight': 147.1, 'polarity': 'polar', 'charge': 'negative', 'hydrophobicity': -3.5},
    'Gln': {'weight': 146.2, 'polarity': 'polar', 'charge': 'neutral', 'hydrophobicity': -3.5},
    'Gly': {'weight': 75.1, 'polarity': 'nonpolar', 'charge': 'neutral', 'hydrophobicity': -0.4},
    'His': {'weight': 155.2, 'polarity': 'polar', 'charge': 'positive', 'hydrophobicity': -3.2},
    'Ile': {'weight': 131.2, 'polarity': 'nonpolar', 'charge': 'neutral', 'hydrophobicity': 4.5},
    'Leu': {'weight': 131.2, 'polarity': 'nonpolar', 'charge': 'neutral', 'hydrophobicity': 3.8},
    'Lys': {'weight': 146.2, 'polarity': 'polar', 'charge': 'positive', 'hydrophobicity': -3.9},
    'Met': {'weight': 149.2, 'polarity': 'nonpolar', 'charge': 'neutral', 'hydrophobicity': 1.9},
    'Phe': {'weight': 165.2, 'polarity': 'nonpolar', 'charge': 'neutral', 'hydrophobicity': 2.8},
    'Pro': {'weight': 115.1, 'polarity': 'nonpolar', 'charge': 'neutral', 'hydrophobicity': -1.6},
    'Ser': {'weight': 105.1, 'polarity': 'polar', 'charge': 'neutral', 'hydrophobicity': -0.8},
    'Thr': {'weight': 119.1, 'polarity': 'polar', 'charge': 'neutral', 'hydrophobicity': -0.7},
    'Trp': {'weight': 204.2, 'polarity': 'nonpolar', 'charge': 'neutral', 'hydrophobicity': -0.9},
    'Tyr': {'weight': 181.2, 'polarity': 'polar', 'charge': 'neutral', 'hydrophobicity': -1.3},
    'Val': {'weight': 117.1, 'polarity': 'nonpolar', 'charge': 'neutral', 'hydrophobicity': 4.2}
}
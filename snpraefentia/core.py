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
# PATENT NOTICE: The SNP scoring algorithms and methodologies implemented
# in this software are protected by patent rights owned by the SNPraefentia
# Authors. Usage of these algorithms may require a separate patent license.
"""Core functionality for SNAP SNP prioritization.

This module provides the core functionality for SNP prioritization in the
SNPraefentia package. It includes functions for processing SNP data,
calculating impacts score, and managing the overall analysis workflow.
"""

import logging
import pandas as pd
from .processors.depth import extract_depth, normalize_depth
from .processors.amino_acid import extract_aa_change, compute_aa_impact
from .processors.taxonomy import get_taxid
from .processors.uniprot import search_uniprot, check_domain_position
from .io.loader import load_data
from .io.writer import save_data
from .scoring import calculate_priority_score

logger = logging.getLogger(__name__)

class SNPAnalyst:
    """Main class for SNP prioritization pipeline."""
    
    def __init__(self, uniprot_tolerance=50):
        """Initialize the SNP prioritizer with parameters.
        
        Args:
            uniprot_tolerance: Length tolerance when matching UniProt entries
        """
        self.uniprot_tolerance = uniprot_tolerance
        
    def run(self, input_file, species, output_file=None):
        """Run the SNP prioritization pipeline on an input file.
        
        Args:
            input_file: Path to input Excel file
            species: Bacterial species name
            output_file: Path to save output Excel file (optional)
            
        Returns:
            DataFrame with prioritized SNPs
        """
        logger.info("Loading input data...")
        df = load_data(input_file)
        
        # Process the dataframe
        result_df = self.process_dataframe(df, species)
        
        # Save results if output file specified
        if output_file:
            logger.info(f"Saving results to {output_file}")
            save_data(result_df, output_file)
            
        return result_df
    
    def process_dataframe(self, df, species):
        """Process a dataframe of SNPs.
        
        Args:
            df: DataFrame with SNP data
            species: Bacterial species name
            
        Returns:
            Processed DataFrame with additional columns and scores
        """
        # Add bacterial species if not present
        if 'Bacterial_Species' not in df.columns:
            df['Bacterial_Species'] = species
        else:
            df['Bacterial_Species'] = df['Bacterial_Species'].fillna(species)
            
        # Clean up species formatting
        df['Bacterial_Species'] = df['Bacterial_Species'].str.replace('_', ' ')
        
        # Step 2: Get taxonomy IDs
        logger.info("Fetching taxonomy IDs...")
        df['TAX_ID'] = df['Bacterial_Species'].apply(get_taxid)
        
        # Step 3-4: Extract and normalize depth
        logger.info("Processing read depth information...")
        df['Max_Depth'] = df['EVIDENCE'].apply(extract_depth)
        df['Depth'] = df['Max_Depth']
        df['Normalized_Depth'] = normalize_depth(df['Depth'])
        
        # Step 5-7: Process amino acid changes
        logger.info("Analyzing amino acid changes...")
        df['AA_Change'] = df['EFFECT'].apply(extract_aa_change)
        df['AA_Impact_Score'] = df.apply(compute_aa_impact, axis=1)
        
        # Step 8-9: Extract AA positions
        logger.info("Processing protein positions...")
        df['Total_AA'] = df['AA_POS'].apply(
            lambda x: int(str(x).split('/')[-1]) if '/' in str(x) else None
        )
        df['Mutated_AA'] = df['AA_POS'].apply(
            lambda x: int(str(x).split('/')[0]) if '/' in str(x) else None
        )
        
        # Step 10-11: UniProt and domain analysis
        logger.info("Searching UniProt database...")
        uniprot_ids = []
        for index, row in df.iterrows():
            gene = str(row['GENE']).split('_')[0]
            taxid = row['TAX_ID']
            length = row['Total_AA']
            if pd.notna(gene) and pd.notna(taxid) and pd.notna(length):
                uid = search_uniprot(gene, taxid, length, self.uniprot_tolerance)
            else:
                uid = None
            uniprot_ids.append(uid)
        df['UniProt_ID'] = uniprot_ids
        
        logger.info("Checking domain positions...")
        df['Domain_Position_Match'] = df.apply(
            lambda row: check_domain_position(row['UniProt_ID'], row['Mutated_AA']),
            axis=1
        )
        
        # Step 12: Calculate final priority score
        logger.info("Calculating final priority scores...")
        df['Final_Priority_Score'] = calculate_priority_score(df)
        
        # Add percentage score
        df['Final_Priority_Score_Percent'] = df['Final_Priority_Score'] * 100
        
        return df
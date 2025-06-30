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
from .processors.taxonomy import validate_specie_name, get_taxid
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
        
    def run(self, input_file, specie, output_file=None):
        """Run the SNP prioritization pipeline on an input file.
        
        Args:
            input_file: Path to input Excel file
            specie: Bacterial specie name
            output_file: Path to save output Excel file (optional)
            
        Returns:
            DataFrame with prioritized SNPs
            
        Raises:
            ValueError: If the specie name is invalid
        """
        logger.info("Loading input data...")
        try:
            df = load_data(input_file)
        except ValueError:
            # Just re-raise the error without additional logging
            raise
            
        # Validate specie name before processing
        if not validate_specie_name(specie):
            raise ValueError(
                f"Invalid specie name: '{specie}'. Please verify the specie name and try again."
            )
        
        # Process the dataframe
        result_df = self.process_dataframe(df, specie)
        
        # Save results if output file specified
        if output_file:
            logger.info(f"Saving results to {output_file}")
            save_data(result_df, output_file)
            
        return result_df
    
    def process_dataframe(self, df, specie, tax_id=None):
        """Process a dataframe of SNPs.
        
        Args:
            df: DataFrame with SNP data
            specie: Bacterial specie name
            tax_id: Optional pre-validated taxonomy ID
            
        Returns:
            Processed DataFrame with additional columns and scores
        """
        # Add bacterial specie if not present
        if 'Bacterial_Specie' not in df.columns:
            df['Bacterial_Specie'] = specie
        else:
            df['Bacterial_Specie'] = df['Bacterial_Specie'].fillna(specie)
            
        # Clean up specie formatting
        df['Bacterial_Specie'] = df['Bacterial_Specie'].str.replace('_', ' ')
        
        # Step 2: Fetching taxonomy ID (using pre-validated ID if available)
        logger.info("Fetching taxonomy ID...")
        df['Taxonomic_ID'] = tax_id if tax_id else df['Bacterial_Specie'].apply(get_taxid)
        
        # Step 3-4: Extract and normalize depth
        logger.info("Processing read depth information...")
        df['Depth'] = df['Evidence'].apply(extract_depth)
        #df['Depth'] = df['Max_Depth']
        df['Normalized_Depth'] = normalize_depth(df['Depth'])
        
        # Step 5-7: Process amino acid changes
        logger.info("Analyzing amino acid changes...")
        df['AA_Change'] = df['Effect'].apply(extract_aa_change)
        df['Amino_Acid_Impact_Score'] = df.apply(compute_aa_impact, axis=1)
        
        # Step 8-9: Extract AA positions
        logger.info("Processing protein positions...")
        df['Total_Protein_Length'] = df['Amino_Acid_Position'].apply(
            lambda x: int(str(x).split('/')[-1]) if '/' in str(x) else None
        )
        df['Mutated_AA'] = df['Amino_Acid_Position'].apply(
            lambda x: int(str(x).split('/')[0]) if '/' in str(x) else None
        )
        
        # Step 10-11: UniProt and domain analysis
        logger.info("Searching UniProt database...")
        uniprot_ids = []
        for index, row in df.iterrows():
            gene = str(row['Gene']).split('_')[0]
            taxid = row['Taxonomic_ID']
            length = row['Total_Protein_Length']
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
        df['Final_Priority_Score (%)'] = df['Final_Priority_Score'] * 100
        
        return df
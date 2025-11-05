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
from rich.console import Console
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
        self.console = Console()
    
    def print_status(self, message, style="green"):
        """Print status messages with Rich formatting."""
        self.console.print(f"[+] {message}", style=f"bold {style}")
        
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
        self.print_status("Loading input data...")
        try:
            df = load_data(input_file)
            self.print_status(f"Loaded {len(df)} SNPs from input file", "cyan")
        except ValueError:
            # Just re-raise the error without additional logging
            raise
            
        # Validate specie name before processing
        self.print_status("Validating species name...")
        if not validate_specie_name(specie):
            raise ValueError(
                f"Invalid specie name: '{specie}'. Please verify the specie name and try again."
            )
        self.print_status(f"Species validated: {specie}", "cyan")
        
        # Process the dataframe
        self.print_status("Processing SNP data...")
        result_df = self.process_dataframe(df, specie)
        
        # Save results if output file specified
        if output_file:
            import os
            # Create output directory based on output file name (without extension)
            base_name = os.path.splitext(os.path.basename(output_file))[0]
            parent_dir = os.path.dirname(output_file) or os.getcwd()
            output_dir = os.path.join(parent_dir, base_name)
            os.makedirs(output_dir, exist_ok=True)

            # Save output file inside this directory
            output_path = os.path.join(output_dir, os.path.basename(output_file))
            self.print_status(f"Saving results to {output_path}", "cyan")
            save_data(result_df, output_path)

            # Generate Plots for output data using plotting module
            try:
                from .plotting import plot_boxplot, plot_pie_chart, plot_histogram, plot_top_variants
                plots_dir = os.path.join(output_dir, "plots")
                os.makedirs(plots_dir, exist_ok=True)
                plot_boxplot(output_path, plots_dir)
                plot_pie_chart(output_path, plots_dir)
                plot_histogram(output_path, plots_dir)
                plot_top_variants(output_path, plots_dir, top_n=20)
                self.print_status(f"Plots generated in: {plots_dir}", "cyan")
            except Exception as pe:
                self.print_status(f"Plotting failed: {pe}", "red")

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
        self.print_status("Fetching taxonomy ID...", "cyan")
        df['Taxonomic_ID'] = tax_id if tax_id else df['Bacterial_Specie'].apply(get_taxid)
        
        # Step 3-4: Extract and normalize depth
        self.print_status("Processing read depth information...", "cyan")
        df['Depth'] = df['Evidence'].apply(extract_depth)
        #df['Depth'] = df['Max_Depth']
        df['Normalized_Depth'] = normalize_depth(df['Depth'])
        
        # Step 5-7: Process amino acid changes
        self.print_status("Analyzing amino acid changes...", "cyan")
        df['AA_Change'] = df['Effect'].apply(extract_aa_change)
        df['Amino_Acid_Impact_Score'] = df.apply(compute_aa_impact, axis=1)
        
        # Step 8-9: Extract AA positions
        self.print_status("Processing protein positions...", "cyan")
        df['Total_Protein_Length'] = df['Amino_Acid_Position'].apply(
            lambda x: int(str(x).split('/')[-1]) if '/' in str(x) else None
        )
        df['Mutated_AA'] = df['Amino_Acid_Position'].apply(
            lambda x: int(str(x).split('/')[0]) if '/' in str(x) else None
        )
        
        # Step 10-11: UniProt and domain analysis
        self.print_status("Searching UniProt database...", "cyan")
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
        
        self.print_status("Checking domain positions...", "cyan")
        df['Domain_Position_Match'] = df.apply(
            lambda row: check_domain_position(row['UniProt_ID'], row['Mutated_AA']),
            axis=1
        )
        
        # Step 12: Calculate final priority score
        self.print_status("Calculating final priority scores...", "cyan")
        df['Final_Priority_Score'] = calculate_priority_score(df)
        
        # Add percentage score
        df['Final_Priority_Score (%)'] = df['Final_Priority_Score'] * 100
        
        self.print_status("SNP analysis completed successfully!", "green")
        
        return df
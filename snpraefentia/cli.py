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
# PATENT NOTICE: This software uses patent-protected SNP scoring algorithms.
# See the LICENSE and NOTICE files for details.
"""Command-line interface for SNPraefentia.

This module provides the command-line interface for the SNPraefentia package,
allowing users to interact with the SNP analysis functionality through
command-line arguments and options.
"""

import argparse
import logging
import sys
import os
from . import __version__
from .core import SNPAnalyst

def setup_logging(log_file=None, verbose=False, quiet=False):
    """Configure logging based on command line arguments."""
    log_level = logging.INFO
    if verbose:
        log_level = logging.DEBUG
    elif quiet:
        log_level = logging.ERROR
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Add file handler if log file is specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        ))
        logging.getLogger().addHandler(file_handler)

def main():
    """Main entry point for the SNPraefentia command-line interface."""
    parser = argparse.ArgumentParser(
        description="SNPraefentia: SNP Prioritization Tool",
        epilog="For more information, visit: https://github.com/muneebdev7/SNPraefentia",
    )
    
    # Required arguments
    parser.add_argument("--input", "-i", required=True, 
                        help="Path to input file (supports .xlsx, .xls, .csv, .tsv, .txt)")
    parser.add_argument("--species", "-s", required=True,
                        help="Bacterial species name (e.g., 'Bacteroides uniformis')")
    
    # Output options
    parser.add_argument("--output", "-o", default=None,
                        help="Path to save output file (supports .xlsx, .xls, .csv, .tsv, .txt)")
    parser.add_argument("--format", "-f", choices=["excel", "csv", "tsv"], default=None,
                        help="Output format override (default: determined from output file extension)")
    
    # Processing options
    parser.add_argument("--uniprot-tolerance", "-ut", type=int, default=50,
                        help="Length tolerance when matching UniProt entries (default: 50)")
    
    # Logging and verbosity options
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Increase output verbosity")
    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Suppress all non-error output")
    parser.add_argument("--log-file", "-l",
                        help="Path to save log file")
    
    # Version and help
    parser.add_argument("--version", action="version",
                        version=f"SNPraefentia version {__version__}")
    
    args = parser.parse_args()
    
    # Check for conflicting arguments
    if args.verbose and args.quiet:
        parser.error("--verbose and --quiet cannot be used together")
    
    # Set default output file if not provided
    if not args.output:
        input_name = os.path.splitext(os.path.basename(args.input))[0]
        if args.format == "excel":
            args.output = f"{input_name}_results.xlsx"
        elif args.format == "csv":
            args.output = f"{input_name}_results.csv"
        elif args.format == "tsv":
            args.output = f"{input_name}_results.tsv"
        else:
            # Default to the same format as input if possible
            input_ext = os.path.splitext(args.input)[1].lower()
            if input_ext in ['.xlsx', '.xls']:
                args.output = f"{input_name}_results.xlsx"
            elif input_ext == '.csv':
                args.output = f"{input_name}_results.csv"
            elif input_ext in ['.tsv', '.txt']:
                args.output = f"{input_name}_results.tsv"
            else:
                args.output = f"{input_name}_results.csv"  # Default to CSV
    
    # Override output format if specified
    if args.format:
        output_path, _ = os.path.splitext(args.output)
        if args.format == "excel":
            args.output = f"{output_path}.xlsx"
        elif args.format == "csv":
            args.output = f"{output_path}.csv"
        elif args.format == "tsv":
            args.output = f"{output_path}.tsv"
    
    # Setup logging
    setup_logging(log_file=args.log_file, verbose=args.verbose, quiet=args.quiet)
    logger = logging.getLogger("snprior")
    
    try:
        # Run the main functionality
        logger.info(f"Starting SNPraefentia v{__version__}")
        logger.info(f"Processing input file: {args.input}")
        logger.info(f"Target species: {args.species}")
        logger.info(f"Output will be saved to: {args.output}")
        
        # Initialize the SNPanalyst class with command line arguments
        analyst = SNPAnalyst(
            uniprot_tolerance=args.uniprot_tolerance
        )
        
        # Run the pipeline
        results = analyst.run(
            input_file=args.input,
            species=args.species,
            output_file=args.output
        )
        
        logger.info(f"Results saved to: {args.output}")
        logger.info("SNPraefentia completed successfully")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=args.verbose)
        sys.exit(1)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
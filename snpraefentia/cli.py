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
from . import __version__, check_dependencies
from .core import SNPAnalyst

class SNPraefentiaCLI:
    def __init__(self):
        self.logger = None

    def setup_logging(self, log_file=None, verbose=False, quiet=False):
        """Configure logging based on command line arguments."""
        log_level = logging.INFO
        if verbose:
            log_level = logging.DEBUG
        elif quiet:
            log_level = logging.ERROR
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            ))
            logging.getLogger().addHandler(file_handler)
        self.logger = logging.getLogger("snprior")

    def parse_args(self):
        parser = argparse.ArgumentParser(
            description="SNPraefentia: SNP Prioritization Tool",
            epilog="For more information, visit: https://github.com/muneebdev7/SNPraefentia",
        )
        parser.add_argument("--input", "-i", required=True, 
                            help="Path to input file (supports .xlsx, .xls, .csv, .tsv, .txt)")
        parser.add_argument("--specie", "-s", required=True,
                            help="Bacterial specie name (e.g., 'Bacteroides uniformis')")
        parser.add_argument("--output", "-o", required=True,
                            help="Path to save output file (supports .xlsx, .xls, .csv, .tsv, .txt)")
        parser.add_argument("--format", "-f", choices=["excel", "csv", "tsv"], default=None,
                            help="Output format override (default: determined from output file extension)")
        parser.add_argument("--uniprot-tolerance", "-ut", type=int, default=50,
                            help="Length tolerance when matching UniProt entries (default: 50)")
        parser.add_argument("--verbose", "-v", action="store_true",
                            help="Increase output verbosity")
        parser.add_argument("--quiet", "-q", action="store_true",
                            help="Suppress all non-error output")
        parser.add_argument("--log-file", "-l",
                            help="Path to save log file")
        parser.add_argument("--version", action="version",
                            version=f"SNPraefentia version {__version__}")
        args = parser.parse_args()
        if args.verbose and args.quiet:
            parser.error("--verbose and --quiet cannot be used together")
        return args

    def ensure_output_extension(self, args):
        output_ext = os.path.splitext(args.output)[1].lower()
        if output_ext not in ['.xlsx', '.xls', '.csv', '.tsv', '.txt']:
            if args.format == "excel":
                args.output = f"{args.output}.xlsx"
            elif args.format == "csv":
                args.output = f"{args.output}.csv"
            elif args.format == "tsv":
                args.output = f"{args.output}.tsv"
            else:
                args.output = f"{args.output}.csv"
        return args

    def run(self):
        args = self.parse_args()
        args = self.ensure_output_extension(args)
        self.setup_logging(log_file=args.log_file, verbose=args.verbose, quiet=args.quiet)

        # Dependency check
        try:
            check_dependencies(raise_on_missing=True)
        except ImportError as e:
            self.logger.error(str(e))
            sys.exit(1)

        try:
            self.logger.info(f"Starting SNPraefentia v{__version__}")
            self.logger.info(f"Processing input file: {args.input}")
            self.logger.info(f"Target specie: {args.specie}")
            self.logger.info(f"Output will be saved to: {args.output}")
            analyst = SNPAnalyst(uniprot_tolerance=args.uniprot_tolerance)
            try:
                analyst.run(
                    input_file=args.input,
                    specie=args.specie,
                    output_file=args.output
                )
                self.logger.info(f"Results saved to: {args.output}")
                self.logger.info("SNPraefentia completed successfully")
            except ValueError as ve:
                self.logger.error(str(ve))
                sys.exit(1)
        except Exception as e:
            self.logger.error(f"Error: {str(e)}", exc_info=args.verbose)
            sys.exit(1)
        return 0

def main():
    cli = SNPraefentiaCLI()
    return cli.run()

if __name__ == "__main__":
    sys.exit(main())
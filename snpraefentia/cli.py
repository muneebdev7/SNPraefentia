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
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from . import __version__, check_dependencies
from .core import SNPAnalyst

class SNPraefentiaCLI:
    def __init__(self):
        self.logger = None
        self.console = Console()

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

    def print_banner(self):
        """Print the SNPraefentia banner with Rich formatting."""
        banner = r"""
 ____  _   _ ____                  __            _   _       
/ ___|| \ | |  _ \ _ __ __ _  ___ / _| ___ _ __ | |_(_) __ _ 
\___ \|  \| | |_) | '__/ _` |/ _ \ |_ / _ \ '_ \| __| |/ _` |
 ___) | |\  |  __/| | | (_| |  __/  _|  __/ | | | |_| | (_| |
|____/|_| \_|_|   |_|  \__,_|\___|_|  \___|_| |_|\__|_|\__,_|
                                                            
        """
        self.console.print(Text(banner, style="bold cyan"))
        self.console.print(Panel(Text("SNPraefentia CLI Agent", justify="right"), style="bold magenta", expand=False))

    def print_status(self, message, style="green"):
        """Print status messages with Rich formatting."""
        self.console.print(f"[+] {message}", style=f"bold {style}")

    def print_help_table(self):
        """Print help information in a tabular format using Rich."""
        table = Table(show_header=True, header_style="bold blue", box=box.ROUNDED, highlight=True)
        table.add_column("Options", style="bold cyan", width=30, min_width=25)
        table.add_column("Description", style="white", min_width=40)
        
        table.add_row("-h, --help", "Show this help message and exit")
        table.add_row("-i, --input", "Path to input file ('supports .xlsx, .xls, .csv, .tsv')")
        table.add_row("-s, --specie", "Bacterial specie name (e.g., 'Bacteroides uniformis')")
        table.add_row("-o, --output", "Path to save output file ('supports .xlsx, .xls, .csv, .tsv')")
        table.add_row("-f, --format", "Output format override ('excel/csv/tsv')")
        table.add_row("-ut, --uniprot-tolerance", "Length tolerance for UniProt entries (default: 50)")
        table.add_row("-v, --verbose", "Increase output verbosity")
        table.add_row("-q, --quiet", "Suppress all non-error output")
        table.add_row("-l, --log-file", "Path to save log file")
        table.add_row("--version", "Show package version")
        
        self.console.print(table)

    def parse_args(self):
        parser = argparse.ArgumentParser(
            description="SNPraefentia: SNP Prioritization Tool",
            epilog="For more information, visit: https://github.com/muneebdev7/SNPraefentia",
            add_help=False
        )
        parser.add_argument("-h", "--help", action="store_true", help="Show this help message and exit")
        parser.add_argument("--input", "-i", required=False, 
                            help="Path to input file (supports .xlsx, .xls, .csv, .tsv, .txt)")
        parser.add_argument("--specie", "-s", required=False,
                            help="Bacterial specie name (e.g., 'Bacteroides uniformis')")
        parser.add_argument("--output", "-o", required=False,
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
        parser.add_argument("--version", action="store_true",
                            help="Show package version")
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
        # Always show banner
        self.print_banner()
        
        args = self.parse_args()
        
        # Handle help or no arguments
        if args.help or len(sys.argv) == 1:
            self.print_help_table()
            self.console.print(Panel(Text("For more information, visit: https://github.com/muneebdev7/SNPraefentia", justify="center"), style="bold green", expand=False))
            return 0
        
        # Handle version
        if args.version:
            self.console.print(f"SNPraefentia version {__version__}", style="bold green")
            return 0
        
        # Validate required arguments
        if not (args.input and args.specie and args.output):
            self.console.print("Error: --input, --specie, and --output are required for analysis.", style="bold red")
            self.print_help_table()
            return 1
        
        args = self.ensure_output_extension(args)
        self.setup_logging(log_file=args.log_file, verbose=args.verbose, quiet=args.quiet)

        # Dependency check
        self.print_status("Checking dependencies...")
        try:
            check_dependencies(raise_on_missing=True)
            self.print_status("All dependencies found.")
        except ImportError as e:
            self.console.print(f"Dependency error: {str(e)}", style="bold red")
            return 1

        try:
            self.print_status(f"Starting SNPraefentia v{__version__}")
            self.print_status(f"Processing input file: {args.input}", "cyan")
            self.print_status(f"Target specie: {args.specie}", "cyan")
            self.print_status(f"Output will be saved to: {args.output}", "cyan")
            
            analyst = SNPAnalyst(uniprot_tolerance=args.uniprot_tolerance)
            
            try:
                analyst.run(
                    input_file=args.input,
                    specie=args.specie,
                    output_file=args.output
                )
                self.print_status(f"Results saved to: {args.output}")
                self.print_status("SNPraefentia completed successfully!", "green")
            except ValueError as ve:
                self.console.print(f"Error: {str(ve)}", style="bold red")
                return 1
        except Exception as e:
            self.console.print(f"Error: {str(e)}", style="bold red")
            return 1
        return 0

def main():
    cli = SNPraefentiaCLI()
    return cli.run()

if __name__ == "__main__":
    sys.exit(main())
# SNPraefentia: SNP Prioritization from Metagenomic Variants

SNPraefentia is a comprehensive tool for prioritizing Single Nucleotide Polymorphisms (SNPs) in metagenomic variants. It helps in identifying 
potentially significant variants by analyzing sequencing depth, amino acid changes, and protein domain information.

## Installation

SNPraefentia can be installed using pip:

```bash
# Install from PyPI
pip install snpraefentia
```

Or you can install from source:

```bash
# Clone the repository
git clone https://github.com/muneebdev7/SNPraefentia.git
cd SNPraefentia

# Install
pip install .

# Install in development mode (if you want to modify the code)
pip install -e .
```

### Dependencies

SNPraefentia requires the following Python packages, which will be automatically installed:

- pandas (≥1.0.0)
- numpy (≥1.18.0)
- requests (≥2.22.0)
- ete3 (≥3.1.1)
- openpyxl (≥3.1.5)

## First-time Setup

### NCBI Taxonomy Database

On first use, SNPraefentia needs to download the NCBI taxonomy database. This is a one-time process that requires approximately 600+ MB of disk space:

```bash
# This happens automatically on first use, but might take a few minutes
# You can also trigger it manually before running SNPraefentia:
python -c "from ete3 import NCBITaxa; ncbi = NCBITaxa()"
```

The database will be stored in `~/.etetoolkit/` by default.

### Verifying Installation

To verify that the package is installed correctly:

```bash
snpraefentia --version
```

This should display the current version (1.0.0).

## Usage

### Command Line Interface

#### Basic Usage

```bash
snpraefentia --input your_data.csv --specie "Bacteroides uniformis" --output results.csv
```

#### Required Arguments

- `--input`, `-i`: Path to input CSV file containing SNP data
- `--specie`, `-s`: Bacterial species name (e.g., 'Bacteroides uniformis')
- `--output`, `-o`: Path to save output CSV file

#### Optional Arguments

- `--format`, `-f`: Output format override (determined from output file extension)
- `--uniprot-tolerance`, `-ut`: Length tolerance when matching UniProt entries (default: 50)

#### Logging Options

- `--verbose`, `-v`: Increase output verbosity (shows DEBUG messages)
- `--quiet`, `-q`: Suppress all non-error output
- `--log-file`, `-l`: Path to save log file

#### Help and Version

- `--help`, `-h`: Show help message and exit
- `--version`: Show version and exit

### Python API

You can also use SNPraefentia programmatically in your Python scripts:

```python
from snpraefentia.core import SNPAnalyst

# Initialize with default settings
analyst = SNPAnalyst()

# Process an input file
results = analyst.run(
    input_file="path/to/input.csv",
    species="Bacteroides uniformis",
    output_file="path/to/output.csv"  # Optional, omit to skip saving
)

# Or process an existing DataFrame
import pandas as pd
df = pd.read_csv("my_snps.csv")
processed_df = analyst.process_dataframe(df, "Bacteroides uniformis")

# Save results manually if needed
processed_df.to_csv("custom_output.csv", index=False)
```

## Input Format

SNPraefentia expects a CSV file (`.csv`) with the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| `EVIDENCE` | Read depth information | `A:10 C:5` |
| `EFFECT` | Variant effect prediction | `p.Ala123Gly` |
| `GENE` | Gene name | `geneA` |
| `AA_POS` | Amino acid position information | `123/500` |

Additional columns are allowed and will be preserved in the output.

## Output Format

SNPraefentia adds the following columns to the input data:

| Column | Description |
|--------|-------------|
| `Bacterial_Species` | Species name |
| `TAX_ID` | NCBI taxonomy ID |
| `Max_Depth` | Maximum read depth extracted from EVIDENCE |
| `Depth` | Adjusted depth value |
| `Normalized_Depth` | Depth normalized to range [0,1] |
| `AA_Change` | Extracted amino acid change (e.g., "AlaGly") |
| `AA_Impact_Score` | Score based on physicochemical property changes |
| `Total_AA` | Total protein length |
| `Mutated_AA` | Position of the mutated amino acid |
| `UniProt_ID` | UniProt identifier if found |
| `Domain_Position_Match` | Whether mutation is in a protein domain (1=yes, 0=no) |
| `Final_Priority_Score` | Combined priority score (0-1) |
| `Final_Priority_Score_Percent` | Priority score as percentage (0-100%) |

## Configuration

### Weighting Parameters

SNPraefentia uses a weighted scoring system. You can adjust these weights to customize the prioritization:

- `depth_weight`: Importance of sequencing depth (default: 2.0)
- `aa_weight`: Importance of amino acid changes (default: 1.0)
- `domain_weight`: Importance of domain position (default: 1.0)

Higher weights increase the influence of that factor on the final score. The final score is calculated as:

```math
(depth_weight * Normalized_Depth + aa_weight * AA_Impact_Score + domain_weight * Domain_Position_Match) / Total Score
```

### UniProt Parameters

- `uniprot_tolerance`: When matching genes to UniProt entries, this parameter controls how close the protein length must be to the expected length (default: 50 amino acids)

### Logging Options

SNPraefentia provides three verbosity levels:

- **Normal** (default): Shows INFO level messages (major processing steps)
- **Verbose** (`--verbose`): Shows DEBUG level messages (detailed information)
- **Quiet** (`--quiet`): Shows only ERROR level messages (problems only)

You can also save logs to a file with `--log-file path/to/logfile.log`.

## Examples

### Detailed Logging

```bash
snpraefentia --input snps.csv --specie "Klebsiella pneumoniae" --output results.csv --verbose --log-file snpraefentia_run.log
```

## Running Tests

This package uses Python's built-in unittest framework for testing all functions in the package.

To run all tests:

```bash
python -m unittest discover -s snpraefentia/tests
```

## Troubleshooting

### Common Issues

#### Missing NCBI Taxonomy Database

```
Error: NCBITaxa not initialized
```

Solution: Run the following command to download the database:
```bash
python -c "from ete3 import NCBITaxa; ncbi = NCBITaxa()"
```

#### Species Not Found

```
Warning: No taxonomy ID found for [species]
```

Solution: Check the spelling of your species name. Use the scientific name (genus and species).

## License

SNPraefentia is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

### Patent Notice

The SNP scoring algorithms and methodologies implemented in this software are protected by patent rights owned by the SNPraefentia Authors. While the source code is available under the Apache License 2.0, usage of the scoring algorithms may require a separate patent license, particularly for commercial applications.

For patent licensing inquiries, please contact the authors.

See the [NOTICE](NOTICE) file for additional details regarding copyright and patent notices.

## Citation

If you use SNPraefentia in your research, please cite:

```
Khan, N., & Nasir, M. M. (2025). SNPraefentia: A Comprehensive Tool for SNP Prioritization in Bacterial Genomes. 
GitHub repository: https://github.com/muneebdev7/SNPraefentia
Version 1.0.0
```

For questions, feature requests, or bug reports, please open an issue on GitHub.
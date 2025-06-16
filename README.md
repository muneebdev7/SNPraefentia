# SNAP: SNP Prioritization Tool

SNAP (SNP Prioritization) is a comprehensive tool for prioritizing Single Nucleotide Polymorphisms (SNPs) in bacterial genomes. It helps researchers identify potentially significant variants by analyzing sequencing depth, amino acid changes, and protein domain information.

## Installation

SNAP can be installed using pip:

```bash
# Install from PyPI
pip install snap
```

Or you can install from source:

```bash
# Clone the repository
git clone https://github.com/muneebdev7/SNAP.git
cd snap

# Install
pip install .

# Install in development mode (if you want to modify the code)
pip install -e .
```

### Dependencies

SNAP requires the following Python packages, which will be automatically installed:
- pandas (≥1.0.0)
- numpy (≥1.18.0)
- requests (≥2.22.0)
- ete3 (≥3.1.1)
- openpyxl (≥3.1.5)

## First-time Setup

### NCBI Taxonomy Database

On first use, SNAP needs to download the NCBI taxonomy database. This is a one-time process that requires approximately 600+ MB of disk space:

```bash
# This happens automatically on first use, but might take a few minutes
# You can also trigger it manually before running SNAP:
python -c "from ete3 import NCBITaxa; ncbi = NCBITaxa()"
```

The database will be stored in `~/.etetoolkit/` by default.

### Verifying Installation

To verify that SNAP is installed correctly:

```bash
snap --version
```

This should display the current version of SNAP.

## Usage

### Command Line Interface

#### Basic Usage

```bash
snap --input your_data.xlsx --species "Bacteroides uniformis" --output results.xlsx
```

#### Required Arguments

- `--input`, `-i`: Path to input Excel file containing SNP data
- `--species`, `-s`: Bacterial species name (e.g., 'Bacteroides uniformis')

#### Optional Arguments

- `--output`, `-o`: Path to save output Excel file (default: "snap_results.xlsx")

#### Processing Options

- `--uniprot-tolerance`, `-ut`: Length tolerance when matching UniProt entries (default: 50)
- `--depth-weight`, `-dw`: Weight for normalized depth in priority score (default: 2.0)
- `--aa-weight`, `-aw`: Weight for amino acid impact in priority score (default: 1.0)
- `--domain-weight`, `-dow`: Weight for domain position in priority score (default: 1.0)

#### Logging Options

- `--verbose`, `-v`: Increase output verbosity (shows DEBUG messages)
- `--quiet`, `-q`: Suppress all non-error output
- `--log-file`, `-l`: Path to save log file

#### Help and Version

- `--help`, `-h`: Show help message and exit
- `--version`: Show version and exit

### Python API

You can also use SNAP programmatically in your Python scripts:

```python
from snap.core import SNPPrioritizer

# Initialize with default settings
prioritizer = SNPPrioritizer()

# Or customize parameters
prioritizer = SNPPrioritizer(
    uniprot_tolerance=75,  # Adjust tolerance for UniProt matches
    depth_weight=3.0,      # Give more weight to sequencing depth
    aa_weight=2.0,         # Increase importance of amino acid changes
    domain_weight=1.5      # Adjust domain position importance
)

# Process an input file
results = prioritizer.run(
    input_file="path/to/input.xlsx",
    species="Bacteroides uniformis",
    output_file="path/to/output.xlsx"  # Optional, omit to skip saving
)

# Or process an existing DataFrame
import pandas as pd
df = pd.read_excel("my_snps.xlsx")
processed_df = prioritizer.process_dataframe(df, "Bacteroides uniformis")

# Save results manually if needed
processed_df.to_excel("custom_output.xlsx", index=False)
```

## Input Format

SNAP expects an Excel file (`.xlsx`) with the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| `EVIDENCE` | Read depth information | `A:10 C:5` |
| `EFFECT` | Variant effect prediction | `p.Ala123Gly` |
| `GENE` | Gene name | `geneA` |
| `AA_POS` | Amino acid position information | `123/500` |

Additional columns are allowed and will be preserved in the output.

## Output Format

SNAP adds the following columns to the input data:

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

SNAP uses a weighted scoring system. You can adjust these weights to customize the prioritization:

- `depth_weight`: Importance of sequencing depth (default: 2.0)
- `aa_weight`: Importance of amino acid changes (default: 1.0)
- `domain_weight`: Importance of domain position (default: 1.0)

Higher weights increase the influence of that factor on the final score. The final score is calculated as:

```
(depth_weight * Normalized_Depth + aa_weight * AA_Impact_Score + domain_weight * Domain_Position_Match) / Total Score
```

### UniProt Parameters

- `uniprot_tolerance`: When matching genes to UniProt entries, this parameter controls how close the protein length must be to the expected length (default: 50 amino acids)

### Logging Options

SNAP provides three verbosity levels:

- **Normal** (default): Shows INFO level messages (major processing steps)
- **Verbose** (`--verbose`): Shows DEBUG level messages (detailed information)
- **Quiet** (`--quiet`): Shows only ERROR level messages (problems only)

You can also save logs to a file with `--log-file path/to/logfile.log`.

## Scoring Methodology

### Depth Score

Read depth is normalized to [0,1] across all SNPs in the dataset:
- Higher depth = higher confidence = higher score

### Amino Acid Impact Score

Based on physicochemical properties:
- Weight difference (normalized by 130)
- Hydrophobicity difference (normalized by 9)
- Polarity change (0 or 1)
- Charge change (0 or 1)

These factors are summed to produce a score between 0 and ~3.

### Domain Position Score

Binary score (0 or 1):
- 1 if mutation occurs in a functional protein domain
- 0 otherwise

## Examples

### Basic SNP Prioritization

```bash
snap --input snps.xlsx --species "Escherichia coli" --output prioritized_snps.xlsx
```

### Emphasize Sequencing Depth

```bash
snap --input snps.xlsx --species "Salmonella enterica" --depth-weight 4.0 --output depth_prioritized.xlsx
```

### Emphasize Amino Acid Changes

```bash
snap --input snps.xlsx --species "Staphylococcus aureus" --aa-weight 3.0 --output aa_prioritized.xlsx
```

### Emphasize Domain Positions

```bash
snap --input snps.xlsx --species "Pseudomonas aeruginosa" --domain-weight 3.0 --output domain_prioritized.xlsx
```

### Detailed Logging

```bash
snap --input snps.xlsx --species "Klebsiella pneumoniae" --verbose --log-file snap_run.log
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

#### UniProt Connection Issues

```
Warning: Error searching UniProt: Connection error
```

Solution: Check your internet connection. UniProt lookups require internet access.

#### Species Not Found

```
Warning: No taxonomy ID found for [species]
```

Solution: Check the spelling of your species name. Use the scientific name (genus and species).

#### Input File Format Issues

```
Error: Could not load data: [error message]
```

Solution: Ensure your input file is a valid Excel file (.xlsx) with the required columns.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Citation

If you use SNAP in your research, please cite:

```
Nadeem, Muneeb. (2025). SNAP: SNP Prioritization Tool. GitHub repository. https://github.com/muneebdev7/SNAP
```

For questions, feature requests, or bug reports, please open an issue on GitHub.
# Bioinformatics Toolkit

> A comprehensive collection of command-line bioinformatics tools for sequence analysis, BLAST processing, protein domain analysis, genome assembly QC, and data visualization.

[![License](https://img.shields.io/github/license/olympus-terminal/bioinformatics-toolkit)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/olympus-terminal/bioinformatics-toolkit?style=social)](https://github.com/olympus-terminal/bioinformatics-toolkit/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/olympus-terminal/bioinformatics-toolkit)](https://github.com/olympus-terminal/bioinformatics-toolkit/issues)
[![GitHub last commit](https://img.shields.io/github/last-commit/olympus-terminal/bioinformatics-toolkit)](https://github.com/olympus-terminal/bioinformatics-toolkit/commits/main)
[![Tools](https://img.shields.io/badge/tools-51-green.svg)](https://github.com/olympus-terminal/bioinformatics-toolkit)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/olympus-terminal/bioinformatics-toolkit)

## 🧬 Overview

This repository consolidates essential bioinformatics utilities designed for researchers and bioinformaticians working with genomic and proteomic data. The toolkit covers the entire workflow from raw sequence processing to visualization, with special support for high-performance computing (HPC) environments.

### Key Features

- **Sequence Manipulation**: FASTA/FASTQ processing, header modification, length filtering
- **BLAST Suite**: Result parsing, hit filtering, taxonomic analysis
- **Domain Analysis**: PFAM/HMM processing, motif discovery with ML
- **Assembly QC**: N50 calculation, k-mer analysis, contamination detection
- **Visualization**: Circos plots, UMAP projections, custom graphics
- **HPC Integration**: SLURM job scripts for cluster computing

## 📁 Repository Structure

```
bioinformatics-toolkit/
├── sequence-analysis/      # FASTA/Q manipulation, format conversion
├── blast-tools/           # BLAST processing and analysis
├── domain-analysis/       # Protein domain and motif tools
├── assembly-tools/        # Genome assembly statistics
├── visualization/         # Data visualization scripts
├── hpc-scripts/          # SLURM batch job scripts
└── utils/                # General bioinformatics utilities
```

## 🚀 Quick Start

### Prerequisites

```bash
# Core requirements
python >= 3.7
perl >= 5.10
bash >= 4.0

# Bioinformatics software
blast+ >= 2.10.0
hmmer >= 3.3
diamond >= 2.0.0
circos >= 0.69

# Python packages
pip install biopython pandas numpy matplotlib umap-learn
```

### Installation

```bash
# Clone the repository
git clone https://github.com/olympus-terminal/bioinformatics-toolkit.git
cd bioinformatics-toolkit

# Make scripts executable
find . -name "*.sh" -o -name "*.py" -o -name "*.pl" | xargs chmod +x

# Add to PATH (optional)
export PATH="$PATH:$(pwd)"
```

## 🔧 Tool Categories

### Sequence Analysis (`sequence-analysis/`)

| Tool | Description | Usage |
|------|-------------|-------|
| `filter_fasta_on_length` | Filter sequences by length | `./filter_fasta_on_length input.fa 1000 > filtered.fa` |
| `rename-fasta-headers-simple.sh` | Batch rename FASTA headers | `./rename-fasta-headers-simple.sh sequences.fa prefix` |
| `interleave.sh` | Interleave paired-end reads | `./interleave.sh read1.fq read2.fq > interleaved.fq` |
| `remove_line_wraps_fa.py` | Convert multi-line to single-line FASTA | `python remove_line_wraps_fa.py wrapped.fa > unwrapped.fa` |
| `csv2fa.py` | Convert CSV to FASTA format | `python csv2fa.py data.csv > sequences.fa` |
| `count-amino-acid-residues` | Count AA composition | `./count-amino-acid-residues proteins.fa` |

### BLAST Tools (`blast-tools/`)

| Tool | Description | Usage |
|------|-------------|-------|
| `ExtractSeqFromBLASTresults.sh` | Extract sequences from BLAST hits | `./ExtractSeqFromBLASTresults.sh blast.out seqs.fa` |
| `TakeOnlyBestBLASThit.sh` | Filter best hits only | `./TakeOnlyBestBLASThit.sh results.blast6` |
| `tally_blastp_by_genera.sh` | Summarize by taxonomic genera | `./tally_blastp_by_genera.sh blastp.out` |
| `make_taxid_diamond-blastdb` | Create DIAMOND DB with taxonomy | `./make_taxid_diamond-blastdb proteins.fa taxdb` |

### Domain Analysis (`domain-analysis/`)

| Tool | Description | Usage |
|------|-------------|-------|
| `extractPFAMs.sh` | Extract PFAM domains | `./extractPFAMs.sh hmmscan.out` |
| `Find-ECs-from-PFAMs.sh` | Map EC numbers from domains | `./Find-ECs-from-PFAMs.sh pfam_results.txt` |
| `LAAASR_motifMinerPro.py` | ML-based motif discovery | `python LAAASR_motifMinerPro.py -i seqs.fa -m model/` |
| `pivot_table_pfams` | Create PFAM pivot tables | `./pivot_table_pfams domain_counts.txt` |

### Assembly Tools (`assembly-tools/`)

| Tool | Description | Usage |
|------|-------------|-------|
| `n50calc.py` | Calculate assembly statistics | `python n50calc.py contigs.fa` |
| `cid_make_unitigs` | Process unitigs/contigs | `./cid_make_unitigs assembly.fa` |

### Visualization (`visualization/`)

| Tool | Description | Usage |
|------|-------------|-------|
| `circos-make.py` | Generate Circos configuration | `python circos-make.py -i data.txt -o circos.conf` |
| `run_pycirclize_v8.py` | Create circular plots | `python run_pycirclize_v8.py -i matrix.csv -o plot.png` |
| `UMAP-matrix-1.py` | UMAP dimensionality reduction | `python UMAP-matrix-1.py expression.csv` |

### HPC Scripts (`hpc-scripts/`)

Pre-configured SLURM job scripts for common bioinformatics tasks:

- `BLEACH_3long.sbatch` - Long-read contamination screening
- `meryl_merqury_long-reads-k-mers-hapQC.sbatch` - K-mer based QC
- `gmap.sbatch` - GMAP alignment pipeline
- `COUNT_AA.sbatch` - Parallel amino acid counting

## 📊 Example Workflows

### 1. Genome Assembly QC Pipeline

```bash
# Calculate assembly statistics
python assembly-tools/n50calc.py genome.fa > stats.txt

# Check for contamination
sbatch hpc-scripts/QuickCheckContam.sbatch genome.fa

# Analyze k-mer distribution
sbatch hpc-scripts/meryl_merqury_long-reads-k-mers-hapQC.sbatch reads.fq genome.fa
```

### 2. Protein Domain Analysis

```bash
# Run PFAM scan (using HMMER)
hmmscan --tblout domains.tbl Pfam-A.hmm proteins.fa

# Extract and format results
./domain-analysis/extractPFAMs.sh domains.tbl > pfam_hits.txt
./domain-analysis/format_pfams.sh pfam_hits.txt > formatted.txt

# Find enzyme classifications
./domain-analysis/Find-ECs-from-PFAMs.sh formatted.txt > ec_numbers.txt
```

### 3. BLAST Analysis Pipeline

```bash
# Run BLASTP
blastp -query proteins.fa -db nr -out blast.out -outfmt 6 -num_threads 8

# Filter best hits
./blast-tools/TakeOnlyBestBLASThit.sh blast.out > best_hits.txt

# Summarize by genera
./blast-tools/tally_blastp_by_genera.sh best_hits.txt > genera_summary.txt
```

## 🔍 Advanced Features

### Machine Learning Motif Discovery

The `LAAASR_motifMinerPro.py` tool uses GPTNeoX models for advanced motif discovery:

```bash
python domain-analysis/LAAASR_motifMinerPro.py \
    -i sequences.fa \
    -m gpt-neox-model/ \
    -o motifs_discovered.txt \
    --min-support 0.1
```

### Contamination Detection

The BLEACH pipeline identifies potential contamination in sequencing data:

```bash
# For long reads
sbatch hpc-scripts/BLEACH_3long.sbatch sample.fastq reference.fa

# For short reads (5x5 layout)
sbatch hpc-scripts/BLEACH_5x5L.sbatch sample_R1.fq sample_R2.fq
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-tool`)
3. Commit your changes (`git commit -am 'Add new tool'`)
4. Push to the branch (`git push origin feature/new-tool`)
5. Create a Pull Request

### Contribution Guidelines

- Include usage documentation for new tools
- Add example commands in tool headers
- Follow existing naming conventions
- Test on Linux and macOS when possible

## 📚 Citations

If you use these tools in your research, please cite:

```
@software{bioinformatics_toolkit,
  author = {olympus-terminal},
  title = {Bioinformatics Toolkit},
  url = {https://github.com/olympus-terminal/bioinformatics-toolkit},
  year = {2024}
}
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 External Resources

- [BLAST+ Documentation](https://www.ncbi.nlm.nih.gov/books/NBK279690/)
- [HMMER User Guide](http://hmmer.org/documentation.html)
- [Circos Tutorials](http://circos.ca/documentation/tutorials/)
- [BioPython Tutorial](https://biopython.org/wiki/Documentation)

## 💡 Tips & Tricks

- Many scripts support parallel processing - check for `-threads` or `-j` options
- Use SLURM scripts as templates for your own HPC workflows
- Combine tools with Unix pipes for complex analyses
- Check script headers for detailed usage examples

## 🐛 Troubleshooting

Common issues and solutions:

1. **Permission denied**: Run `chmod +x script_name.sh`
2. **Module not found**: Install Python dependencies with pip
3. **SLURM errors**: Check partition names and resource requirements
4. **Memory issues**: Use HPC scripts for large datasets

## 📮 Contact

For questions, issues, or collaborations:
- GitHub Issues: [Create an issue](https://github.com/olympus-terminal/bioinformatics-toolkit/issues)
- GitHub: [@olympus-terminal](https://github.com/olympus-terminal)

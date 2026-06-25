<p align="center">
  <img src="assets/banner.png" alt="bioinformatics-toolkit banner" width="100%">
</p>

# Bioinformatics Toolkit

Command-line tools for genomics and proteomics analysis — BLAST workflows, sequence manipulation, domain annotation, genome assembly QC, and visualization.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Tool Categories

| Category | Tools | Description |
|---|---|---|
| **BLAST** | `ExtractSeqFromBLASTresults.sh`, `TakeOnlyBestBLASThit.sh`, `estimate_BLASTP_FLOPs.py` | Result extraction, filtering, and benchmarking |
| **Sequence Analysis** | `csv2fa.py`, `split_fasta.sh`, `filter_fasta_on_length/`, `TrimSeqStart.sh`, `rename-fasta-headers-simple.sh`, `breakIn100s.py` | FASTA manipulation, filtering, and format conversion |
| **Domain & Annotation** | `extractPFAMs.sh`, `extractCDSfromPfam/`, `Find-ECs-from-PFAMs.sh`, `format.hmmsearchresults/`, `GoGetter.py` | PFAM extraction, EC number mapping, GO term retrieval |
| **Assembly** | `assembly-tools/`, `meryl_merqury_long-reads-k-mers-hapQC.sbatch`, `n50calc.py` | Genome assembly QC and k-mer analysis |
| **Protein Interactions** | `cry2h_PPI_calc.sh`, `sum_PPIs.awk`, `targeted_insilico_editing/` | PPI scoring and in silico editing |
| **Visualization** | `visualization/`, `run_pycirclize_v8.py`, `circos-make.py`, `UMAP-matrix-1.py` | Circos plots, UMAP projections, publication figures |
| **HPC** | `hpc-scripts/`, `BLEACH_*.sbatch`, `COUNT_AA.sbatch`, `gmap.sbatch` | SLURM job scripts for cluster execution |
| **Citation** | `CountCitations.py`, `fetch_pubmed_fulltext.py` | PubMed full-text retrieval and citation counting |
| **Utilities** | `utils/`, `header_extract.sh`, `tally-awk/`, `conda-data-fetcher-envMaker.sh` | General-purpose helpers |

## Quick Start

```bash
git clone https://github.com/olympus-terminal/bioinformatics-toolkit.git
cd bioinformatics-toolkit
```

Most scripts are standalone and take input via command-line arguments. See individual script headers for usage.

## License

MIT License - see [LICENSE](LICENSE) for details.

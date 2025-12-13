# Citation Tools

Automated RIS citation fetching from multiple academic databases. Fetches citation metadata in RIS format for direct import into reference managers (EndNote, Zotero, Mendeley).

## Tools

| Script | Description |
|--------|-------------|
| `ris_fetcher_20251022.py` | Core RIS fetcher (PubMed PMID, CrossRef DOI) |
| `ris_fetcher_expanded.py` | Extended fetcher with additional sources |
| `search_refs_template.py` | Template for searching papers via CrossRef API |
| `fetch_refs_template.py` | Template for batch fetching RIS citations |

## Supported Sources

### Core Fetcher (`ris_fetcher_20251022.py`)
- **PubMed** - via NCBI E-utilities (PMID)
- **CrossRef** - DOI resolution with content negotiation

### Expanded Fetcher (`ris_fetcher_expanded.py`)
- **PubMed** - PMID
- **CrossRef** - DOI
- **arXiv** - Preprints (arXiv ID)
- **bioRxiv/medRxiv** - Preprints (DOI)
- **Zenodo** - Datasets via DataCite
- **DataCite** - Generic dataset DOIs
- **NOAA** - Environmental datasets
- **NASA NTRS** - Technical reports

## Usage

### Basic Usage

```bash
# Fetch from a list of identifiers
python ris_fetcher_20251022.py citations.txt

# Using the expanded fetcher
python ris_fetcher_expanded.py citations.txt
```

### Input File Format

```
# Comments start with #
PMID:12345678
DOI:10.1234/example.doi
ARXIV:2311.17179
BIORXIV:10.1101/2023.01.01.123456
ZENODO:10.5281/zenodo.1234567
NASA:20150000001
```

### Output

- Individual `.ris` files for each citation
- Combined `bibliography_combined.ris` for bulk import
- Output directory can be customized via constructor

### Programmatic Usage

```python
from ris_fetcher_20251022 import RISFetcher

# Create fetcher with custom output directory
fetcher = RISFetcher(output_dir="my_citations")

# Process batch file
fetcher.process_batch("references.txt")

# Or fetch individual citations
filename, ris_content = fetcher.fetch_citation("DOI:10.1038/nature12373")
```

## Workflow Example

### 1. Search for papers by author/title/year

Create a search script based on `search_refs_template.py`:

```python
papers = [
    ("Smith 2024 protein folding machine learning", "Smith et al. 2024 - ML protein folding"),
    ("Jones 2023 CRISPR gene editing review", "Jones et al. 2023 - CRISPR review"),
]
```

### 2. Run the search to find DOIs

```bash
python search_refs_template.py
# Outputs: refs_dois.txt
```

### 3. Fetch RIS citations

```bash
python ris_fetcher_20251022.py refs_dois.txt
# Outputs: ris_citations/bibliography_combined.ris
```

### 4. Import into reference manager

Import `bibliography_combined.ris` into EndNote, Zotero, or Mendeley.

## Claude Code Integration

A Claude Code slash command is available in `.claude/commands/fetch-ris.md`. This automates the entire workflow:

1. Reads notes files to extract paper references
2. Searches CrossRef for DOIs
3. Fetches RIS citations
4. Produces combined bibliography

Usage in Claude Code:
```
/fetch-ris
```

## API Rate Limiting

The tools include built-in rate limiting (0.5s between requests) to be respectful of public APIs. For large batches, consider:

- Running overnight for 100+ citations
- Using institutional API keys if available
- Splitting into smaller batches

## Requirements

```bash
pip install requests
```

## License

MIT License - See repository LICENSE file.

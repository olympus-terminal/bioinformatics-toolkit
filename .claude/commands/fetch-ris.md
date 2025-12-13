# Fetch RIS Citations

Automatically extract paper references from the latest refs notes file and fetch RIS citations.

## Your Task

When this command is invoked, execute this pipeline:

### Step 1: Find the latest refs file
Find the latest `refs_X.txt` file (highest alphabetical letter, excluding `_dois.txt` files).
```bash
ls -la refs_*.txt | grep -v _dois
```

### Step 2: Read and analyze the notes
Read the latest refs file and carefully extract ALL paper references mentioned. For each paper, identify:
- First author surname
- Publication year
- Key title words (enough to uniquely identify the paper)
- Journal name if mentioned

Papers may be referenced in various formats:
- Prose: "Farrell et al. (2025) examined bacterial growth temperature..."
- Structured: "Alam, S. T., et al. 2025. Universal orthologs infer deep phylogenies. NAR."
- Descriptive: "A 2024 Nature Biotechnology paper by Nevers et al. on OMArk..."

### Step 3: Compile the search list
Create a Python script that searches CrossRef for each paper. Use `search_refs_D.py` as a template.

The papers list should contain tuples of (search_query, label):
```python
papers = [
    ("Farrell 2024 bacterial growth temperature horizontally acquired", "Farrell et al. 2024 - Bacterial thermal phenotype"),
    ("Nevers 2024 OMArk quality assessment Nature Biotechnology", "Nevers et al. 2024 - OMArk"),
    # ... all extracted papers
]
```

### Step 4: Search for DOIs
Run the search script to find DOIs via CrossRef API. Save results to `refs_X_dois.txt`.

### Step 5: Fetch RIS citations
Use `ris_fetcher_20251022.py` to fetch RIS files from the DOIs:
```bash
python3 ris_fetcher_20251022.py refs_X_dois.txt
```
Or create a fetch script that specifies the output directory:
```python
from ris_fetcher_20251022 import RISFetcher
fetcher = RISFetcher(output_dir="ris_citations_X")
fetcher.process_batch("refs_X_dois.txt")
```

### Step 6: Report results
Summarize:
- How many papers were identified in the notes
- How many DOIs were found
- How many RIS files were successfully fetched
- Location of the combined bibliography file

## Key Files
- `ris_fetcher_20251022.py` - Core RIS fetcher (DOIs via CrossRef, PMIDs via PubMed)
- `search_refs_*.py` - Example search scripts for reference
- `fetch_refs_*.py` - Example fetch scripts for reference

## Output
- `refs_X_dois.txt` - Found DOIs with comments
- `ris_citations_X/` - Individual RIS files
- `ris_citations_X/bibliography_combined.ris` - Combined file for Endnote/Zotero import

$ARGUMENTS

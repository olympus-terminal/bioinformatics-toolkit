#!/usr/bin/env python3
"""
Fetch RIS citations for a batch of DOIs/PMIDs

Template Usage:
    1. Edit the input_file and output_dir variables below
    2. Run: python fetch_refs_template.py
    3. Import bibliography_combined.ris into your reference manager
"""

import sys
sys.path.insert(0, '.')
from ris_fetcher_20251022 import RISFetcher

if __name__ == "__main__":
    # ==========================================================================
    # EDIT THESE VARIABLES
    # ==========================================================================
    input_file = "refs_dois.txt"      # File with DOIs/PMIDs (one per line)
    output_dir = "ris_citations"       # Directory for output .ris files
    # ==========================================================================

    fetcher = RISFetcher(output_dir=output_dir)
    fetcher.process_batch(input_file)

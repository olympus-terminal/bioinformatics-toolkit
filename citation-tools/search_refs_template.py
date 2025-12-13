#!/usr/bin/env python3
"""
Search for papers via CrossRef API and find their DOIs

Template Usage:
    1. Edit the 'papers' list with your search queries
    2. Run: python search_refs_template.py
    3. Output: refs_dois.txt with found DOIs

Search Query Tips:
    - Include author surname, year, and key title words
    - More specific queries yield better results
    - Format: "AuthorName Year keyword1 keyword2 keyword3"
"""

import requests
import time
from typing import Optional

class PaperSearcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Paper Searcher/1.0'
        })

    def search_crossref(self, query: str) -> Optional[str]:
        """Search CrossRef for a paper and return DOI"""
        url = "https://api.crossref.org/works"
        params = {
            'query': query,
            'rows': 1
        }

        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if data['message']['items']:
                item = data['message']['items'][0]
                doi = item.get('DOI')
                title = item.get('title', [''])[0]
                authors = item.get('author', [])
                author_names = ', '.join([f"{a.get('family', '')} {a.get('given', '')}" for a in authors[:3]])
                year = item.get('published', {}).get('date-parts', [[None]])[0][0]

                print(f"  Found: {author_names} ({year})")
                print(f"  Title: {title[:80]}")
                print(f"  DOI: {doi}")

                return doi
            else:
                print(f"  No results found")
                return None

        except Exception as e:
            print(f"  Error: {e}")
            return None

def main():
    # ==========================================================================
    # EDIT THIS LIST WITH YOUR PAPERS
    # Format: (search_query, label_for_output)
    # ==========================================================================
    papers = [
        # Example entries - replace with your own
        ("Smith 2024 protein folding machine learning nature", "Smith et al. 2024 - ML protein folding"),
        ("Jones 2023 CRISPR gene editing review cell", "Jones et al. 2023 - CRISPR review"),
        ("Brown 2022 single cell RNA sequencing cancer", "Brown et al. 2022 - scRNA-seq cancer"),
    ]
    # ==========================================================================

    searcher = PaperSearcher()
    results = []

    print("=" * 80)
    print("SEARCHING FOR PAPERS VIA CROSSREF")
    print("=" * 80)

    for i, (query, label) in enumerate(papers, 1):
        print(f"\n[{i}/{len(papers)}] Searching: {label}...")

        doi = searcher.search_crossref(query)
        if doi:
            results.append(f"# {label}\nDOI:{doi}")
        else:
            results.append(f"# NOT FOUND: {label}\n# Query: {query}")

        # Rate limiting - be respectful of the API
        time.sleep(0.5)

    # Save results
    output_file = "refs_dois.txt"
    with open(output_file, 'w') as f:
        f.write("# DOIs found via CrossRef search\n")
        f.write("# Use with ris_fetcher_20251022.py to fetch RIS citations\n\n")
        for result in results:
            f.write(f"{result}\n\n")

    print("\n" + "=" * 80)
    print(f"RESULTS SAVED TO: {output_file}")
    print("=" * 80)
    found_count = len([r for r in results if 'DOI:' in r and 'NOT FOUND' not in r])
    print(f"Found: {found_count}/{len(papers)}")
    print("=" * 80)

if __name__ == "__main__":
    main()

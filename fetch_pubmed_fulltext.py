#!/usr/bin/env python3
"""
Fetch full text articles from PubMed IDs and save as TXT files for TTS conversion.
"""

import requests
import xml.etree.ElementTree as ET
from pathlib import Path
import time
import re
from urllib.parse import urlparse
import argparse
from bs4 import BeautifulSoup
import subprocess
import tempfile

class PubMedFetcher:
    def __init__(self, output_dir="pubmed_articles-08OCT2025"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })

    def fetch_article_metadata(self, pmid):
        """Fetch article metadata from PubMed."""
        url = f"{self.base_url}efetch.fcgi"
        params = {
            'db': 'pubmed',
            'id': pmid,
            'retmode': 'xml'
        }

        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"  Error fetching metadata for PMID {pmid}: {e}")
            return None

    def parse_metadata(self, xml_data):
        """Parse article metadata from XML."""
        try:
            root = ET.fromstring(xml_data)
            article = root.find('.//Article')

            if article is None:
                return None

            # Extract title
            title_elem = article.find('.//ArticleTitle')
            title = ''.join(title_elem.itertext()) if title_elem is not None else "Unknown"

            # Extract abstract
            abstract_parts = []
            abstract_elem = article.find('.//Abstract')
            if abstract_elem is not None:
                for abstract_text in abstract_elem.findall('.//AbstractText'):
                    label = abstract_text.get('Label', '')
                    text = ''.join(abstract_text.itertext())
                    if label:
                        abstract_parts.append(f"{label}: {text}")
                    else:
                        abstract_parts.append(text)

            abstract = '\n\n'.join(abstract_parts) if abstract_parts else ""

            # Extract authors
            authors = []
            author_list = article.find('.//AuthorList')
            if author_list is not None:
                for author in author_list.findall('.//Author'):
                    last_name = author.find('LastName')
                    fore_name = author.find('ForeName')
                    if last_name is not None:
                        name = last_name.text
                        if fore_name is not None:
                            name = f"{fore_name.text} {name}"
                        authors.append(name)

            # Extract journal info
            journal_elem = article.find('.//Journal')
            journal = ""
            if journal_elem is not None:
                journal_title = journal_elem.find('.//Title')
                journal = journal_title.text if journal_title is not None else ""

            # Extract publication year
            pub_date = article.find('.//PubDate')
            year = ""
            if pub_date is not None:
                year_elem = pub_date.find('Year')
                year = year_elem.text if year_elem is not None else ""

            # Extract DOI
            article_id_list = root.find('.//ArticleIdList')
            doi = ""
            pmc_id = ""
            if article_id_list is not None:
                for article_id in article_id_list.findall('ArticleId'):
                    id_type = article_id.get('IdType')
                    if id_type == 'doi':
                        doi = article_id.text
                    elif id_type == 'pmc':
                        pmc_id = article_id.text

            return {
                'title': title,
                'abstract': abstract,
                'authors': authors,
                'journal': journal,
                'year': year,
                'doi': doi,
                'pmc_id': pmc_id
            }
        except Exception as e:
            print(f"  Error parsing metadata: {e}")
            return None

    def fetch_from_pmc(self, pmc_id):
        """Fetch full text from PubMed Central if available."""
        if not pmc_id:
            return None

        # Remove PMC prefix if present
        pmc_id = pmc_id.replace('PMC', '')

        url = f"{self.base_url}efetch.fcgi"
        params = {
            'db': 'pmc',
            'id': pmc_id,
            'retmode': 'xml'
        }

        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()

            # Parse XML and extract text
            root = ET.fromstring(response.text)
            text_parts = []

            # Extract all text content
            for elem in root.iter():
                if elem.text and elem.text.strip():
                    text_parts.append(elem.text.strip())
                if elem.tail and elem.tail.strip():
                    text_parts.append(elem.tail.strip())

            full_text = ' '.join(text_parts)
            # Clean up extra whitespace
            full_text = re.sub(r'\s+', ' ', full_text)

            return full_text if len(full_text) > 500 else None
        except Exception as e:
            print(f"  Could not fetch from PMC: {e}")
            return None

    def fetch_from_doi(self, doi):
        """Try to fetch full text using DOI."""
        if not doi:
            return None

        # Try different sources
        sources = [
            f"https://doi.org/{doi}",
            f"https://www.ncbi.nlm.nih.gov/pmc/articles/pmid/{doi}/"
        ]

        for url in sources:
            try:
                response = self.session.get(url, timeout=30, allow_redirects=True)
                if response.status_code == 200:
                    return self.extract_text_from_html(response.text)
            except Exception as e:
                continue

        return None

    def extract_text_from_html(self, html_content):
        """Extract readable text from HTML."""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style", "nav", "header", "footer"]):
                script.decompose()

            # Try to find article content
            article_selectors = [
                'article',
                'main',
                '.article-content',
                '.article-body',
                '#article-content',
                '.content'
            ]

            text = None
            for selector in article_selectors:
                article = soup.select_one(selector)
                if article:
                    text = article.get_text()
                    break

            if not text:
                text = soup.get_text()

            # Clean up text
            lines = [line.strip() for line in text.splitlines()]
            lines = [line for line in lines if line]
            text = '\n\n'.join(lines)

            # Remove excessive whitespace
            text = re.sub(r'\n\n+', '\n\n', text)

            return text if len(text) > 500 else None
        except Exception as e:
            print(f"  Error extracting text from HTML: {e}")
            return None

    def convert_pdf_to_text(self, pdf_content):
        """Convert PDF to text using pdftotext."""
        try:
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_pdf:
                tmp_pdf.write(pdf_content)
                tmp_pdf_path = tmp_pdf.name

            with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp_txt:
                tmp_txt_path = tmp_txt.name

            # Use pdftotext command
            result = subprocess.run(
                ['pdftotext', '-layout', tmp_pdf_path, tmp_txt_path],
                capture_output=True,
                timeout=60
            )

            if result.returncode == 0:
                with open(tmp_txt_path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()

                # Clean up temp files
                Path(tmp_pdf_path).unlink(missing_ok=True)
                Path(tmp_txt_path).unlink(missing_ok=True)

                return text if len(text) > 500 else None

            return None
        except Exception as e:
            print(f"  Error converting PDF: {e}")
            return None

    def clean_filename(self, text):
        """Create a clean filename from text."""
        # Remove invalid characters
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[\s]+', '_', text)
        text = text[:100]  # Limit length
        return text

    def save_article(self, pmid, metadata, full_text=None):
        """Save article as TXT file."""
        # Create filename
        title_clean = self.clean_filename(metadata['title'])
        filename = f"PMID_{pmid}_{title_clean}.txt"
        filepath = self.output_dir / filename

        # Build content
        content_parts = []
        content_parts.append(f"PubMed ID: {pmid}")
        content_parts.append(f"Title: {metadata['title']}")

        if metadata['authors']:
            content_parts.append(f"Authors: {', '.join(metadata['authors'])}")

        if metadata['journal']:
            journal_info = metadata['journal']
            if metadata['year']:
                journal_info += f" ({metadata['year']})"
            content_parts.append(f"Journal: {journal_info}")

        if metadata['doi']:
            content_parts.append(f"DOI: {metadata['doi']}")

        content_parts.append("\n" + "="*80 + "\n")

        if full_text:
            content_parts.append("FULL TEXT:\n")
            content_parts.append(full_text)
        elif metadata['abstract']:
            content_parts.append("ABSTRACT:\n")
            content_parts.append(metadata['abstract'])
        else:
            content_parts.append("No full text or abstract available.")

        content = "\n\n".join(content_parts)

        # Save file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return filepath

    def process_pmid(self, pmid):
        """Process a single PubMed ID."""
        print(f"Processing PMID {pmid}...")

        # Fetch metadata
        xml_data = self.fetch_article_metadata(pmid)
        if not xml_data:
            print(f"  Failed to fetch metadata")
            return False

        metadata = self.parse_metadata(xml_data)
        if not metadata:
            print(f"  Failed to parse metadata")
            return False

        print(f"  Title: {metadata['title'][:80]}...")

        # Try to get full text
        full_text = None

        # Try PMC first
        if metadata['pmc_id']:
            print(f"  Trying PMC ({metadata['pmc_id']})...")
            full_text = self.fetch_from_pmc(metadata['pmc_id'])
            if full_text:
                print(f"  ✓ Retrieved from PMC")

        # Try DOI if PMC failed
        if not full_text and metadata['doi']:
            print(f"  Trying DOI ({metadata['doi']})...")
            full_text = self.fetch_from_doi(metadata['doi'])
            if full_text:
                print(f"  ✓ Retrieved via DOI")

        if not full_text:
            print(f"  ⚠ Full text not available, using abstract only")

        # Save article
        filepath = self.save_article(pmid, metadata, full_text)
        print(f"  Saved to: {filepath.name}")

        return True

    def process_pmid_list(self, pmid_file, delay=0.5):
        """Process a list of PubMed IDs from a file."""
        # Read PMIDs
        with open(pmid_file, 'r') as f:
            pmids = [line.strip() for line in f if line.strip()]

        print(f"Found {len(pmids)} PubMed IDs to process\n")

        success_count = 0
        fail_count = 0

        for i, pmid in enumerate(pmids, 1):
            print(f"\n[{i}/{len(pmids)}]")

            try:
                if self.process_pmid(pmid):
                    success_count += 1
                else:
                    fail_count += 1
            except Exception as e:
                print(f"  Error: {e}")
                fail_count += 1

            # Delay to be respectful to servers
            if i < len(pmids):
                time.sleep(delay)

        print(f"\n{'='*80}")
        print(f"Summary:")
        print(f"  Total: {len(pmids)}")
        print(f"  Success: {success_count}")
        print(f"  Failed: {fail_count}")
        print(f"  Output directory: {self.output_dir}")


def main():
    parser = argparse.ArgumentParser(
        description='Fetch full text articles from PubMed IDs'
    )
    parser.add_argument(
        'pmid_file',
        help='File containing PubMed IDs (one per line)'
    )
    parser.add_argument(
        '-o', '--output',
        default='pubmed_articles',
        help='Output directory (default: pubmed_articles)'
    )
    parser.add_argument(
        '-d', '--delay',
        type=float,
        default=0.5,
        help='Delay between requests in seconds (default: 0.5)'
    )

    args = parser.parse_args()

    fetcher = PubMedFetcher(output_dir=args.output)
    fetcher.process_pmid_list(args.pmid_file, delay=args.delay)


if __name__ == '__main__':
    main()

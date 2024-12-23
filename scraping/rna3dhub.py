"""
Scrape Pseudobase++ for sequences with known pseudoknots.
"""

import requests
import urllib3
from bs4 import BeautifulSoup
from fetch_entrez import entrez_record, StructureRecord
from nakb import contains_pseudoknot

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def scrape_rna3dhub() -> list:
    """
    Retrieve list of PDB ids for high quality RNA structures.
    """
    url = 'http://rna.bgsu.edu/rna3dhub/nrlist/release/3.327/1.5A'

    r = requests.get(url, timeout=5, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    pdb_recs = soup.find_all('a', class_='pdb')
    pdb_ids = [a.text for a in pdb_recs if '|' not in a.text]

    return pdb_ids

def fetch_rna3dhub_record(pdb_id) -> StructureRecord:
    """
    Get entrez info for a pseudobase record.
    """
    entrez = entrez_record(pdb_id, True)

    if not entrez:
        print(f'No Entrez record fetched for {pdb_id}.')
        return False

    has_pseudoknot = contains_pseudoknot(pdb_id)

    if isinstance(has_pseudoknot, bool):
        return StructureRecord(*entrez, contains_pseudoknot(pdb_id))

    return False

if __name__ == "__main__":
    pdb_ids = scrape_rna3dhub()
    print(fetch_rna3dhub_record(pdb_ids[0]))

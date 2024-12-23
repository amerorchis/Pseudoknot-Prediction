"""
Scrape Pseudobase++ for sequences with known pseudoknots.
"""

import requests
import urllib3
from bs4 import BeautifulSoup
from fetch_entrez import entrez_record, StructureRecord

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def scrape_pseudobase() -> list:
    """
    Retrieve records for every known pseudoknot structure in pseudobase.
    """
    url = 'https://rnavlab.utep.edu/dbresults'

    r = requests.get(url, timeout=5, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')

    # Each link to a structure has the text 'view'
    return [link['href'] for link in soup.find_all('a', string='view')]

def fetch_pseudobase_record(struct_id) -> StructureRecord:
    """
    Get entrez info for a pseudobase record.
    """
    acc = ''
    org = ''
    seq = ''
    kingdom = ''
    struct_url = 'https://rnavlab.utep.edu' + struct_id
    struct_r = requests.get(struct_url, timeout=5, verify=False)
    struct_soup = BeautifulSoup(struct_r.text, 'html.parser')
    ncbi_id = struct_soup.find('td', string='NCBI no.').find_next_sibling('td').find('a')
    acc = ncbi_id.text if ncbi_id else acc

    organism_soup = struct_soup.find('td', string=' Organism').find_next('td')
    org = organism_soup.text if organism_soup else org
    if 'virus' in org.lower():
        kingdom = 'Viruses'
    elif 'coli' in org.lower():
        kingdom = 'Bacteria'
    elif 'homo' in org.lower() or 'mus' in org.lower() or 'bos' in org.lower():
        kingdom = 'Eukaryota'

    seq_soup = struct_soup.find('td', string='Bracket view')
    if seq_soup:
        seq_raw = seq_soup.find_next('pre').text.split('\n')
        for i in seq_raw:
            if '$' in i:
                seq_row = i
                seq = '>\n' + seq_row.split('=')[0].split()[-1]
                break

    if acc and seq:
        return StructureRecord(acc, org, kingdom, seq, True)

if __name__ == "__main__":
    #print(scrape_pseudobase()[0])
    print(fetch_pseudobase_record('/static/PKB_files/PKB345'))
    print(fetch_pseudobase_record('/static/PKB_files/PKB1'))

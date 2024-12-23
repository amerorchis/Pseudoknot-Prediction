"""
Retrieve records from Entrez including organism, kingdom, and fasta file using acc or pdb number.
"""

from collections import namedtuple
import re
import urllib
from Bio import Entrez

# Named tuple definitions to store record.
EntrezRecord = namedtuple('EntrezRecord', ['Accession', 'Organism', 'Kingdom', 'fasta'])
StructureRecord = namedtuple('StructureRecord', ['Accession', 'Organism', 'Kingdom', 'FASTA', 'contains_pk'])

def entrez_record(acc_num, pdb=False) -> EntrezRecord:
    """
    Take accession number and retrieve record from Entrez.
    """
    Entrez.email = ""

    # Look up accession number if we just have pdb accession.
    if pdb:
        pdb_handle = Entrez.esearch(db="nucleotide", term=f"{acc_num}[PDB]", limit=1)
        acc_results = Entrez.read(pdb_handle)['IdList']
        if acc_results:
            acc_num = acc_results[0]
        else:
            print(f'No Entrez accession found for {acc_num}')
            return False
        pdb_handle.close()

    # Fetch records from Entrez.
    try:
        genbank_handle = Entrez.efetch(db="nucleotide", id=acc_num, rettype="gb", retmode="text")
        fasta_handle = Entrez.efetch(db="nucleotide", id=acc_num, rettype="fasta", retmode="text")
    except urllib.error.HTTPError as e:
        print(acc_num, e)
        return False

    genbank_record = genbank_handle.read()

    # Parse out organism and kingdom with regex.
    pattern = r'ORGANISM(.*?)REFERENCE'
    genbank_organism = re.search(pattern, genbank_record, re.DOTALL)
    if genbank_organism:
        genbank_organism = genbank_organism.group(1).strip()
        organism, kingdom = genbank_organism.split('\n', 1)
        organism = organism.strip()
        kingdom = kingdom.split(';')[0].strip()

    else:
        organism, kingdom = ('Unknown Organism', 'Unknown Kingdom')

    genbank_handle.close()

    # Retrieve fasta
    fasta = fasta_handle.read()
    fasta_handle.close()

    return EntrezRecord(acc_num, organism, kingdom, fasta)

if __name__ == "__main__":
    print(entrez_record("7MKY", True))

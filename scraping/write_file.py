"""
Create a fasta file with relevant information in the comment field.
"""

from fetch_entrez import StructureRecord

def write_file(rec: StructureRecord):
    """
    Write a fasta file with the structure information
    """
    comment = f'>{rec.Accession}|{rec.Organism}|{rec.Kingdom}|Has Pseudoknot: {rec.contains_pk}'
    fasta = rec.FASTA.split('\n')
    fasta[0] = comment
    fasta = '\n'.join(fasta)

    with open(f'benchmark_fastas/{rec.Accession}.fa', 'w', encoding='utf-8') as f:
        f.write(fasta)

"""
A class defining an RNA sequence for benchmarking.
"""

import re

class Sequence:
    """
    An RNA sequence derived from a FASTA file.
    """
    base_path = 'benchmark_fastas/'
    def __init__(self, file_path):
        # Extract comment and fasta seq from file.
        self.fasta_file = self.base_path + file_path
        with open(self.fasta_file, 'r', encoding='utf-8') as fa:
            self.comment = fa.readline()
            seq = fa.read().strip()

        # Parse out comment
        self.accession, self.organism, self.kingdom, self.has_pk = self.comment.split('|')

        # Clean up comment text
        self.accession = self.accession.replace('>', '')
        if self.kingdom in ['other sequences', 'unclassified sequences.', 'Unclassified.', '']:
            self.kingdom = 'Unknown Kingdom'
        self.has_pk = True if 'True' in self.has_pk else False

        # Store raw sequence.
        self.raw_seq = seq.replace('\n', '')
        self.seq_length = len(self.raw_seq)

        try:
            rna_pattern = re.compile(r"[^ACGTNU]", re.IGNORECASE)
            assert not bool(rna_pattern.search(self.raw_seq))
        except AssertionError:
            print(f'Issue with sequence {self.accession}\n')
            bad_seq = self.raw_seq.upper().replace('A','').replace('C','').replace('G','').replace('T','').replace('N','').replace('U','')
            print(bad_seq)

        # Check if sequence is greater than 1000 nt long.
        self.long = self.seq_length > 1000

    def __str__(self):
        return self.comment

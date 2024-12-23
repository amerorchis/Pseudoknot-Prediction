"""
Build the benchmark set as Python objects.
"""

import os
from Sequence import Sequence

def build_benchmark_set(dir = 'benchmark_fastas'):
    """
    Get list of fasta files in a directory and 
    """
    fastas = os.listdir(dir)
    return [Sequence(fasta) for fasta in fastas if '.fa' in fasta]

# Only include FASTAs that aren't too long
benchmark_set = [i for i in build_benchmark_set() if not i.long]

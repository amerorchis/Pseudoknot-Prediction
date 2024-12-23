"""
A class defining a method for detecting pseudoknots.
"""

from time import time_ns as time
from typing import Callable
import subprocess
from analysis.DataRow import DataRow
from analysis.MethodData import MethodData

from Sequence import Sequence

class Method:
    """
    A methodology for determining pseudoknots.
    """
    def __init__(self, name: str, method: Callable, debug: bool = False):
        self.name = name
        self.debug = debug
        self.assess = method

        self.timeout_file = f'results/{name}/timeout.txt'
        self.kill_file = f'results/{name}/killed.txt'
        self.results_file = f'results/{name}/results.csv'
        self.already_tried = self.seqs_tried()

        self.stats = ''

    def seqs_tried(self, include_kill = True):
        """
        Sometimes the program crashed midway through, this retrieves what progress
        has already been made so that it doesn't have to restart from scratch.
        """
        tried = []
        with open(self.timeout_file, 'r', encoding='utf-8') as file:
            timeouts = file.read()
            tried.extend(timeouts.split('\n'))

        with open(self.results_file, 'r', encoding='utf-8') as file:
            results = file.read()
            results = results.split('\n')[1:]
            tried.extend([i.split(',')[0] for i in results])

        if include_kill:
            with open(self.kill_file, 'r', encoding='utf-8') as file:
                killed = file.read()
                tried.extend(killed.split('\n'))

        return tried

    def test(self, seq: Sequence):
        """
        Test a sequence for pseudoknot prediction accuracy.
        """
        # Make sure it hasn't already been done.
        if seq.accession in self.already_tried:
            return

        start = time() # Record start time
        try:
            pk_prediction = self.assess(seq) # Record prediction
            elapsed = time() - start # Stop timer
            correct = pk_prediction == seq.has_pk # Verify if prediction is correct

            # Check what kind of miss or hit this is (Negative or Positive)
            miss_type = 'None'
            if not correct:
                miss_type = 'FalseNeg' if seq.has_pk else 'FalsePos'

            hit_type = 'None'
            if correct:
                hit_type = 'TruePos' if seq.has_pk else 'TrueNeg'

            # Save that result in a CSV.
            with open(self.results_file, 'a', encoding='utf-8') as file:
                file.write(f'\n{seq.accession},{seq.seq_length},{seq.kingdom},{correct},{elapsed/1e6:.2f},{miss_type},{hit_type}')

            # Some extra logging for debugging
            if self.debug:
                print(f'{self.name} | {seq.accession}')
                print(f'Predicted: {pk_prediction} | Actual: {seq.has_pk}')
                print(f'Accurate? {"Yes" if pk_prediction == seq.has_pk else "No"}\n')

        # Handle subprocess errors
        except subprocess.TimeoutExpired:
            with open(self.timeout_file, 'a', encoding='utf-8') as file:
                file.write(f'\n{seq.accession}')

        except subprocess.CalledProcessError:
            with open(self.kill_file, 'a', encoding='utf-8') as file:
                file.write(f'\n{seq.accession}')

    def summary_stats(self):
        """
        Generate stats for method.
        """

        with open(self.results_file, 'r', encoding='utf-8') as results_file:
            results = results_file.readlines()

        self.stats = MethodData(self.name, [DataRow(i) for i in results[1:]])
        return str(self.stats)

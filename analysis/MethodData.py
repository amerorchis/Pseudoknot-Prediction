"""
Define an object to represent the results of testing a particular method.
"""

from analysis.DataRow import DataRow
from typing import List

class MethodData:
    def __init__(self, name, data: List[DataRow]):
        self.name = name

        # Length stats
        self.total_sequences = len(data)
        self.len_by_seq = [i.seq_length for i in data]
        self.total_residues = sum(self.len_by_seq)

        # Accuracy stats
        self.acc_by_seq = [i.accurate for i in data]
        self.accuracy = self.acc_by_seq.count(True) / self.total_sequences

        # Negatives
        self.miss_by_seq = [i.miss_type for i in data]
        self.false_positives = self.miss_by_seq.count('FalsePos')
        self.false_negatives = self.miss_by_seq.count('FalseNeg')

        # Positives
        self.hits_by_seq = [i.hit_type for i in data]
        self.true_positives = self.hits_by_seq.count('TruePos')
        self.true_negatives = self.hits_by_seq.count('TrueNeg')

        # PPV, NPV, Sensitivity, and Specificity
        """
        PPV measures what % of hits are right, ie high PPV means a positive is almost always true.
        NPV measures how good it is at detecting absence, ie is a negative result likely to be correct.
        Sensitivity measures how well algo does at not missing pseudoknots, ie detection percentage.
        """
        self.ppv = self.true_positives / (self.true_positives + self.false_positives)
        self.npv = self.true_negatives / (self.true_negatives + self.false_negatives)
        self.sensitivity = self.true_positives / (self.true_positives + self.false_negatives)
        self.specificity = self.true_negatives / (self.true_negatives + self.false_positives)

        # Time stats
        self.time_by_seq = [i.time_ms for i in data]
        self.total_time_ms = sum(self.time_by_seq)
        self.total_time_s = self.total_time_ms * 0.001
        self.mean_time_seq = self.total_time_ms / self.total_sequences
        self.mean_time_res = self.total_time_ms / self.total_residues

        # Kingdom stats
        self.kingdom_by_seq = [i.kingdom for i in data]

        kingdom_total_count = {
            'Viruses':self.kingdom_by_seq.count('Viruses'),
            'Unknown Kingdom':self.kingdom_by_seq.count('Unknown Kingdom'),
            'Bacteria':self.kingdom_by_seq.count('Bacteria'),
            'Eukaryota':self.kingdom_by_seq.count('Eukaryota')
        }
        kingdom_correct_count = {
            'Viruses':0,
            'Unknown Kingdom':0,
            'Bacteria':0,
            'Eukaryota':0
        }
        for prediction, kingdom in zip(self.acc_by_seq, self.kingdom_by_seq):
            if prediction is True:
                kingdom_correct_count[kingdom] += 1

        # Kingdom Stats
        self.virus_accuracy = kingdom_correct_count['Viruses'] / kingdom_total_count['Viruses']
        self.unknown_kingdom_accuracy = kingdom_correct_count['Unknown Kingdom'] / kingdom_total_count['Unknown Kingdom']
        self.bacteria_accuracy = kingdom_correct_count['Bacteria'] / kingdom_total_count['Bacteria']
        self.euk_accuracy = kingdom_correct_count['Eukaryota'] / kingdom_total_count['Eukaryota']

        self.accuracies = [
            ['Overall',    self.name, self.accuracy],
            ['Viruses',    self.name, self.virus_accuracy],
            ['Bacteria',   self.name, self.bacteria_accuracy],
            ['Eukaryotes', self.name, self.euk_accuracy],
            ['Unknown',    self.name, self.unknown_kingdom_accuracy]
            ]

    def __str__(self):
        s = self.name + '\n'
        s += '    ' + f'Total sequences: {self.total_sequences}\n'
        s += '    ' + f'Total length: {self.total_residues}\n'
        s += '    ' + f'Accuracy: {self.accuracy:.2f}\n'
        s += '    ' + f'Positive Predictive Value: {self.ppv:.2f}\n'
        s += '    ' + f'Negative Predictive Value: {self.npv:.2f}\n'
        s += '    ' + f'Sensitivity: {self.sensitivity:.2f}\n'
        s += '    ' + f'Specificity: {self.specificity:.2f}\n'
        s += '    ' + f'Total Time (s): {self.total_time_s:.2f}\n'
        s += '    ' + f'Time Per Seq (ms): {self.mean_time_seq:.2f}\n'
        s += '    ' + f'Time Per Residue (ms): {self.mean_time_res:.2f}\n'
        s += '    ' + f'Virus Accuracy: {self.virus_accuracy:.2f}\n'
        s += '    ' + f'Bacteria Accuracy: {self.bacteria_accuracy:.2f}\n'
        s += '    ' + f'Eukaryote Accuracy: {self.euk_accuracy:.2f}\n'
        return s

"""
Generate data about the overall parameters of the benchmark set.
"""

from collections import Counter

from build_benchmark_set import benchmark_set as bms

benchmark_set = [i for i in bms]

sequences = len(benchmark_set) # Number of sequences

# Make dictionaries with counts of organisms and kingdoms
organisms = dict(Counter(seq.organism for seq in benchmark_set))
kingdoms = dict(Counter(seq.kingdom for seq in benchmark_set))

# Get all sequence lengths
lengths = [seq.seq_length for seq in benchmark_set]

# Find min, max, total, and mean
min_length = min(lengths)
max_length = max(lengths)
total_length = sum(lengths)
mean_length = total_length / sequences

# Check how many have pseudoknots
pseudoknot_count = [seq.has_pk for seq in benchmark_set].count(True)
percent_pk = f'{pseudoknot_count/sequences*100:.2f}%'

print(f'Sequences:\n{sequences}\n')
print(f'Organisms:\n{len(organisms.keys())}\n')
print(f'Kingdoms:\n{kingdoms}\n')
print(f'Shortest Seq Length:\n{min_length}\n')
print(f'Longest Seq Length:\n{max_length}\n')
print(f'Mean Seq Length:\n{mean_length}\n')
print(f'Total Seq Length:\n{total_length}\n')
print(f'Pseudoknots:\n{pseudoknot_count}\n')
print(f'% Pseudoknotted:\n{percent_pk}\n')
print(f'Under 300k residues?:\n{total_length<300000}\n')

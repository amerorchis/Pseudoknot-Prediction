"""
Driver to run the tests for pseudoknot detection.
"""

from time import time_ns as time

from build_benchmark_set import benchmark_set, build_benchmark_set
from methods import methods

def run_test(seq_set):
    """
    Test each sequence with each method.
    """
    for method in methods:
        # Test each sequence
        for seq in seq_set:
            method.test(seq)


def mini_test(method):
    """
    Run a test with a small benchmark set to make sure positive and negative outcomes
    can be predicted by the method.
    """
    mini_bms = build_benchmark_set('mini_benchmark_fastas')

    predict_yes = False
    predict_no = False

    # Go through the mini benchmark set and quit when both a positive and negative prediction
    # have been made.
    while mini_bms:
        i = mini_bms.pop()
        pk_predicted = method(i)
        if pk_predicted:
            predict_yes = True
        else:
            predict_no = True

        if predict_yes and predict_no:
            print('Both outcomes predicted.')
            break

    # If both outcomes aren't predicted, raise exception.
    else:
        raise Exception('Same prediction for every sequence.')

if __name__ == "__main__":
    run_test(benchmark_set)
    for i in methods:
        i.summary_stats()

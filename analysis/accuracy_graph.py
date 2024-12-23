"""
Generate accuracy plots with matplotlib.
"""

import matplotlib.pyplot as plt
from methods import methods
import numpy as np

# Get stats for each and sort by accuracy
[i.summary_stats() for i in methods]
methods.sort(key=lambda x : x.stats.accuracy)

def accuracy_by_kingdom_graph():
    """
    Make a graph of the accuracy split out by kingdom/virus.
    """
    overall_means = {i.name: i.stats.accuracy for i in methods}
    virus_means = {i.name: i.stats.virus_accuracy for i in methods}
    eukaryote_means = {i.name: i.stats.euk_accuracy for i in methods}
    bacteria_means = {i.name: i.stats.bacteria_accuracy for i in methods}
    unknown_means = {i.name: i.stats.unknown_kingdom_accuracy for i in methods}

    method_names = list(overall_means.keys())

    bar_width = 0.15

    # Calculate the positions for each group
    x = np.arange(len(method_names))

    # Plot sets of data
    dataset1 = plt.bar(x - 2*bar_width, overall_means.values(), bar_width, color='darkred', label='Overall')
    dataset2 = plt.bar(x - bar_width, virus_means.values(), bar_width, color='springgreen', label='Viruses')
    dataset3 = plt.bar(x, eukaryote_means.values(), bar_width, color='pink', label='Eukaryotes')
    dataset4 = plt.bar(x + bar_width, bacteria_means.values(), bar_width, color='deepskyblue', label='Bacteria')
    dataset5 = plt.bar(x + 2*bar_width, unknown_means.values(), bar_width, color='peru', label='Unknown Kingdom')

    # Format axes and labels
    plt.xlabel('Method')
    plt.ylim(0, 1)
    plt.ylabel('Accuracy')
    plt.title('Accuracy by Kingdom')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=5)
    plt.tight_layout()
    plt.xticks(x, method_names)

    # Function to add labels on top of each bar
    def label(datasets):
        for dataset in datasets:
            height = dataset.get_height()
            plt.text(dataset.get_x() + dataset.get_width()/2., 1.05*height,
                    f'{height:.2f}',
                    ha='center', va='bottom')

    [label(i) for i in [dataset1, dataset2, dataset3, dataset4, dataset5]]

    plt.show()

def accuracy_graph():
    """
    Graph the topline accuracy for each method.
    """
    overall_means = {i.name: i.stats.accuracy for i in methods}

    method_names = list(overall_means.keys())

    bar_width = 0.4

    # Calculate the positions for each group
    x = np.arange(len(method_names))

    # Plot sets of data
    dataset = plt.bar(x - 2*bar_width, overall_means.values(), bar_width, color='darkred')

    # Format axes and labels
    plt.xlabel('Method')
    plt.ylim(0, 1)
    plt.ylabel('Accuracy')
    plt.title('Accuracy by Method')
    plt.tight_layout()
    plt.xticks(x - (2*bar_width), method_names)

    # Function to add labels on top of each bar
    def label(datasets):
        for dataset in datasets:
            height = dataset.get_height()
            plt.text(dataset.get_x() + dataset.get_width()/2., 1.05*height,
                    f'{height:.2f}',
                    ha='center', va='bottom')

    label(dataset)
    plt.show()

def accuracy_by_measure_graph():
    """
    Make a graph for each measure of accuracy.
    """
    overall = {i.name: i.stats.accuracy for i in methods}
    ppv = {i.name: i.stats.ppv for i in methods}
    npv = {i.name: i.stats.npv for i in methods}
    sensitivity = {i.name: i.stats.sensitivity for i in methods}
    specificity = {i.name: i.stats.specificity for i in methods}

    method_names = list(overall.keys())

    bar_width = 0.15

    # Calculate the positions for each group
    x = np.arange(len(method_names))

    # Plot sets of data
    dataset1 = plt.bar(x - 2*bar_width, overall.values(), bar_width, color='darkred', label='Overall')
    dataset2 = plt.bar(x - bar_width, ppv.values(), bar_width, color='springgreen', label='PPV')
    dataset3 = plt.bar(x, npv.values(), bar_width, color='pink', label='NPV')
    dataset4 = plt.bar(x + bar_width, sensitivity.values(), bar_width, color='deepskyblue', label='Sensitivity')
    dataset5 = plt.bar(x + 2*bar_width, specificity.values(), bar_width, color='peru', label='Specificity')

    # Format axes and labels
    plt.xlabel('Method')
    plt.ylim(0, 1.19)
    plt.ylabel('Accuracy')
    plt.title('Measures of Accuracy')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=5)
    plt.tight_layout()
    plt.xticks(x, method_names)

    # Function to add labels on top of each bar
    def label(datasets):
        for dataset in datasets:
            height = dataset.get_height()
            plt.text(dataset.get_x() + dataset.get_width()/2., 1.05*height,
                    f'{height:.2f}',
                    ha='center', va='bottom')

    [label(i) for i in [dataset1, dataset2, dataset3, dataset4, dataset5]]

    plt.show()

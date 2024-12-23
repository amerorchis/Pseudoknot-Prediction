"""
Graph the length of time that each method takes with matplotlib.
"""

import matplotlib.pyplot as plt
import numpy as np

from methods import methods

# Generate stats for each method.
[i.summary_stats() for i in methods]

def length_v_time(log = False):
    """
    Make a graph of length of sequence vs analysis runtime.
    """

    # X axis data is sequence lengths, Y axis is runtime.
    x_data_series = [i.stats.len_by_seq for i in methods]
    y_data_series = [i.stats.time_by_seq for i in methods]
    names = [i.stats.name for i in methods]

    colors = ['blue', 'green', 'red', 'orange', 'purple'] # Colors for the graph

    # Plot each data series with a different color
    for x_data, y_data, color, name in zip(x_data_series, y_data_series, colors, names):
        # Plot the data points
        plt.scatter(x_data, y_data, color=color, label=name, s=10)

    # Set labels and title
    plt.xlabel('Sequence Length')
    plt.xlim(0, 150)

    # Set options for log scale axis
    if log:
        plt.ylabel('Log of Time (ms)')
        plt.yscale('log')
    else:
        plt.ylabel('Time (ms)')

    plt.title('Sequence Length vs. Time')

    # Show legend and plot
    plt.legend()
    plt.show()

def time_bar_graph():
    """
    Make a bar graph of each overall runtime.
    """

    # Create dictionary of times and sort it, find max for scaling.
    times = {i.name: i.stats.total_time_s for i in methods}
    times = {k: v for k, v in sorted(times.items(), key=lambda x: x[1])}
    max_time = max([i.stats.total_time_s for i in methods])

    method_names = list(times.keys())
    bar_width = 0.4

    # Calculate the positions for each group
    x = np.arange(len(method_names))

    # Plot sets of data
    dataset = plt.bar(x - 2*bar_width, times.values(), bar_width, color='mediumseagreen')

    # Format axes and labels
    plt.xlabel('Method')
    plt.ylim(0, max_time * 1.1)
    plt.ylabel('Time (s)')
    plt.title('Total Time by Method')
    plt.tight_layout()
    plt.xticks(x - (2*bar_width), method_names)

    # Function to add labels on top of each bar
    def autolabel(datasets):
        for dataset in datasets:
            height = dataset.get_height()
            plt.text(dataset.get_x() + dataset.get_width()/2., 1.05*height,
                    f'{height:.2f}',
                    ha='center', va='bottom')

    autolabel(dataset)
    plt.show()

if __name__ == "__main__":
    length_v_time()

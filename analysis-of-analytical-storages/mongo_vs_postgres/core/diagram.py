import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

mpl.use('TkAgg')


def show_stats(stats: dict):
    max_val = 1
    species = tuple(stats.keys())
    actions = {}
    for storage in stats.keys():
        for action in stats[storage].keys():
            if not actions.get(action):
                actions[action] = []
            if stats[storage][action]:
                val = sum(stats[storage][action]) / len(stats[storage][action]) * 1000000
            else:
                val = 0
            if val > max_val:
                max_val = val
            actions[action].append(
                val
            )

    x = np.arange(len(species))  # the label locations
    width = 0.3  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(constrained_layout=True)

    for attribute, measurement in actions.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Time (microseconds)')
    ax.set_title('Actions with storages (1 million records)')
    ax.set_xticks(x + width, species)
    ax.legend(loc='upper left', ncols=3)
    ax.set_ylim(0, max_val * 1.1)

    plt.show()

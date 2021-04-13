import matplotlib.pyplot as plt
import seaborn as sns

import os

sns.set()
sns.set_style('whitegrid')


def plot_tradeoff(sw_all, consistency_all, annotations_all = None, fpath=None):
    fig, ax = plt.subplots(1, 1, figsize=(12,8))
    if annotations_all is None:
        annotations_all = [None] * len(sw_all)
    for sw, consistency, text in zip(sw_all, consistency_all, annotations_all):
        ax.scatter(consistency, sw)
        ax.annotate(text, (consistency, sw))
    ax.set_xlabel("Consistency")
    ax.set_ylabel("Total social welfare")
    if fpath is not None:
        os.makedirs(os.path.dirname(fpath), exist_ok=True)
        fig.savefig(fpath)
    else:
        plt.show()
    plt.close()
import matplotlib.pyplot as plt
import seaborn as sns

import os

sns.set()


def plot_tradeoff(sw_all, consistency_all, annotations_all=None, title=None, fpath=None):
    sns.set_style('whitegrid')
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    if annotations_all is None:
        annotations_all = [None] * len(sw_all)
    for sw, consistency, text in zip(sw_all, consistency_all, annotations_all):
        ax.scatter(consistency, sw)
        ax.annotate(text, (consistency, sw))
    ax.set_xlabel("Consistency")
    ax.set_ylabel("Mean social welfare")
    plt.title(title)
    plt.tight_layout()
    if fpath is not None:
        os.makedirs(os.path.dirname(fpath), exist_ok=True)
        fig.savefig(fpath)
    else:
        plt.show()
    plt.close()


def plot_tradeoff_hue(sw_all, consistency_all, annotations_all, annotations_title, title=None, fpath=None, palette="crest"):
    sns.set_style('whitegrid')
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    # if annotations_all is None:
    #     annotations_all = [None] * len(sw_all)
    # for sw, consistency, text in zip(sw_all, consistency_all, annotations_all):
    #     ax.scatter(consistency, sw)
    g = sns.scatterplot(x=consistency_all, y=sw_all,
                        hue=annotations_all, palette=palette, ax=ax, s=100)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.88, box.height])
    plt.xlabel('Consistency', fontsize=24)
    plt.ylabel('Mean social welfare', fontsize=24)
    # g.ax.margins(.15)
    # g.legend.set_title(annotations_title)
    # g.fig.set_size_inches(7, 4.5)
    # g.ax.margins(.15)
    g.legend(title=annotations_title, bbox_to_anchor=(
        1.02, 1.12), loc=2, borderaxespad=0.)
    plt.title(title, fontsize=18)
    if fpath is not None:
        os.makedirs(os.path.dirname(fpath), exist_ok=True)
        fig.savefig(fpath)
    else:
        plt.show()
    plt.close()


def plot_relationship(sw_all, consistency_all, annotations_all, annotations_title, title=None, fpath=None, palette="crest"):
    sns.set_style('ticks')
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    # if annotations_all is None:
    #     annotations_all = [None] * len(sw_all)
    # for sw, consistency, text in zip(sw_all, consistency_all, annotations_all):
    #     ax.scatter(consistency, sw)
    p1 = ax.scatter(x=annotations_all, y=sw_all,
                    color='#7798AB', label='Mean social welfare')
    ax2 = plt.twinx()
    p2 = ax2.scatter(x=annotations_all, y=consistency_all,
                     color='#D17B0F', label='Consistency')

    ps = []
    ps.append(p1)
    ps.append(p2)
    labels = [p.get_label() for p in ps]

    box = ax.get_position()

    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax2.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(ps, labels, bbox_to_anchor=(1.1, 1), loc=2, borderaxespad=0.)

    ax.set_xlabel(annotations_title)
    ax.set_ylabel('Mean social welfare')
    ax2.set_ylabel('Consistency')

    plt.title(title, fontsize=18)
    if fpath is not None:
        os.makedirs(os.path.dirname(fpath), exist_ok=True)
        fig.savefig(fpath)
    else:
        plt.show()
    plt.close()

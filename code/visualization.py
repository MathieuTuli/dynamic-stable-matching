from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import matplotlib

import os
import numpy as np

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
    ax.set_ylabel("Social Welfare")
    plt.title(title)
    plt.tight_layout()
    if fpath is not None:
        os.makedirs(os.path.dirname(fpath), exist_ok=True)
        fig.savefig(fpath)
    else:
        plt.show()
    plt.close()


def plot_tradeoff_hue_fixed_mean(sw_all, consistency_all,
                                 annotations_title, title=None,
                                 fpath=None, palette="crest"):
    sns.set_style('whitegrid')
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    maps = [cm.get_cmap("Purples"), cm.get_cmap('Greys'), cm.get_cmap('Reds'), cm.get_cmap(
        'Blues'), cm.get_cmap('Greens'), cm.get_cmap("Purples")]
    for idx, (mean, data) in enumerate(sw_all.items()):
        colour = maps[idx]
        sharpness = 0.2
        for j, (var, val) in enumerate(data):
            ax.scatter(x=[consistency_all[mean][j][1]],
                       y=[val],
                       c=colour(sharpness + (1 - sharpness) * j / len(data)),
                       # hue=annotations_all,
                       # palette=palette,
                       # ax=ax,
                       s=100,
                       label=f'$\mu={mean}, \sigma^2={var}$'
                       )
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.88, box.height])
    plt.xlabel('Consistency', fontsize=24)
    plt.ylabel('Mean social welfare', fontsize=24)
    # ax.legend(title=annotations_title, bbox_to_anchor=(
    #     1.02, 1.12), loc=2, borderaxespad=0.)
    fig.colorbar(cm.ScalarMappable(norm=matplotlib.colors.Normalize(0, 10),
                                   cmap=maps[0]), ax=ax)
    plt.title(title, fontsize=18)
    if fpath is not None:
        os.makedirs(os.path.dirname(fpath), exist_ok=True)
        plt.tight_layout()
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
    plt.ylabel('Social Welfare', fontsize=24)
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
                    color='#7798AB', label='Social Welfare')
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
    ax.set_ylabel('Social Welfare')
    ax2.set_ylabel('Consistency')

    plt.title(title, fontsize=18)
    if fpath is not None:
        os.makedirs(os.path.dirname(fpath), exist_ok=True)
        fig.savefig(fpath)
    else:
        plt.show()
    plt.close()


def plot_tradeoff_hue_extra(
    sw_all, consistency_all, annotations_all, annotations_title,
    sw_extra, consistency_extra, labels_extra, colors_extra,
    xlabel="Consistency", ylabel="Social Welfare",
    title=None, fpath=None, palette="crest"
):
    sns.set_style('whitegrid')
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    # if annotations_all is None:
    #     annotations_all = [None] * len(sw_all)
    # for sw, consistency, text in zip(sw_all, consistency_all, annotations_all):
    #     ax.scatter(consistency, sw)
    g = sns.scatterplot(x=consistency_all, y=sw_all,
                        hue=annotations_all, palette=palette, ax=ax, s=100, legend="brief")
    ylim_min = np.min(list(sw_all) + list(sw_extra))
    if ylim_min < 0.01:
        ylim_min = -0.005
    else:
        ylim_min *= 0.9
    ax.set_ylim(ylim_min, np.max(list(sw_all) + list(sw_extra)) * 1.1)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.82, box.height])
    plt.xlabel(xlabel, fontsize=22, labelpad=10)
    plt.ylabel(ylabel, fontsize=22, labelpad=20)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    # g.ax.margins(.15)
    # g.legend.set_title(annotations_title)
    # g.fig.set_size_inches(7, 4.5)
    # g.ax.margins(.15)

    for consistency, sw, label, color in zip(consistency_extra, sw_extra, labels_extra, colors_extra):
        g.scatter(consistency, sw, s=100, color=color, marker="x", label=label)
    # ax.legend()
    lgd = ax.legend(title=annotations_title, bbox_to_anchor=(
        1.03, 1), loc=2, borderaxespad=0., fontsize=15)
    lgd.get_title().set_fontsize('17')
    ttl = plt.title(title, fontsize=24, pad=20, fontweight='bold')
    if fpath is not None:
        os.makedirs(os.path.dirname(fpath), exist_ok=True)
        fig.savefig(fpath)
    else:
        plt.show()
    plt.close()


def plot_utility_matching(
    men_utilities, women_utilities, men_match, women_match, title=None, fpath=None
):

    fig, axs = plt.subplots(len(men_utilities), 2, sharey=True, figsize=(10, 8))

    lblue_patch = mpatches.Patch(color='#9dbccf', label='Unmatched woman')
    dblue_patch = mpatches.Patch(color='#1f4d69', label='Matched woman')
    lred_patch = mpatches.Patch(color='#f7abab', label='Unmatched man')
    dred_patch = mpatches.Patch(color='#803333', label='Matched man')
    axs[0,1].legend(handles=[lblue_patch,dblue_patch,lred_patch,dred_patch],bbox_to_anchor=(
        1.05, 1), loc=2, borderaxespad=0., fontsize=15)

    fig.add_subplot(111, frameon=False)
    # hide tick and tick label of the big axes
    plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
    plt.grid(False)

    plt.ylabel("Utility", fontsize=22, labelpad=10)


    plt.setp(axs, ylim=(0,0.3))

    for (i, man_utilities) in enumerate(men_utilities):
        #9dbccf 7798AB
        clr = ['#1f4d69' if (x==men_match[i]) else '#9dbccf' for x in [w.id for w in man_utilities.keys()]]
        p = sns.barplot(x = ['woman '+str(w.id) for w in man_utilities.keys()],y=list(man_utilities.values()), ax=axs[i,0], palette=clr)
        p.set_xticklabels(p.get_xticklabels(),rotation=45, fontsize=16)

    for (i, woman_utilities) in enumerate(women_utilities):
        #f7abab 803333
        clr = ['#803333' if (x==women_match[i]) else '#f7abab' for x in [m.id for m in woman_utilities.keys()]]
        p = sns.barplot(x = ['man '+str(m.id) for m in woman_utilities.keys()],y=list(woman_utilities.values()), ax=axs[i,1], palette=clr)
        p.set_xticklabels(p.get_xticklabels(),rotation=45, fontsize=16)

    for i in range(len(men_utilities)-1):
        axs[i,0].xaxis.set_visible(False)
        axs[i,1].xaxis.set_visible(False)

    axs[0,0].set_title('Men', fontsize=22, pad=10)
    axs[0,1].set_title('Women', fontsize=22, pad=10)

    fig.subplots_adjust(bottom=0.15, top=0.85, right=0.7)

    ttl = plt.title(title, fontsize=24, pad=40, fontweight='bold')


    if fpath is not None:
        os.makedirs(os.path.dirname(fpath), exist_ok=True)
        fig.savefig(fpath)
    else:
        plt.show()
    plt.close()
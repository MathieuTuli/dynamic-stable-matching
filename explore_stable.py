from copy import deepcopy

import pdb
import random

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()
sns.set_style('whitegrid')

from dynamics import (
    initialize_utilities_from_array,
    initialize_utilities_constant,
    initialize_utilities_gaussian,
    initialize_utilities_uniform_random,
    update_utilities_with_match,
    update_utilities_with_match_decay_only,
    update_utilities,
    initialize_excitement_from_array,
    initialize_excitement_constant,
    initialize_excitement_gaussian,
    initialize_excitement_uniform_random)
from evaluate import Evaluator, compute_consistency, compute_social_welfare
from utils import config_file_parser
from agents import Man, Woman
from match import get_all_pairs, get_stable_pairs, compute_social_welfare


def main():
    seed = 1000
    random.seed(seed)
    np.random.seed(seed)

    horizon = 10
    size = 4
    
    men = [Man() for i in range(size)]
    women = [Woman() for i in range(size)]
    
    initialization = {'name': 'constant', 'value': 0.1}
    excitement = {'name': 'constant', 'value': 0.1}
    update = 'match'

    if initialization['name'] == 'constant':
        initialize_utilities_constant(
            men, women, initialization['value']
        )
    elif initialization['name'] == 'gaussian':
        initialize_utilities_gaussian(
            men, women, initialization['mean'], initialization['var']
        )
    elif initialization['name'] == 'uniform_random':
        initialize_utilities_uniform_random(
            men, women, 0.0, 1.0
        )
    else:
        raise ValueError(f'Uknown initialization method {init}')
    if excitement['name'] == 'constant':
        initialize_excitement_constant(
            men, women, excitement['value']
        )
    elif excitement['name'] == 'gaussian':
        initialize_excitement_gaussian(
            men, women, excitement['mean'], excitement['var']
        )
    elif excitement['name'] == 'uniform_random':
        initialize_excitement_uniform_random(
            men, women, 0.0, 1.0
        )
    else:
        raise ValueError(
            f'Uknown excitement initialization method {excitement}'
        )

    print("Number of agents in each group: " + str(size))
    print("Number of timesteps: " + str(horizon))
    print(initialization['name'] + " initialization + " +
          excitement['name'] + " excitement")

    update_algorithm = update_utilities_with_match
    most_recent_match = None
    results_all = []
    for i in range(horizon):
        print("Timestep " + str(i) + ": ")
        # print("Men's preferences:")
        # for man in men:
            # print([w.id for w in man.preferences])
            # print([(w.id, man.utilities[w]) for w in man.preferences])
        # print("Women's preferences:")
        # for woman in women:
        #     print([m.id for m in woman.preferences])
            # print([(m.id, woman.utilities[m]) for m in woman.preferences])

        all_pairs = get_all_pairs(men, women)
        stable_matches_all = get_stable_pairs(men, women, all_pairs)

        print("Number of stable matches:", len(stable_matches_all))
        
        if i > 0:
            results = []
            for match in stable_matches_all:
                welfare = compute_social_welfare(match)
                consistency = compute_consistency(match, most_recent_match)
                results_all.append([consistency, welfare])
                results.append([consistency, welfare])
            fig, ax = plt.subplots(1, 1, figsize=(12,8))
            for consistency, match in results:
                ax.scatter(consistency, match)
                print(consistency, match)
            plt.show()
            plt.close()
        
        # update with a random stable match
        most_recent_match = random.choice(stable_matches_all)
        for man, woman in most_recent_match:
            man.match = woman
            woman.match = man
        update_algorithm(men, women)

    # results_all = np.array(results_all)
    fig, ax = plt.subplots(1, 1, figsize=(12,8))
    for consistency, match in results_all:
        ax.scatter(consistency, match)
    plt.show()
    plt.close()


if __name__ == "__main__":
    main()

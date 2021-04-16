from copy import deepcopy

import pdb
import random
import os

import numpy as np
from visualization import plot_tradeoff, plot_tradeoff_hue_extra

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
from match import probabilistic, is_stable, MPDA, WPDA


def main():
    seed = 1000

    horizon = 10
    # size = 10
    # size = 20
    size = 6
    
    men = [Man() for i in range(size)]
    women = [Woman() for i in range(size)]
    
    # initialization = {'name': 'constant', 'value': 0.1}
    initialization = {'name': 'gaussian', 'mean': 10, 'var': 10}
    # excitement = {'name': 'constant', 'value': 0.1}
    excitement = {'name': 'gaussian', 'mean': 0.1, 'var': 0.1}
    update = 'match'

    guarantee_stability = True
    # guarantee_stability = False

    def initialize(men, women):
        random.seed(seed)
        np.random.seed(seed)
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
                f'Unknown excitement initialization method {excitement}'
            )

    print("Number of agents in each group: " + str(size))
    print("Number of timesteps: " + str(horizon))
    print(initialization['name'] + " initialization + " +
          excitement['name'] + " excitement")

    update_algorithm = update_utilities_with_match
    results_all = []
    annotations_all = []
    for prob in np.linspace(0.0, 1.0, num=50):
        most_recent_match = None
        initialize(men, women)
        results = []
        print("prob:", prob)
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

            new_match = probabilistic(0.0 if i == 0 else prob, men, women, stable=guarantee_stability)
            if new_match is None:
                # no change
                new_match = most_recent_match

            if i > 0:
                welfare = compute_social_welfare(new_match)
                consistency = compute_consistency(new_match, most_recent_match)
                results.append([welfare, consistency])
                print(welfare, consistency)
            
            most_recent_match = new_match
            print("Stability:", is_stable(men, women, most_recent_match))
            update_algorithm(men, women)
        
        results = np.array(results)
        results_all.append([np.mean(results[:, 0]), np.mean(results[:, 1])])
        annotations_all.append(prob)
        # annotations_all.append(f"p={prob:.4f}")
    
        results_extra = []
    labels_extra = ['MPDA', 'WPDA']
    for alg in [MPDA, WPDA]:
        initialize(men, women)
        results = []
        most_recent_match = None
        for i in range(horizon):
            print("Timestep " + str(i) + ": ")

            new_match = alg(men, women)

            if i > 0:
                welfare = compute_social_welfare(new_match)
                consistency = compute_consistency(new_match, most_recent_match)
                results.append([welfare, consistency])
                print(welfare, consistency)
            
            most_recent_match = new_match
            print("Stability:", is_stable(men, women, most_recent_match))
            update_algorithm(men, women)
        
        results = np.array(results)
        results_extra.append([np.mean(results[:, 0]), np.mean(results[:, 1])])
    
    results_all = np.array(results_all)
    results_extra = np.array(results_extra)
    colors_extra = ["red", "blue"]

    results_all = np.array(results_all)
    # plot_tradeoff_hue_extra(
    #     results_all[:, 0], results_all[:, 1],
    #     annotations_all, "probability",
    #     results_extra[:, 0], results_extra[:, 1],
    #     labels_extra, colors_extra,
    #     title=f"Prob (N={size}, T={horizon})")
    
    out_dir = "visualization"
    alg_name = "Prob" if not guarantee_stability else "Prob-Stable"
    plot_tradeoff_hue_extra(
        results_all[:, 0], results_all[:, 1],
        annotations_all, "probability",
        results_extra[:, 0], results_extra[:, 1],
        labels_extra, colors_extra,
        fpath=os.path.join(out_dir, f"{alg_name}_{size}_{horizon}_{initialization['mean']}_{initialization['var']}.pdf"),
        title=f"{alg_name} (N={size}, T={horizon}, $\mu_u$={initialization['mean']}, $\sigma_u$={initialization['var']}, , $\mu_e$={excitement['mean']}, $\sigma_e$={excitement['var']})")
    plot_tradeoff_hue_extra(
        results_all[:, 0], results_all[:, 1],
        annotations_all, "probability",
        results_extra[:, 0], results_extra[:, 1],
        labels_extra, colors_extra,
        fpath=os.path.join(out_dir, f"{alg_name}_{size}_{horizon}_{initialization['mean']}_{initialization['var']}.png"),
        title=f"{alg_name} (N={size}, T={horizon}, $\mu_u$={initialization['mean']}, $\sigma_u$={initialization['var']}, , $\mu_e$={excitement['mean']}, $\sigma_e$={excitement['var']})")


    # plot_tradeoff(results_all[:, 0], results_all[:, 1], annotations_all=annotations_all, title=f"N={size} Time Steps={horizon} Guarantee Stability={guarantee_stability}")
    


if __name__ == "__main__":
    main()

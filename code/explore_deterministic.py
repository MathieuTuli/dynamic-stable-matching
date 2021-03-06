from copy import deepcopy

import pdb
import random
import os

import numpy as np
from visualization import plot_tradeoff, plot_tradeoff_hue_extra, plot_tradeoff_hue

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
from match import deterministic, is_stable, MPDA, WPDA, get_num_blocking


def main():
    seed = 1000

    horizon = 10
    # horizon = 100
    # size = 10
    # size = 100
    size = 20
    
    men = [Man() for i in range(size)]
    women = [Woman() for i in range(size)]
    
    # initialization = {'name': 'constant', 'value': 0.1}
    initialization = {'name': 'gaussian', 'mean': 10, 'var': 10}
    # excitement = {'name': 'constant', 'value': 0.1}
    excitement = {'name': 'gaussian', 'mean': 0.1, 'var': 0.1}
    update = 'match'

    guarantee_stability = False

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
    instabilities_all = []
    annotations_all = []
    for consistency_num in range(size + 1):
        initialize(men, women)
        results = []
        instabilities = []
        most_recent_match = None
        print("Consistency thresh:", consistency_num)
        for i in range(horizon):
            print("Timestep " + str(i) + ": ")

            new_match = deterministic(consistency_num, men, women, most_recent_match)
            if new_match is None:
                # no change
                new_match = most_recent_match
            

            if i > 0:
                welfare = compute_social_welfare(new_match)
                instability = get_num_blocking(men, women, new_match) * 1.0 / len(men)
                consistency = compute_consistency(new_match, most_recent_match)
                results.append([welfare, consistency])
                instabilities.append(instability)
                print(welfare, consistency)
                print("Instability:", instability)
            
            most_recent_match = new_match
            print("Stability:", is_stable(men, women, most_recent_match))
            update_algorithm(men, women)
        
        results = np.array(results)
        results_all.append([np.mean(results[:, 0]), np.mean(results[:, 1])])
        annotations_all.append(consistency_num * 1.0 / size)
        instabilities_all.append(np.mean(instabilities))
        # annotations_all.append(f"{consistency_num * 1.0 / size:.4f}")

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
    # plot_tradeoff_hue(
    #     results_all[:, 0], results_all[:, 1],
    #     annotations_all, "consistency threshold",
    #     title=f"N={size} Time Steps={horizon} Guarantee Stability={guarantee_stability}")
    out_dir = "visualization"
    plot_tradeoff_hue_extra(
        results_all[:, 0], results_all[:, 1],
        annotations_all, "consistency threshold",
        results_extra[:, 0], results_extra[:, 1],
        labels_extra, colors_extra,
        fpath=os.path.join(out_dir, f"Det_{size}_{horizon}_{initialization['mean']}_{initialization['var']}.pdf"),
        title=f"Det (N={size}, T={horizon}, $\mu_u$={initialization['mean']}, $\sigma_u$={initialization['var']}, , $\mu_e$={excitement['mean']}, $\sigma_e$={excitement['var']})")
    plot_tradeoff_hue_extra(
        results_all[:, 0], results_all[:, 1],
        annotations_all, "consistency threshold",
        results_extra[:, 0], results_extra[:, 1],
        labels_extra, colors_extra,
        fpath=os.path.join(out_dir, f"Det_{size}_{horizon}_{initialization['mean']}_{initialization['var']}.png"),
        title=f"Det (N={size}, T={horizon}, $\mu_u$={initialization['mean']}, $\sigma_u$={initialization['var']}, , $\mu_e$={excitement['mean']}, $\sigma_e$={excitement['var']})")
    plot_tradeoff_hue_extra(
        results_all[:, 0], instabilities_all,
        annotations_all, "consistency threshold",
        results_extra[:, 0], [0, 0],
        labels_extra, colors_extra,
        fpath=os.path.join(out_dir, f"Det_sw_{size}_{horizon}_{initialization['mean']}_{initialization['var']}.pdf"),
        xlabel="Instability",
        title=f"Det (N={size}, T={horizon}, $\mu_u$={initialization['mean']}, $\sigma_u$={initialization['var']}, , $\mu_e$={excitement['mean']}, $\sigma_e$={excitement['var']})")
    plot_tradeoff_hue_extra(
        results_all[:, 0], instabilities_all,
        annotations_all, "consistency threshold",
        results_extra[:, 0], [0, 0],
        labels_extra, colors_extra,
        fpath=os.path.join(out_dir, f"Det_sw_{size}_{horizon}_{initialization['mean']}_{initialization['var']}.png"),
        xlabel="Instability",
        title=f"Det (N={size}, T={horizon}, $\mu_u$={initialization['mean']}, $\sigma_u$={initialization['var']}, , $\mu_e$={excitement['mean']}, $\sigma_e$={excitement['var']})")
    # plot_tradeoff(results_all[:, 0], results_all[:, 1], annotations_all=annotations_all, title=f"N={size} Time Steps={horizon} Guarantee Stability={guarantee_stability}")
    


if __name__ == "__main__":
    main()

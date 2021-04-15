from copy import deepcopy

import pdb
import random

import numpy as np
from visualization import plot_tradeoff, plot_tradeoff_hue_extra, plot_tradeoff_hue, plot_utility_matching

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

    horizon = 1
    # size = 10
    size = 5
    
    men = [Man() for i in range(size)]
    women = [Woman() for i in range(size)]
    
    # initialization = {'name': 'constant', 'value': 0.1}
    initialization = {'name': 'gaussian', 'mean': 10, 'var': 1}
    excitement = {'name': 'constant', 'value': 0.1}
    # excitement = {'name': 'gaussian', 'mean': 0.1, 'var': 0.1}
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
    for consistency_num in range(1):
        initialize(men, women)
        results = []
        instabilities = []
        most_recent_match = None
        print("Consistency thresh:", consistency_num)
        for i in range(horizon):
            print("Timestep " + str(i) + ": ")

            men_util = [man.utilities for man in men]
            women_util = [woman.utilities for woman in women]
            
            new_match = deterministic(consistency_num, men, women, most_recent_match)
            if new_match is None:
                # no change
                new_match = most_recent_match

            matches = [(man.id, woman.id) for man, woman in new_match]
            man_matches = sorted(matches, key= lambda x:x[0])
            man_matches = [match[1] for match in man_matches]
            woman_matches = sorted(matches, key= lambda x:x[1])
            woman_matches = [match[0] for match in woman_matches]
            
            plot_utility_matching(men_util, women_util, man_matches, woman_matches, title="Timestep " + str(i))
            
            most_recent_match = new_match
            print("Stability:", is_stable(men, women, most_recent_match))
            update_algorithm(men, women)
    


if __name__ == "__main__":
    main()

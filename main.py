from argparse import Namespace, ArgumentParser
from copy import deepcopy

import pdb

import numpy as np

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
from evaluate import Evaluator
from utils import config_file_parser
from agents import Man, Woman
from match import MPDA, WPDA


parser = ArgumentParser(__doc__)
# parser = ArgumentParser(__doc__)
parser.add_argument("--config", default=None, help='Config file')
parser.add_argument("-s", "--size", type=int,
                    dest='size',
                    default=10, help="Population size")
parser.add_argument("--initialization",
                    type=dict,
                    default=None,
                    help='Initialization type')
parser.add_argument("--excitement",
                    type=dict,
                    default=None,
                    help='Excitement initialization type')
parser.add_argument("--matching",
                    default='MPDA',
                    choices=['MPDA', 'WPDA'],
                    help='Matching algorithm')
parser.add_argument("--update",
                    default='regular',
                    choices=['regular', 'match', 'match_decay_only'],
                    help='Dynamic updating algorithm')
parser.add_argument("--seed", default=1000,
                    type=int,
                    help='Seed')
parser.add_argument("--horizon", default=1,
                    type=int,
                    help='Horizon')
parser.add_argument("--debug", default=False,
                    type=bool,
                    help='Debug flag')


def main(args: Namespace):
    if args.debug:
        pdb.set_trace()
    np.random.seed(args.seed)
    history = list()
    men = [Man() for i in range(args.size)]
    women = [Woman() for i in range(args.size)]
    if args.initialization['name'] == 'constant':
        initialize_utilities_constant(
            men, women, args.initialization['value']
        )
    elif args.initialization['name'] == 'gaussian':
        initialize_excitement_gaussian(
            men, women, args.initialization['mean'], args.initialization['var']
        )
    elif args.initialization['name'] == 'uniform_random':
        initialize_excitement_uniform_random(
            men, women, 9.5, 10.5
        )
    else:
        raise ValueError(f'Uknown initialization method {args.init}')
    if args.excitement['name'] == 'constant':
        initialize_excitement_constant(
            men, women, args.excitement['value']
        )
    elif args.excitement['name'] == 'gaussian':
        initialize_excitement_gaussian(
            men, women, args.excitement['mean'], args.excitement['var']
        )
    elif args.excitement['name'] == 'uniform_random':
        initialize_excitement_uniform_random(
            men, women, 0.0, 1.0
        )
    else:
        raise ValueError(
            f'Uknown excitement initialization method {args.excitement}'
        )
    matching_algorithm = MPDA if args.matching == 'MPDA' else\
        WPDA if args.matchings == 'WPDA' else None
    if args.update == 'regular':
        update_algorithm = update_utilities
    elif args.update == 'match':
        update_algorithm = update_utilities_with_match
    elif args.update == 'match_decay_only':
        update_algorithm = update_utilities_with_match_decay_only
    else:
        raise ValueError(
            f'Unknown updating transition method {args.update}'
        )

    # print("Matching algorithm: " + args.matching)
    # print("Update method: "  + args.update)
    # print("Number of agents in each group: " + str(args.size))
    # print("Number of timesteps: "  + str(args.horizon))
    # print(args.initialization['name'] + " initialization + " + args.excitement['name'] + " excitement")

    evaluator = Evaluator(args.size)
    averages = []
    longest = []
    # print("Preferences: ")
    for i in range(args.horizon):

        # print("Timestep" + str(i) + ": ")
        # print("Men's preferences:")
        # for man in men:
        #     print([w.id for w in man.preferences])
        # print("Women's preferences:")
        # for woman in women:
        #     print([m.id for m in woman.preferences])

        pairs = matching_algorithm(men, women)
        history.append([(pair[0].id, pair[1].id) for pair in pairs])
        update_algorithm(men, women)
        averages.append(evaluator.evaluate_average(history))
        longest.append(evaluator.evaluate_longest(history))
    consistency_rate = evaluator.evaluate_consistency_rate(history)

    # print("Matches: ")
    # for i, matches in enumerate(history):
    #     print("Timestep " + str(i)  + ": " , end='')
    #     print(matches)
    # print("Average number of timestep staying married: ", end='')
    # print(averages)
    # print("Largest number of timestep staying married: ", end='')
    # print(longest)
    # print("Proportion of marriage persisted: ", end='')
    # print(consistency_rate)


if __name__ == "__main__":
    args = parser.parse_args()
    if args.config is not None:
        args = config_file_parser(args)
    main(args)

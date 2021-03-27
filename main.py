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
# from evaluate import Evaluator
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
                    help='Initialization type')
parser.add_argument("--excitement",
                    type=dict,
                    help='Excitement initialization type')
parser.add_argument("--matching",
                    default='MPDA',
                    help='Matching algorithm')
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
            men, women, args.initialization['value'])
    elif args.init == ['']:
        ...
    else:
        raise ValueError(f'Uknown initialization method {args.init}')
    if args.excitement['name'] == 'gaussian':
        initialize_excitement_gaussian(
            men, women, args.excitement['mean'], args.excitement['var'])
    elif args.init == ['']:
        ...
    else:
        raise ValueError(
            f'Uknown excitement initialization method {args.init}')
    matching_algorithm = MPDA if args.matching == 'MPDA' else\
        WPDA if args.matchings == 'WPDA' else None
    # evaluator = Evaluator(args.size)
    for i in range(args.horizon):
        pairs = matching_algorithm(men, women)
        history.append([(pair[0].id, pair[1].id) for pair in pairs])
        update_utilities(men, women)
        # evaluator.evaluate_average()


if __name__ == "__main__":
    args = parser.parse_args()
    if args.config is not None:
        args = config_file_parser(args)
    main(args)

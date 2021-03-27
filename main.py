from argparse import Namespace

import pdb

from configargparse import ArgumentParser, YAMLConfigFileParser

import numpy as np

from dynamics import *
from evluator import Evaluator
from match import MPDA, WPDA, MatchAlgorithms
from agents import Man, Woman
from copy import deepcopy


parser = ArgumentParser(
    config_file_parser_class=YAMLConfigFileParser)
parser.add_argument("--config", is_config_file=True)
parser.add_argument("-a", "--algorithm", dest='algorithm',
                    default=MatchAlgorithms.MPDA,
                    choices=MatchAlgorithms.__members__.values(),
                    help="The algorithm to run.")
parser.add_argument("-s", "--size", type=int,
                    dest='size',
                    default=10, help="Population size")
parser.add_argument("--dynamics", default=Dynamics.STATIC,
                    choices=Dynamics.__members__.values(),
                    help='Dynamics type')
parser.add_argument("--seed", default=1000,
                    type=int,
                    help='Seed')
parser.add_argument("--horizon", default=1,
                    type=int,
                    help='Horizon')


def main(args: Namespace):
    pdb.set_trace()
    np.random.seed(args.seed)
    history = list()
    men = [Man() for i in range(args.size)]
    women = [Woman() for i in range(args.size)]
    initialize_utilities_constant(men, women, 1.0)
    initialize_excitement_gaussian(men, women, 0, 1)
    evaluator = Evaluator(args.size)
    for i in range(args.horizon):
        # initialize_excitement_constant(men, women, 0.5)
        pairs = MPDA(men, women)
        history.append([(pair[0].id, pair[1].id) for pair in pairs])
        update_utilities(men, women)
        evaluator.evaluate_average()


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)

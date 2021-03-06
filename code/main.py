from argparse import Namespace, ArgumentParser
# from copy import deepcopy
from pathlib import Path

import pdb

import numpy as np
import json

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
from match import MPDA, WPDA, BFWO, BFSM


parser = ArgumentParser(__doc__)
# parser = ArgumentParser(__doc__)
parser.add_argument("--config", default=None, help='Config file')
parser.add_argument("-s", "--size", type=int,
                    dest='size',
                    default=10, help="Population size")
parser.add_argument("--initialization",
                    # type=dict,
                    default=None,
                    help='Initialization type')
parser.add_argument("--excitement",
                    # type=dict,
                    default=None,
                    help='Excitement initialization type')
parser.add_argument("--matching",
                    default='MPDA',
                    choices=['MPDA', 'WPDA', 'BFWO', 'BFSM'],
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
parser.add_argument("--print", default=False,
                    type=bool,
                    help='Print flag')
parser.add_argument("--output", default='outputs',
                    type=str,
                    help='Output dir')


def main(args: Namespace):
    data = args.__dict__.copy()
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
        initialize_utilities_gaussian(
            men, women, args.initialization['mean'], args.initialization['var']
        )
    elif args.initialization['name'] == 'uniform_random':
        initialize_utilities_uniform_random(
            men, women, 0.0, 1.0
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
        WPDA if args.matching == 'WPDA' else BFWO if args.matching == 'BFWO' \
        else BFSM if args.matching == 'BFSM' else None
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

    if args.print:
        print("Matching algorithm: " + args.matching)
        print("Number of agents in each group: " + str(args.size))
        print("Number of timesteps: " + str(args.horizon))
        print(args.initialization['name'] + " initialization + " +
              args.excitement['name'] + " excitement")

    evaluator = Evaluator(args.size)
    averages = []
    longest = []
    if args.print:
        print("Preferences: ")
    data['preferences'] = dict()
    social_welfare = list()
    consistency = list()
    prev_pairs = None
    for i in range(args.horizon):
        data['preferences'][i] = dict()
        data['preferences'][i]['men'] = dict()
        data['preferences'][i]['women'] = dict()
        if args.print:
            print("Timestep " + str(i) + ": ")
            print("Men's preferences:")
        for man in men:
            data['preferences'][i]['men'][man.id] = \
                [w.id for w in man.preferences]
            if args.print:
                print(data['preferences'][i]['men'][man.id])
            # print([(w.id, man.utilities[w]) for w in man.preferences])
        if args.print:
            print("Women's preferences:")
        for woman in women:
            data['preferences'][i]['women'][woman.id] = \
                [m.id for m in woman.preferences]
            if args.print:
                print(data['preferences'][i]['women'][woman.id])
            # print([(m.id, woman.utilities[m]) for m in woman.preferences])

        pairs = matching_algorithm(men, women)
        history.append([(pair[0].id, pair[1].id) for pair in pairs])
        update_algorithm(men, women)
        if i > 0:
            social_welfare.append(compute_social_welfare(pairs))
            consistency.append(compute_consistency(pairs, prev_pairs))
        averages.append(evaluator.evaluate_average(history))
        longest.append(evaluator.evaluate_longest(history))
        prev_pairs = pairs
    data['social_welfare'] = np.mean(social_welfare)
    data['consistency'] = np.mean(consistency)
    consistency_rate = evaluator.evaluate_consistency_rate(history)

    if args.print:
        print("Matches: ")
    data['matches'] = dict()
    for i, matches in enumerate(history):
        if args.print:
            print("Timestep " + str(i) + ": ", end='')
            print(matches)
        data['matches'][i] = matches
    if args.print:
        print("Average number of timestep staying married: ", end='')
        print(averages)
        print("Largest number of timestep staying married: ", end='')
        print(longest)
        print("Proportion of marriage persisted: ", end='')
        print(consistency_rate)
    data['averages'] = averages
    data['longest'] = longest
    data['consistency_rate'] = consistency_rate
    save(args, data)
    return data


def save(args, data) -> None:
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True, parents=True)
    filename = 'results'
    filename += f'_maching={args.matching}'
    filename += f'_size={args.size}'
    filename += f'_horizon={args.horizon}'
    filename += f'_update={args.update}'
    filename += f'_seed={args.seed}'
    filename += '_initialization='
    for k, v in args.initialization.items():
        filename += f'{k}:{v},'
    filename += '_excitement='
    for k, v in args.initialization.items():
        filename += f'{k}:{v},'
    filename += '.json'
    with (output_dir / filename).open('w') as f:
        json.dump(data, f)


if __name__ == "__main__":
    args = parser.parse_args()
    if args.config is not None:
        args = config_file_parser(args)
    if isinstance(args.initialization, str):
        args.initialization = json.loads(args.initialization)
    if isinstance(args.excitement, str):
        args.excitement = json.loads(args.excitement)
    main(args)

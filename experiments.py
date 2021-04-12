from argparse import Namespace

import itertools
import tqdm

from main import main, parser

if __name__ == "__main__":
    dist = [
        [0, 0.5, 1],
        [1, 5, 10],
    ]
    values = [0.5, 1, 10]
    parameters = [
        [2, 5, 10],  # ('size',
        [5, 10],  # ('horizon',
        [{'name': 'gaussian', 'mean': mean, 'var': var}
            for mean, var in itertools.product(*dist)],  # ('initialization',
        [{'name': 'constant', 'value': value}
            for value in values],  # ('excitement',
        # [{'name': 'gaussian', 'mean': mean, 'var': var}
        #     for mean, var in itertools.product(*dist)],  # ('excitement',
        ['match'],  # ('update',
    ]
    parameters = list(itertools.product(*parameters))
    for i, params in enumerate(tqdm.tqdm(parameters, desc='EXP')):
        args = {
            'size': params[0],
            'horizon': params[1],
            'initialization': params[2],
            'excitement': params[3],
            'update': params[4],
            'debug': False,
            'seed': 1000,
            'matching': 'BFSM',
            'print': False,
            'output': 'outputs',
        }
        main(Namespace(**args))

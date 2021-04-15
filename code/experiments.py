from argparse import Namespace

import itertools

import numpy as np
import tqdm

from visualization import plot_tradeoff, plot_tradeoff_hue
from main import main, parser
from agents import Man, Woman

if __name__ == "__main__":
    dist = [
        [20],
        [5],
        # [round(x, 9) for x in np.linspace(10, 30, 5)],
        # [round(x, 9) for x in np.linspace(0, 10, 5)],
    ]
    diste = [
        # [0.1],
        # [0.],
        [round(x, 9) for x in np.linspace(0, 1, 5)],
        [round(x, 9) for x in np.linspace(0, 1, 5)],
    ]
    values = [0.5, 1, 10]
    parameters = [
        [20],  # ('size',
        [10],  # ('horizon',
        [{'name': 'gaussian', 'mean': mean, 'var': var}
            for mean, var in itertools.product(*dist)],  # ('initialization',
        # [{'name': 'constant', 'value': value}
        #     for value in values],  # ('excitement',
        [{'name': 'gaussian', 'mean': mean, 'var': var}
            for mean, var in itertools.product(*diste)],  # ('excitement',
        ['match'],  # ('update',
    ]
    parameters = list(itertools.product(*parameters))
    social_welfares = list()
    consistencies = list()
    names = list()
    for i, params in enumerate(tqdm.tqdm(parameters, desc='EXP')):
        Man.id_counter = 0
        Woman.id_counter = 0
        args = {
            'size': params[0],
            'horizon': params[1],
            'initialization': params[2],
            'excitement': params[3],
            'update': params[4],
            'debug': False,
            'seed': 1000,
            'matching': 'MPDA',
            'print': False,
            'output': 'outputs',
        }
        # print('SIZE', params[0], 'HOR', params[1],
        #       'INIT', params[2], 'EXC', params[3])
        data = main(Namespace(**args))
        # print(data['social_welfare'])
        # print(data['consistency'])
        social_welfares.append(data['social_welfare'])
        consistencies.append(data['consistency'])
        # names.append(
        #     f'Mean{params[2]["mean"]}Var{params[2]["var"]}Mean{params[3]["mean"]}Var{params[3]["var"]}')
        if True:
            names.append(
                f'$\mu$={params[3]["mean"]:.2f}, $\sigma^2$={params[3]["var"]:.2f}')
        else:
            names.append(
                f'$\mu$={params[2]["mean"]:.2f}, $\sigma^2$={params[2]["var"]:.2f}')
        # names.append(
        #     '')
    plot_tradeoff_hue(social_welfares, consistencies,
                      names, annotations_title='Excitements', fpath='figures/mpda_dynamics_excitement.png')

    dist = [
        [round(x, 9) for x in np.linspace(10, 30, 5)],
        [round(x, 9) for x in np.linspace(0, 10, 5)],
    ]
    diste = [
        [0.1],
        [0.],
    ]
    values = [0.5, 1, 10]
    parameters = [
        [20],  # ('size',
        [10],  # ('horizon',
        [{'name': 'gaussian', 'mean': mean, 'var': var}
            for mean, var in itertools.product(*dist)],  # ('initialization',
        # [{'name': 'constant', 'value': value}
        #     for value in values],  # ('excitement',
        [{'name': 'gaussian', 'mean': mean, 'var': var}
            for mean, var in itertools.product(*diste)],  # ('excitement',
        ['match'],  # ('update',
    ]
    parameters = list(itertools.product(*parameters))
    social_welfares = list()
    consistencies = list()
    names = list()
    for i, params in enumerate(tqdm.tqdm(parameters, desc='EXP')):
        Man.id_counter = 0
        Woman.id_counter = 0
        args = {
            'size': params[0],
            'horizon': params[1],
            'initialization': params[2],
            'excitement': params[3],
            'update': params[4],
            'debug': False,
            'seed': 1000,
            'matching': 'MPDA',
            'print': False,
            'output': 'outputs',
        }
        # print('SIZE', params[0], 'HOR', params[1],
        #       'INIT', params[2], 'EXC', params[3])
        data = main(Namespace(**args))
        # print(data['social_welfare'])
        # print(data['consistency'])
        social_welfares.append(data['social_welfare'])
        consistencies.append(data['consistency'])
        # names.append(
        #     f'Mean{params[2]["mean"]}Var{params[2]["var"]}Mean{params[3]["mean"]}Var{params[3]["var"]}')
        if False:
            names.append(
                f'$\mu$={params[3]["mean"]:.2f}, $\sigma^2$={params[3]["var"]:.2f}')
        else:
            names.append(
                f'$\mu$={params[2]["mean"]:.2f}, $\sigma^2$={params[2]["var"]:.2f}')
        # names.append(
        #     '')
    plot_tradeoff_hue(social_welfares, consistencies,
                      names, annotations_title='Excitements', fpath='figures/mpda_dynamics_initliazation.png')
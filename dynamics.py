"""Defines transition models wrt utilities."""
import numpy as np

from typing import List, Dict
from enum import Enum

from agents import Man, Woman


class Dynamics(Enum):
    STATIC = 0

    def __str__(self):
        return self.name


def initialize_utilities_from_array(men: List[Man], women: List[Woman], values: np.ndarray) -> None:
    """Helper function that populates agent utilities with a flattened array."""
    assert(len(values) == 2 * len(men) * len(women))
    count = 0
    for man in men:
        for woman in women:
            man.utilities[woman] = values[count]
            count += 1
            woman.utilities[man] = values[count]
            count += 1


def initialize_utilities_constant(men: List[Man], women: List[Woman], constant: float) -> None:
    utilities_all = np.array([constant] * (2 * len(men) * len(women)))
    initialize_utilities_from_array(men, women, utilities_all)


def initialize_utilities_gaussian(men: List[Man], women: List[Woman], mu: float, sigma: float) -> None:
    utilities_all = np.random.normal(mu, sigma, 2 * len(men) * len(women))
    initialize_utilities_from_array(men, women, utilities_all)


def initialize_utilities_uniform_random(men: List[Man], women: List[Woman], low: float, high: float) -> None:
    utilities_all = np.random.uniform(low, high, 2 * len(men) * len(women))
    initialize_utilities_from_array(men, women, utilities_all)


def update_utilities_with_match(men: List[Man], women: List[Woman]) -> None:
    """Decay the utilities matched couples have for each other, and increase the utilities
        unmatched couples have for each other."""
    for man in men:
        for woman in women:
            if man.match == woman:
                man.utilities[woman] *= max(1, 1 - man.boredom[woman])
                woman.utilities[man] *= max(1, 1 - woman.boredom[man])
            else:
                man.utilities[woman] *= min(1, 1 + man.boredom[woman])
                woman.utilities[man] *= min(1, 1 + woman.boredom[man])


def update_utilities_with_match_decay_only(men: List[Man], women: List[Woman]) -> None:
    """Decay the utilities matched couples have for each other."""
    for agent in [men + women]:
        agent.utilities[agent.match] *= max(1, 1 - agent.boredom[agent.match])


def update_utilities(men: List[Man], women: List[Woman]) -> None:
    """Always multiply the utility with 1 + boredom"""
    for man in men:
        for woman in women:
            man.utilities[woman] *= 1 + man.boredom[woman]
            woman.utilities[man] *= 1 + woman.boredom[man]


def initialize_boredom_from_array(men: List[Man], women: List[Woman], values: np.ndarray) -> None:
    """Helper function that populates agent boredom with a flattened array."""
    assert(len(values) == 2 * len(men) * len(women))
    count = 0
    for man in men:
        for woman in women:
            man.boredom[woman] = values[count]
            count += 1
            woman.boredom[man] = values[count]
            count += 1


def initialize_boredom_constant(men: List[Man], women: List[Woman], constant: float) -> None:
    boredom_all = np.array([constant] * (2 * len(men) * len(women)))
    initialize_boredom_from_array(men, women, boredom_all)


def initialize_boredom_gaussian(men: List[Man], women: List[Woman], mu: float, sigma: float) -> None:
    boredom_all = np.random.normal(mu, sigma, 2 * len(men) * len(women))
    initialize_boredom_from_array(men, women, boredom_all)


def initialize_boredom_uniform_random(men: List[Man], women: List[Woman], low: float, high: float) -> None:
    boredom_all = np.random.uniform(low, high, 2 * len(men) * len(women))
    initialize_boredom_from_array(men, women, boredom_all)
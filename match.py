from typing import List, Tuple
from functools import partial
from enum import Enum
from multiprocessing import Pool

import itertools

import numpy as np

from agents import Man, Woman
from evaluate import compute_social_welfare


class MatchAlgorithms(Enum):
    MPDA = 0
    WPDA = 1
    SEXOPT = 2

    def __str__(self):
        return self.name

def get_num_blocking(men: List[Man], women: List[Woman], pairing: List[Tuple[Man, Woman]]) -> bool:
    for i in range(len(pairing)):
        for j in range(i+1, len(pairing)):
            m1, w1 = pairing[i]
            m2, w2 = pairing[j]
            if m1.utilities[w2] > m1.utilities[w1] and w2.utilities[m1] > w2.utilities[m2]:
                return False
            if w1.utilities[m2] > w1.utilities[m1] and m2.utilities[w1] > m2.utilities[w2]:
                return False
    return True
    # blocking = list()
    
    # for paired_man, paired_woman in pairing:
    #     for man in men:
    #         if man == paired_man:
    #             continue
    #         for m, w in pairing:
    #             if m == man:
    #                 other_woman = w
    #                 break
    #             if paired_woman.utilities[man] > paired_woman.utilities[woman] and \
    #                 man.utilities[paired_woman] > man.utilities[other_woman]:
    #                 return False

        #     blocking.append(
        #         np.greater(paired_woman.utilities[man],
        #                     paired_woman.utilities[paired_man])
        #         and
        #         np.greater(man.utilities[paired_woman],
        #                     man.utilities[other_woman]))
        # for woman in women:
        #     if woman == paired_woman:
        #         continue
        #     for m, w in pairing:
        #         if w == woman:
        #             other_man = m
        #             break
        #     blocking.append(
        #         np.greater(paired_man.utilities[woman],
        #                     paired_man.utilities[paired_woman])
        #         and
        #         np.greater(woman.utilities[paired_man],
        #                     woman.utilities[other_man]))
    # return np.sum(np.array(blocking) == True)
    

def get_stable_pairs(men: List[Man], women: List[Woman], pairings: List[List[Tuple[Man, Woman]]]) -> List[List[Tuple[Man, Woman]]]:
    pool = Pool(20)
    fn = partial(get_num_blocking, men, women)
    num_blocking_all = pool.map(fn, pairings)
    num_blocking_all = np.array(num_blocking_all)
    # inds = np.where(num_blocking_all == np.min(num_blocking_all))[0]
    inds = np.where(num_blocking_all)[0]
    stable_pairs = list()
    for idx in inds:
        stable_pairs.append(pairings[idx])

    return stable_pairs


def get_all_pairs(men: List[Man], women: List[Woman]) -> List[List[Tuple[Man, Woman]]]:
    # all pairings have the same ordering of women
    pairings = [list(zip(perm, women)) for
                perm in itertools.permutations(men, len(women))]
    return pairings


def brute_force(men: List[Man], women: List[Woman],
                method='welfare-optimal') -> List[Tuple[Man, Woman]]:
    # print("Computing brute force pairs")
    # pairings = [
    #     (list(zip(perm, women)),
    #      sum([man.utilities[woman] + woman.utilities[man]
    #           for man, woman in list(zip(perm, women))])) for
    #     perm in itertools.permutations(men, len(women))]
    pairings = get_all_pairs(men, women)

    def get_welfare_optimal_paring(pairings: List[List[Tuple[Man, Woman]]]
                                   ) -> List[Tuple[Man, Woman]]:
        best_welfare = -1
        best_pairing = None
        for pairing in pairings:
            welfare = compute_social_welfare(pairing)
            if np.greater(welfare, best_welfare):
                best_welfare = welfare
                best_pairing = pairing
        return best_pairing

    if method == 'welfare-optimal':
        pairing = get_welfare_optimal_paring(pairings)
        for pair in pairing:
            pair[0].match = pair[1]
            pair[1].match = pair[0]
        return pairing
    elif method == 'stable-matching':
        stable_pairs = get_stable_pairs(men, women, pairings)
        pairing = get_welfare_optimal_paring(stable_pairs)
        for pair in pairing:
            pair[0].match = pair[1]
            pair[1].match = pair[0]
        return pairing
    else:
        raise ValueError("Unkown brute force method")


def deferred_acceptance(men: List[Man], women: List[Woman],
                        method='MPDA') -> List[Tuple[Man, Woman]]:
    """
    The deferred accptance algorithm for stable matching
    inputs:
        @men: list of Man objects. Must be length N
        @women: list of Woman objects. Must be length N
        @method: string, one of ['MPDA', 'WPDA'].
    returns:
        @pairs: list of (Man, Woman) tuples indicating pairs
    """
    if method not in ['MPDA', 'WPDA']:
        raise ValueError('Unknown method: must be MPDA or WPDA')
    N = len(men)
    if N == 0:
        raise ValueError('Men list is empty')
    if len(women) == 0:
        raise ValueError('Women list is empty')
    if N != len(women):
        raise ValueError("Men and women list don't match length")
    proposers = men if method == 'MPDA' else women
    proposed_to = women if method == 'MPDA' else men
    unmatched = list(range(len(proposers)))
    for agent in proposers + proposed_to:
        agent.match = None
    while unmatched:
        idx = unmatched[0]
        incr = 0
        while proposers[idx].match is None and incr < N:
            spouse_idx = proposed_to.index(proposers[idx].preferences[incr])
            if proposed_to[spouse_idx].match is None:
                proposed_to[spouse_idx].match = proposers[idx]
                proposers[idx].match = proposed_to[spouse_idx]
                unmatched.pop(0)
            elif proposed_to[spouse_idx].prefers(proposers[idx]):
                proposed_to[spouse_idx].match.match = None
                unmatched.append(proposers.index(
                    proposed_to[spouse_idx].match))
                proposed_to[spouse_idx].match = proposers[idx]
                proposers[idx].match = proposed_to[spouse_idx]
                unmatched.pop(0)
            incr += 1
    if any([x.match is None for x in proposers + proposed_to]):
        for agent in proposers + proposed_to:
            print(f"{agent}, {agent.match}")
        raise RuntimeError(
            "Someone is unmatched.")
    matchings_1 = sorted([(x, x.match) for x in proposers])
    matchings_2 = sorted([(x.match, x) for x in proposed_to])
    if matchings_1 != matchings_2:
        raise RuntimeError(
            "Something went horribly wrong. Matchings don't match")
    return matchings_1


def sex_optimal(men: List[Man], women: List[Woman]) -> List[Tuple[Man, Woman]]:
    pass


MPDA = partial(deferred_acceptance, method='MPDA')
WPDA = partial(deferred_acceptance, method='WPDA')
BFWO = partial(brute_force, method='welfare-optimal')
BFSM = partial(brute_force, method='stable-matching')

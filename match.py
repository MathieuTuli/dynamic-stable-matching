from typing import List, Tuple
from functools import partial
from enum import Enum


from agents import Man, Woman


class MatchAlgorithms(Enum):
    MPDA: 0
    WPDA: 1
    SEXOPT: 2

    def __str__(self):
        return self.name


def deferred_acceptance(men: List[Man], women: List[Woman],
                        method='MPDA') -> List[Tuple[Man, Woman]]:
    if method not in ['MPDA', 'WPDA']:
        raise ValueError('Unknown method: must be MPDA or WPDA')
    if len(men) == 0:
        raise ValueError('Men list is empty')
    if len(women) == 0:
        raise ValueError('Women list is empty')
    if len(men) != len(women):
        raise ValueError("Men and women list don't match length")
    proposers = men if method == 'MPDA' else women
    proposed_to = women if method == 'MPDA' else men
    unmatched = list(range(len(proposers)))
    while unmatched:
        idx = unmatched[0]
        incr = 0
        while proposers[idx].match is None:
            spouse_idx = proposed_to.index(proposers[idx].preferences()[incr])
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

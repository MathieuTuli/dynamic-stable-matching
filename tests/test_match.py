import random
import sys

import pytest

from src.match import deferred_acceptance
from src.agents import Man, Woman
from .support import fail_if


def test_deferred_accptance():
    try:
        deferred_acceptance([], [])
        deferred_acceptance([None, None], [None])
        deferred_acceptance([None], [None, None])
        pytest.fail()
    except ValueError:
        pass
    _test_mpda()
    _test_wpda()


def _test_mpda() -> None:
    men = [Man(), Man(), Man()]
    women = [Woman(), Woman(), Woman()]
    incr = 0
    for man in men:
        incr_2 = 0
        for woman in women:
            if woman.utilities is None:
                woman.utilities = dict()
            if man.utilities is None:
                man.utilities = dict()
            woman.utilities[man] = incr
            man.utilities[woman] = incr_2
            incr_2 += 1
        incr += 1
    for man in men:
        print(f"{man}, {[str(x) for x in man.preferences()]}")
    for woman in women:
        print(f"{woman}, {[str(x) for x in woman.preferences()]}")
    try:
        matchings = deferred_acceptance(men, women, method='WPDA')
        fail_if(men[0].match != women[2])
        fail_if(men[1].match != women[1])
        fail_if(men[2].match != women[0])
    except Exception as e:
        print(e)
        pytest.fail()

    for match in matchings:
        print(f"{match[0]}, {match[1]}")


def _test_wpda() -> None:
    men = [Man(), Man(), Man()]
    women = [Woman(), Woman(), Woman()]
    incr = 0
    for man in men:
        incr_2 = 0
        for woman in women:
            if woman.utilities is None:
                woman.utilities = dict()
            if man.utilities is None:
                man.utilities = dict()
            woman.utilities[man] = incr
            man.utilities[woman] = incr_2
            incr_2 += 1
        incr += 1
    for man in men:
        print(f"{man}, {[str(x) for x in man.preferences()]}")
    for woman in women:
        print(f"{woman}, {[str(x) for x in woman.preferences()]}")
    try:
        matchings = deferred_acceptance(men, women, method='WPDA')
        fail_if(men[0].match != women[2])
        fail_if(men[1].match != women[1])
        fail_if(men[2].match != women[0])
    except Exception as e:
        print(e)
        pytest.fail()
    for match in matchings:
        print(f"{match[0]}, {match[1]}")

import random
import sys

import pytest

from match import deferred_acceptance
from agents import Man, Woman
from support import fail_if


def test_deferred_accptance():
    try:
        deferred_acceptance([], [])
        deferred_acceptance([None, None], [None])
        deferred_acceptance([None], [None, None])
        pytest.fail()
    except ValueError:
        pass
    # _test_mpda()
    # _test_wpda()
    _test_mpda_class()


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
        print(f'{[str(x) for x in man.preferences]}')
    for woman in women:
        print(f'{[str(x) for x in woman.preferences]}')
    try:
        matchings = deferred_acceptance(men, women, method='WPDA')
        print("MPDA: results:")
        for match in matchings:
            print(f"{match[0]}, {match[1]}")
        fail_if(men[0].match != women[0])
        fail_if(men[1].match != women[1])
        fail_if(men[2].match != women[2])
    except Exception as e:
        print(e)
        pytest.fail()


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
        print(f'{[str(x) for x in man.preferences]}')
    for woman in women:
        print(f'{[str(x) for x in woman.preferences]}')
    try:
        matchings = deferred_acceptance(men, women, method='WPDA')
        print("WPDA: results:")
        for match in matchings:
            print(f"{match[0]}, {match[1]}")
        fail_if(men[0].match != women[0])
        fail_if(men[1].match != women[1])
        fail_if(men[2].match != women[2])
    except Exception as e:
        print(e)
        pytest.fail()


def _test_mpda_class() -> None:
    men = [Man(), Man(), Man()]
    women = [Woman(), Woman(), Woman()]
    men[0].utilities = {women[0]: 2, women[1]: 1, women[2]: 0}
    men[1].utilities = {women[1]: 2, women[0]: 1, women[2]: 0}
    men[2].utilities = {women[0]: 2, women[1]: 1, women[2]: 0}
    women[0].utilities = {men[1]: 2, men[0]: 1, men[2]: 0}
    women[1].utilities = {men[0]: 2, men[1]: 1, men[2]: 0}
    women[2].utilities = {men[0]: 2, men[1]: 1, men[2]: 0}
    for man in men:
        print(f'{[str(x) for x in man.preferences]}')
    for woman in women:
        print(f'{[str(x) for x in woman.preferences]}')
    fail_if(men[0].preferences != [women[0], women[1], women[2]])
    fail_if(men[1].preferences != [women[1], women[0], women[2]])
    fail_if(men[2].preferences != [women[0], women[1], women[2]])
    try:
        matchings = deferred_acceptance(men, women, method='MPDA')
        print("Class: results:")
        for match in matchings:
            print(f"{match[0]}, {match[1]}")
        fail_if(men[0].match != women[0])
        fail_if(men[1].match != women[1])
        fail_if(men[2].match != women[2])
        fail_if(women[0].match != men[0])
        fail_if(women[1].match != men[1])
        fail_if(women[2].match != men[2])
    except Exception as e:
        print(e)
        pytest.fail()

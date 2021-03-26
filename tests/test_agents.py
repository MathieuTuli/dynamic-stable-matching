import pytest

from agents import Man, Woman
from support import fail_if


def test_attributes() -> None:
    man1 = Man()
    man2 = Man()
    fail_if(man1 != man1)
    fail_if(man2 != man2)
    fail_if((man1 > man2) is not False)
    fail_if((man1 >= man2) is not False)
    fail_if((man1 >= man1) is not True)
    fail_if((man1 < man2) is not True)
    fail_if((man1 <= man2) is not True)
    fail_if((man1 <= man1) is not True)
    try:
        man2.prefers(man1)
        pytest.fail()
    except RuntimeError:
        pass


def test_preferences() -> None:
    men = [Man(), Man(), Man()]
    women = [Woman(), Woman(), Woman()]
    men[0].utilities = {women[0]: 0, women[1]: 1, women[2]: 2}
    men[1].utilities = {women[0]: 2, women[1]: 0, women[2]: 2}
    men[2].utilities = {women[0]: 2, women[1]: 1, women[2]: 0}
    women[0].utilities = {men[0]: 0, men[1]: 1, men[2]: 2}
    women[1].utilities = {men[0]: 0, men[1]: 1, men[2]: 2}
    women[2].utilities = {men[0]: 0, men[1]: 1, men[2]: 2}
    for man in men:
        print(f'{[str(x) for x in man.preferences]}')
    for woman in women:
        print(f'{[str(x) for x in woman.preferences]}')
    fail_if(men[0].preferences != [women[2], women[1], women[0]])
    fail_if(men[1].preferences != [women[0], women[2], women[1]])
    fail_if(men[2].preferences != [women[0], women[1], women[2]])

    print("\nReset\n")
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


def test_change_utilities() -> None:
    man = Man()
    man.utilities = {1: 1, 2: 2, 3: 3, 4: 4}
    fail_if(man.preferences != [4, 3, 2, 1])
    print(man.preferences)
    man.utilities = {1: 4, 2: 3, 3: 2, 4: 1}
    print(man.preferences)
    fail_if(man.preferences != [1, 2, 3, 4])
    fail_if(man.preferences == [4, 3, 2, 1])

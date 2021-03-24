import random
from match import deferred_acceptance
from agents import Man, Woman


men = [Man(), Man(), Man()]
women = [Woman(), Woman(), Woman()]
for man in men:
    for woman in women:
        if woman.utilities is None:
            woman.utilities = dict()
        if man.utilities is None:
            man.utilities = dict()
        woman.utilities[man] = random.randint(0, 100)
        man.utilities[woman] = random.randint(0, 100)
for man in men:
    print(f"{man}, {[str(x) for x in man.preferences()]}")
for woman in women:
    print(f"{woman}, {[str(x) for x in woman.preferences()]}")
matchings = deferred_acceptance(men, women)
for match in matchings:
    print(f"{match[0]}, {match[1]}")

for man in men:
    man.match = None
for man in women:
    man.match = None
matchings = deferred_acceptance(men, women, method='WPDA')
for match in matchings:
    print(f"{match[0]}, {match[1]}")

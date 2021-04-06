"""Defines the agent class."""
from __future__ import annotations
from typing import List, Dict
from functools import lru_cache

import numpy as np


class Utilities(dict):
    @property
    @lru_cache()
    def preferences(self) -> List[Agent]:
        return [k for k, v in sorted(self.items(),
                                     key=lambda x: x[1], reverse=True)]

    def __hash__(self) -> int:
        return hash(str(self))

    def __setitem__(self, key: Agent, value: float):
        super().__setitem__(key, value)
        type(self).preferences.fget.cache_clear()


class Agent:
    id_counter: int = 0

    def __init__(self) -> None:
        self.__utilities: Utilities = Utilities()
        self.excitement: Dict[Agent, float] = {}
        self.match: Agent = None

    def __str__(self) -> str:
        return f"{self.__class__.__name__}-{self.id}"

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: Agent) -> bool:
        return self.id == other.id

    def __gt__(self, other: Agent) -> bool:
        return self.id > other.id

    def __ge__(self, other: Agent) -> bool:
        return self.id >= other.id

    def __lt__(self, other: Agent) -> bool:
        return self.id < other.id

    def __le__(self, other: Agent) -> bool:
        return self.id <= other.id

    @property
    def utilities(self) -> Utilities:
        return self.__utilities

    @utilities.setter
    def utilities(self, value: Dict[Agent, float]) -> Utilities:
        self.__utilities = Utilities(value)

    def normalize_utilities(self) -> None:
        utilities_sum = np.sum(list(self.__utilities.values()))
        for agent, value in self.__utilities.items():
            self.__utilities[agent] = value / utilities_sum

    @property
    def preferences(self) -> List[Agent]:
        return self.__utilities.preferences

    def prefers(self, other: Agent) -> bool:
        if self.match is None:
            raise RuntimeError("Attempting to check if someone else is " +
                               "preferred when no match exists")
        # note a smaller index means better
        return self.preferences.index(other) < \
            self.preferences.index(self.match)


class Man(Agent):
    def __init__(self) -> None:
        super(Man, self).__init__()
        self.id = Man.id_counter
        Man.id_counter += 1


class Woman(Agent):
    def __init__(self) -> None:
        super(Woman, self).__init__()
        self.id = Woman.id_counter
        Woman.id_counter += 1

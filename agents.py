"""Defines the agent class."""
from __future__ import annotations
from typing import List, Dict
from functools import lru_cache


class Agent:
    id: int = None
    id_counter: int = 0
    _utilities: Dict[Agent, float] = None
    match: Agent = None
    _next: int = 0

    def __str__(self) -> str:
        return f"{self.__class__.__name__}-{self.id}"

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: Agent) -> bool:
        return self.id == other.id

    def __gt__(self, other: Agent) -> bool:
        return self.id < other.id

    def __geq__(self, other: Agent) -> bool:
        return self.id <= other.id

    def __lt__(self, other: Agent) -> bool:
        return self.id > other.id

    def __leq__(self, other: Agent) -> bool:
        return self.id >= other.id

    @property
    def next(self) -> int:
        ret = self._next
        self._next += 1
        return ret

    @next.setter
    def next(self, value: int) -> None:
        self._next = value

    @property
    def utilities(self) -> Dict[Agent, float]:
        return self._utilities

    @utilities.setter
    def utilities(self, value: Dict[Agent, float]) -> None:
        self._utilities = value
        type(self).preferences.fget.cache_clear()

    @property
    @lru_cache
    def preferences(self) -> List[Agent]:
        return [k for k, v in sorted(self.utilities.items(),
                                     key=lambda x: x[1], reverse=True)]

    def prefers(self, other: Agent) -> bool:
        if self.match is None:
            raise RuntimeError("Attempting to check if someone else is " +
                               "preferred when no match exists")
        return self.preferences.index(other) > \
            self.preferences.index(self.match)


class Man(Agent):
    def __init__(self) -> None:
        self.id = Man.id_counter
        Man.id_counter += 1


class Woman(Agent):
    def __init__(self) -> None:
        self.id = Woman.id_counter
        Woman.id_counter += 1

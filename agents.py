"""Defines the agent class."""
from __future__ import annotations
from typing import List, Tuple, Dict


class Agent:
    id: int = None
    id_counter: int = 0
    utilities: Dict[Agent, float] = None
    match: Agent = None

    def __str__(self) -> str:
        return f"{self.__class__.__name__}-{self.id}"

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

    # TODO not efficient
    def preferences(self) -> List[Agent]:
        return [k for k, v in sorted(self.utilities.items(),
                                     key=lambda x: x[1], reverse=True)]

    def prefers(self, other: Agent) -> bool:
        if self.match is None:
            raise RuntimeError("Attempting to check if someone else is " +
                               "preferred when no match exists")
        prefs = self.preferences()
        return prefs.index(other) > prefs.index(self.match)

    def __hash__(self) -> int:
        return hash(str(self))


class Man(Agent):
    def __init__(self) -> None:
        self.id = Man.id_counter
        Man.id_counter += 1


class Woman(Agent):
    def __init__(self) -> None:
        self.id = Woman.id_counter
        Woman.id_counter += 1

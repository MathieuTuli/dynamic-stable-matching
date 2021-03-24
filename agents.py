"""Defines the agent class."""
from __future__ import annotations
from typing import List


class Agent:
    id: int = None
    utilities: List[Agent] = None
    match: Agent = None

    def __str__(self) -> str:
        return f"{self.__class__.__name__}-{self.id}"

    def __eq__(self, other: Agent) -> bool:
        return self.id == other.id


class Man(Agent):
    id_counter: int = 0

    def __init__(self) -> None:
        super(Man, self).__init__()
        self.id = Man.id_counter
        Man.id_counter += 1


class Woman(Agent):
    id_counter: int = 0

    def __init__(self) -> None:
        super(Woman, self).__init__()
        self.id = Woman.id_counter
        Woman.id_counter += 1

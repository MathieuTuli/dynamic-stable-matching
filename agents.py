"""Defines the agent class."""
from __future__ import annotations
from typing import List


class Agent:
    id: int = None
    id_counter: int = 0
    utilities: List[Agent] = None
    match: Agent = None

    def __str__(self) -> str:
        return f"{self.__class__.__name__}-{self.id}"

    def __eq__(self, other: Agent) -> bool:
        return self.id == other.id


class Man(Agent):
    def __init__(self) -> None:
        self.id = Man.id_counter
        Man.id_counter += 1


class Woman(Agent):
    def __init__(self) -> None:
        self.id = Woman.id_counter
        Woman.id_counter += 1

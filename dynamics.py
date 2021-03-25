"""Defines transition models wrt utilities."""
from typing import List
from enum import Enum

from .agents import Man, Woman


class Dynamics(Enum):
    STATIC: 0

    def __str__(self):
        return self.name


def initialize_utilities(men: List[Man], women: List[Woman]) -> None:
    pass


def decay(men: List[Man], women: List[Woman]) -> None:
    """Update the respective utilities"""
    pass

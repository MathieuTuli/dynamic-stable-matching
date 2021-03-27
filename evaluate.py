from typing import List, Tuple
from collections import defaultdict

from agents import Man, Woman


class Evaluator():
    n: int = None
    _history_dict: defaultdict[Tuple[int, int], List[int]] = defaultdict(list)
    _next_timestep_unaggregated: int = 0

    def __init__(self, num_agents):
        self.n = num_agents

    def aggregate(self, history: List[List[Tuple[Man, Woman]]]) -> None:
        """
        aggregate the matchingt history to __history_dict
        inputs:
            @histroy: list of matched pairs at each timestep
        """
        if len(history) >= Evaluator._next_timestep_unaggregated:
            for matches in history[Evaluator._next_timestep_unaggregated:]:
                for index, (man, woman) in enumerate(matches):
                    Evaluator._history_dict[(man.id, woman.id)].append(
                        index+Evaluator._next_timestep_unaggregated)

            Evaluator._next_timestep_unaggregated = len(history)

    def evaluate_average(self, history: List[List[Tuple[Man, Woman]]]) -> float:
        """
        Evaluating the consistency of matched pairs across timesteps
        inputs:
            @history: list of matched pairs at each timestep
        returns:
            @consistency: float indicating the average of number of timesteps
                        perserved for each match;
        """

        self.aggregate(history)

        num_match = 0
        for pair, timesteps in Evaluator._history_dict:
            cur_timestep = -2
            for timestep in timesteps:
                if timestep != cur_timestep+1:
                    num_match += 1
                cur_timestep = timestep

        total_timesteps = Evaluator.n/2 * len(history)
        return total_timesteps/num_match

    def evaluate_longest(self, history: List[List[Tuple[Man, Woman]]]) -> float:
        """
        Evaluating the consistency of matched pairs across timesteps
        inputs:
            @history: list of matched pairs at each timestep
        returns:
            @consistency: float indicating the average of number of timesteps
                        perserved for each match;
        """

        self.aggregate(history)

        longest = 1
        cur = 1
        for pair, timesteps in Evaluator._history_dict:
            for timestep in timesteps:
                if timestep == cur_timestep+1:
                    cur += 1
                else:
                    if cur > longest:
                        longest = cur
                    cur = 1
            if cur > longest:
                longest = cur
            cur = 1

        return longest

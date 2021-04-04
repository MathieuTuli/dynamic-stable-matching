from typing import List, Tuple
from collections import defaultdict


class Evaluator():
    def __init__(self, num_agents):
        self.history_dict: defaultdict[Tuple[int, int], List[int]] = \
            defaultdict(list)
        self.next_timestep_unaggregated = 0
        self.n = num_agents  # number of total agents, both men and women

    def aggregate(self, history: List[List[Tuple[int, int]]]) -> None:
        """
        aggregate the matchingt history to __history_dict
        inputs:
            @history: list of matched pairs at each timestep
        """
        if len(history) >= self.next_timestep_unaggregated:
            for matches in history[self.next_timestep_unaggregated:]:
                for index, (man_id, woman_id) in enumerate(matches):
                    self.history_dict[(man_id, woman_id)].append(
                        self.next_timestep_unaggregated)

            self.next_timestep_unaggregated = len(history)

    def evaluate_average(self,
                         history: List[List[Tuple[int, int]]]) -> float:
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
        for timestep in self.history_dict.values():
            cur_timestep = -2
            for timestep in timestep:
                if timestep != cur_timestep+1:
                    num_match += 1
                cur_timestep = timestep

        total_timesteps = self.n/2 * len(history)
        return float(total_timesteps)/num_match

    def evaluate_longest(self,
                         history: List[List[Tuple[int, int]]]) -> float:
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
        for timesteps in self.history_dict.values():
            cur_timestep = -2
            for timestep in timesteps:
                if timestep == cur_timestep+1:
                    cur += 1
                else:
                    if cur > longest:
                        longest = cur
                    cur = 1
                cur_timestep = timestep
            if cur > longest:
                longest = cur
            cur = 1

        return longest

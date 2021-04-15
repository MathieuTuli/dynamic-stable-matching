from typing import List, Tuple
from collections import defaultdict

import numpy as np

from agents import Man, Woman


class Evaluator():
    def __init__(self, num_agents):
        self.history_dict: defaultdict[Tuple[int, int], List[int]] = \
            defaultdict(list)
        self.next_timestep_unaggregated = 0
        self.n = num_agents  # number of total agents, both men and women

    def aggregate(self, history: List[List[Tuple[int, int]]]) -> None:
        """
        aggregate the matching history to __history_dict
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

        total_timesteps = self.n * len(history)
        return float(total_timesteps)/num_match

    def evaluate_longest(self,
                         history: List[List[Tuple[int, int]]]) -> float:
        """
        Evaluating the consistency of matched pairs across timesteps
        inputs:
            @history: list of matched pairs at each timestep
        returns:
            @consistency: float indicating the largest number of timesteps
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

    def evaluate_consistency_rate(self,
                                  history: List[List[Tuple[int, int]]]) -> List[float]:
        """
        Evaluating the consistency of matched pairs across timesteps
        inputs:
            @history: list of matched pairs at each timestep
        returns:
            @consistency: list of float indicating proportion of marriage
                          that stay consistent with last timestep;
        """

        prev_matches = history[0]
        consistency_rate = [0]
        count = 0
        num_pairs = len(prev_matches)
        for matches in history[1:]:
            for match in matches:
                if (match in prev_matches):
                    count += 1
            consistency_rate.append(count/num_pairs)
            count = 0
            prev_matches = matches
        return consistency_rate


def compute_social_welfare(pairing: List[Tuple[Man, Woman]]) -> float:
    welfare = np.mean([man.utilities[woman] + woman.utilities[man]
                       for man, woman in pairing])
    return welfare / 2


def compute_consistency(p1: List[Tuple[Man, Woman]], p2: List[Tuple[Man, Woman]]) -> float:
    # we assume women in m1 and m2 have the same ordering
    consistent_pairs = 0
    for (m1, w1), (m2, w2) in zip(p1, p2):
        assert w1.id == w2.id
        if m1.id == m2.id:
            consistent_pairs += 1
    return consistent_pairs * 1.0 / len(p1)

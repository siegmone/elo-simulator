from typing import List, Tuple
from simulation.player import Player

from enum import Enum, auto


class PairingMode(Enum):
    ROUND_ROBIN = auto()
    SWISS = auto()


class RoundRobinSchedule:
    def __init__(self, players: List[Player]):
        self.matches = []
        n = len(players)
        for i in range(n - 1):
            for j in range(i + 1, n):
                self.matches.append((players[i], players[j]))

    def __iter__(self):
        return iter(self.matches)


class SwissSchedule:
    def __init__(self, players: List[Player]):
        self.matches = []
        for i in range(0, len(players) - 1, 2):
            self.matches.append((players[i], players[i + 1]))

    def __iter__(self):
        return iter(self.matches)

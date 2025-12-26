from typing import List, Tuple
from simulation.player import Player


class RoundRobinSchedule:
    def __init__(self, players: list[Player]):
        self.matches = list(self.round_robin(players))

    def __iter__(self):
        return iter(self.matches)

    def round_robin(self, players: List[Player]) -> List[Tuple[Player, Player]]:
        pairings = []
        n = len(players)
        for i in range(n - 1):
            for j in range(i + 1, n):
                pairings.append((players[i], players[j]))
        return pairings

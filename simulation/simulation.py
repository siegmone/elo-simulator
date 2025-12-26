import random
import uuid
import numpy as np
import copy
from typing import List, Dict, Tuple
from .player import Player
from .elo import delta_elo, expected_score
from .pairings import RoundRobinSchedule


AVERAGE_ELO = 1000
DEFAULT_K = 10
DEFAULT_ALPHA = 100
DEFAULT_LUCK = 0.05
DEFAULT_SEED = 42


class MatchEngine:
    def __init__(self, k: float, alpha: float, luck: float, rng: random.Random):
        self.k: float = k
        self.alpha: float = alpha
        self.luck = luck
        self.rng = rng

    def play(self, p1: Player, p2: Player) -> Tuple[float, float]:
        e_1, e_2 = expected_score(p1.elo, p2.elo, self.alpha)

        # elo_based skill effect + luck
        luck = self.rng.uniform(-self.luck / 2, self.luck / 2)
        skill_gap = (p1.skill - p2.skill) / p2.skill
        chance = e_1 + luck + skill_gap
        chance = max(min(chance, 1.0), 0.0)
        s_1 = int(self.rng.random() < chance)
        s_2 = 1 - s_1

        return (
            delta_elo(e_1, s_1, self.k, self.alpha),
            delta_elo(e_2, s_2, self.k, self.alpha),
        )


class Simulation:
    def __init__(self, players: List[Player], engine: MatchEngine):
        self.start_players = copy.deepcopy(players)
        self.players = players
        self.engine = engine
        self.round: int = 0
        self.history: Dict[str, List[Tuple[int, float]]] = {
            p.name: [(self.round, p.elo)] for p in self.players
        }
        self.schedule = RoundRobinSchedule(self.players)
        self.avg_elo = np.mean([p.elo for p in self.players])

    def add_player(self, player_name: str):
        avg_elo = np.mean([p.elo for p in self.players])
        while player_name in self.history:
            player_name += str(random.randint(0, 9))

        p = Player(
                player_name,
                elo=avg_elo,
                skill=50,
            )
        self.players.append(p)
        self.history[p.name] = [(self.round, p.elo)]
        self.schedule = RoundRobinSchedule(self.players)

    def reset(self):
        self.engine.rng = random.Random(DEFAULT_SEED)
        self.round = 0
        self.players = copy.deepcopy(self.start_players)
        self.history: Dict[str, List[Tuple[int, float]]] = {
            p.name: [(self.round, p.elo)] for p in self.players
        }
        self.schedule = RoundRobinSchedule(self.players)

    def set_k(self, k: float):
        self.engine.k = k

    def set_alpha(self, alpha: float):
        self.engine.alpha = alpha

    def _snapshot(self):
        for p in self.players:
            self.history[p.name].append((self.round, p.elo))

    def simulate_rounds(self, n_rounds: int):
        for _ in range(n_rounds):
            self.step_round()

    def step_round(self):
        for p1, p2 in self.schedule:
            d1, d2 = self.engine.play(p1, p2)
            p1.delta += d1
            p2.delta += d2
        self.round += 1
        for p in self.players:
            p.update_elo()
        self._snapshot()
        self.update_history()
        self.avg_elo = np.mean([p.elo for p in self.players])

    def update_history(self):
        for p in self.players:
            self.history[p.name].append((self.round, p.elo))

    def rankings(self) -> List[Player]:
        return sorted(
            self.players,
            key=lambda x: x.elo,
            reverse=True,
        )

    def get_history(self) -> Dict[str, List[Tuple[int, float]]]:
        return self.history

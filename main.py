#! .venv/bin/python

# def main() -> None:
# alpha = 100
# k = 10

# players = [
#     Player("Ugo", 100, 115),
#     Player("Carmine", 100, 115),
#     Player("Francesco R.", 95, 110),
#     Player("Daniele Ambrosino", 80, 105),
#     Player("Simone I.", 80, 100),
#     Player("Raffaele", 75, 100),
#     Player("Ciro", 70, 95),
#     Player("Mario", 70, 95),
#     Player("Alfonso", 69, 95),
#     Player("Davide", 65, 95),
#     Player("Francesco L.", 50, 85),
#     Player("Simone M.", 30, 85),
# ]

# ranking_history: Dict[str, List[float]] = {}
# for player in players:
#     ranking_history[player.name] = [player.elo]

# n_rounds = 100

# print("Ranking")
# width = max(len(player.name) for player in players)
# for player in players:
#     print(f"{player.name:<{width}} : {player.elo:.2f}")

# for i in range(n_rounds):
#     for player_a, player_b in round_robin(players):
#         r_a = player_a.elo
#         r_b = player_b.elo
#         e_a, e_b = elo_expected_score(r_a, r_b, alpha)

#         # just elo
#         s_a = e_a
#         s_b = 1 - s_a

#         # elo_based skill effect + luck
#         luck_value = 0.1
#         luck = random.uniform(-luck_value / 2, luck_value / 2)
#         skill_gap = (player_a.skill - player_b.skill) / player_b.skill
#         chance = e_a + luck
#         chance = max(min(chance, 1.0), 0.0)
#         s_a = int(random.random() < chance)
#         s_b = 1 - s_a

#         # 50/50 pure luck
#         # s_a = 0.5
#         # s_b = 1 - s_a

#         elo_a = elo(r_a, e_a, s_a, k, alpha)
#         elo_b = elo(r_b, e_b, s_b, k, alpha)
#         player_a.elo = elo_a
#         player_b.elo = elo_b
#         ranking_history[player_a.name].append(elo_a)
#         ranking_history[player_b.name].append(elo_b)

# print()
# print("Ranking")
# width = max(len(player.name) for player in players)
# for player in players:
#     print(f"{player.name:<{width}} : {player.elo:.2f}")

# elos_array = np.array(list(ranking_history.values()))
# mean_elos = np.mean(elos_array, axis=0)

# plt.style.use('seaborn-v0_8-colorblind')
# fig, ax = plt.subplots(figsize=(13, 9))

# for name, values in ranking_history.items():
#     ax.plot(values, label=name, lw=2, ls="solid", alpha=0.7)
# ax.plot(mean_elos,  lw=4, color="black", label="Mean Elo")

# print(mean_elos[0])
# print(mean_elos[-1])

# ax.set_title(f"Ranking Simulation {k=:.0f}, {alpha=:.0f}")
# ax.grid(linestyle='--', alpha=0.7)
# ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
# plt.tight_layout()
# plt.show()

from app.app import App

if __name__ == "__main__":
    app = App(1920, 1080)
    app.run()

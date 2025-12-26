import random

import dearpygui.dearpygui as dpg

from simulation.simulation import Simulation, MatchEngine, DEFAULT_SEED, DEFAULT_ALPHA, DEFAULT_K
from simulation.player import Player
from simulation.pairings import PairingMode


players = [
    # Player("p1", 100, 100),
    # Player("p2", 90, 100),
    # Player("p3", 80, 100),
    # Player("p4", 70, 100),
    # Player("p5", 60, 100),
    # Player("p6", 50, 100),
    # Player("p7", 40, 100),
    # Player("p8", 30, 100),
    Player(f"p{i}", random.uniform(0, 100), 100) for i in range(100)
]


def update_plot(simulation):
    y_axis_tag = "elo_plot_y_axis"

    for name, history in simulation.get_history().items():
        x = [v[0] for v in history]
        y = [v[1] for v in history]

        tag = f"series_{name}"

        if not dpg.does_item_exist(tag):
            dpg.add_line_series(
                x, y,
                label=name,
                parent=y_axis_tag,
                tag=tag,
            )
        else:
            dpg.set_value(f"series_{name}", [x, y])


def update_rank_table(simulation):
    players = simulation.rankings()
    for i, p in enumerate(players):
        dpg.set_value(f"rank_{i}", f"{i + 1:3d}")
        dpg.set_value(f"name_{i}", p.name)
        dpg.set_value(f"elo_{i}", f"{p.elo:.1f}")
        dpg.set_value(f"delta_{i}", f"{p.last_delta:.1f}")
        if p.last_delta >= 0:
            dpg.bind_item_theme(f"delta_{i}", "green_text")
        else:
            dpg.bind_item_theme(f"delta_{i}", "red_text")

    # Clear unused rows
    for i in range(len(players), 20):
        dpg.set_value(f"rank_{i}", "")
        dpg.set_value(f"name_{i}", "")
        dpg.set_value(f"elo_{i}", "")
        dpg.set_value(f"delta_{i}", "")


class App:
    def __init__(self, width: int, height: int):
        rng = random.Random(DEFAULT_SEED)

        engine = MatchEngine(
            k=DEFAULT_K,
            alpha=DEFAULT_ALPHA,
            luck=0.05,
            rng=rng
        )

        self.sim = Simulation(players, engine)
        self.width = width
        self.height = height
        self.n_rounds = 10
        self.new_player = ""

    def update_display_values(self):
        update_rank_table(self.sim)
        update_plot(self.sim)
        dpg.set_value("avg_elo", f"Average Elo = {self.sim.avg_elo:.1f}")

    def set_new_player(self, sender, app_data, user_data):
        self.new_player = app_data

    def add_player(self, sender, app_data, user_data):
        self.sim.add_player(self.new_player)
        self.update_display_values()

    def on_next_round(self, sender, app_data, user_data):
        self.sim.step_round()
        self.update_display_values()

    def on_simulate_rounds(self, sender, app_data, user_data):
        self.sim.simulate_rounds(self.n_rounds)
        self.update_display_values()

    def get_n_rounds(self, sender, app_data, user_data):
        self.n_rounds = app_data

    def reset_simulation(self, sender, app_data, user_data):
        self.sim.reset()
        self.update_display_values()

    def set_simulation_k(self, sender, app_data, user_data):
        self.sim.set_k(app_data)
        self.reset_simulation(sender, app_data, user_data)
        self.on_simulate_rounds(sender, app_data, user_data)

    def set_simulation_alpha(self, sender, app_data, user_data):
        if app_data <= 0:
            app_data = 1
        self.sim.set_alpha(app_data)
        self.reset_simulation(sender, app_data, user_data)
        self.on_simulate_rounds(sender, app_data, user_data)

    def set_pairing_mode(self, sender, app_data, user_data):
        self.sim.set_pairing_mode(app_data)
        self.reset_simulation(sender, app_data, user_data)
        self.on_simulate_rounds(sender, app_data, user_data)

    def run(self):
        # gui setup
        dpg.create_context()
        dpg.create_viewport(
            title="Elo Simulator",
            width=self.width, height=self.height,
            resizable=False
        )

        # initial simulation
        self.sim.simulate_rounds(self.n_rounds)

        with dpg.theme(tag="green_text"):
            with dpg.theme_component(dpg.mvText):
                dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 255, 0))

        with dpg.theme(tag="red_text"):
            with dpg.theme_component(dpg.mvText):
                dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 0, 0))

        # gui widgets
        with dpg.window(label="Elo Simulator",
                        width=self.width, height=self.height,
                        autosize=True,
                        no_resize=True,
                        no_title_bar=True,
                        no_move=True,
                        no_scrollbar=True,
                        no_collapse=True,
                        no_close=True,
                        no_background=False,
                        modal=False,
                        ) as window:
            dpg.set_item_pos(window, [0, 0])

            padding = 0.01
            with dpg.group(horizontal=True):
                with dpg.child_window(
                    width=0.20 * self.width, resizable_x=True
                ):
                    with dpg.table(tag="ranking_table", header_row=True):
                        dpg.add_table_column(label="Rank")
                        dpg.add_table_column(label="Name")
                        dpg.add_table_column(label="Elo")
                        dpg.add_table_column(label="Delta")

                        for i in range(max(len(players), 100)):  # max players
                            with dpg.table_row(tag=f"rank_row_{i}"):
                                dpg.add_text("", tag=f"rank_{i}")
                                dpg.add_text("", tag=f"name_{i}")
                                dpg.add_text("", tag=f"elo_{i}")
                                dpg.add_text("", tag=f"delta_{i}")

                        for i, p in enumerate(players):
                            dpg.set_value(f"rank_{i}", f"{i + 1:3d}")
                            dpg.set_value(f"name_{i}", p.name)
                            dpg.set_value(f"elo_{i}", f"{p.elo:.1f}")
                            dpg.set_value(f"delta_{i}", f"{0:.1f}")

                with dpg.child_window(
                    width=-0.20 * self.width, resizable_x=True
                ):
                    with dpg.plot(
                        label="Elo Progression",
                        tag="elo_plot_axis",
                        width=-padding * self.width,
                        height=-padding * self.height
                    ) as plot:
                        dpg.set_item_pos(
                            plot, [padding * self.width, padding * self.height]
                        )
                        dpg.add_plot_legend()
                        with dpg.plot_axis(
                            dpg.mvXAxis, label="Rounds", auto_fit=True,
                            tag="elo_plot_x_axis",
                        ):
                            pass
                        with dpg.plot_axis(
                            dpg.mvYAxis, label="Elo", auto_fit=True,
                            tag="elo_plot_y_axis",
                        ):
                            for name, values in self.sim.get_history().items():
                                dpg.add_line_series(
                                    [v[0] for v in values],
                                    [v[1] for v in values],
                                    label=name, tag=f"series_{name}"
                                )
                with dpg.child_window(
                    width=0.25 * self.width, autosize_x=True
                ):
                    dpg.add_text(
                        f"Average Elo = {self.sim.avg_elo:.1f}",
                        tag="avg_elo"
                    )
                    with dpg.group(horizontal=True):
                        dpg.add_button(
                            label="Next Round", callback=self.on_next_round, user_data=self.sim
                        )
                        dpg.add_button(
                            label="Reset",
                            callback=self.reset_simulation,
                        )

                    with dpg.group(horizontal=True):
                        dpg.add_button(
                            label="Simulate Rounds",
                            callback=self.on_simulate_rounds
                        )
                        dpg.add_input_int(
                            label="Number of Rounds",
                            tag="n_rounds", width=100,
                            default_value=self.n_rounds,
                            callback=self.get_n_rounds,
                        )

                    with dpg.group(horizontal=True):
                        dpg.add_input_text(
                            label="",
                            callback=self.set_new_player
                        )
                        dpg.add_button(
                            label="Add Player",
                            callback=self.add_player,
                        )

                    with dpg.tree_node(label="Settings", default_open=True):

                        with dpg.tree_node(
                            label="Pairing Mode", default_open=True,
                            bullet=True,
                        ):
                            dpg.add_radio_button(
                                items=[m.name for m in PairingMode],
                                default_value=self.sim.pairing_mode,
                                callback=self.set_pairing_mode,
                                horizontal=True,
                                tag="pairing_mode_selector"
                            )

                        dpg.add_input_float(
                            label="k",
                            tag="k", width=100,
                            format="%.0f",
                            default_value=self.sim.engine.k,
                            min_value=1,
                            step=1,
                            callback=self.set_simulation_k,
                        )
                        dpg.add_input_float(
                            label="alpha",
                            tag="alpha", width=100,
                            format="%.0f",
                            default_value=self.sim.engine.alpha,
                            min_value=1,
                            step=1,
                            callback=self.set_simulation_alpha,
                        )

        # gui render
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()

        # gui end
        dpg.stop_dearpygui()

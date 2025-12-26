class Player:
    def __init__(self, name: str, skill: float, elo: float = 0):
        self.name = name
        self.skill = skill
        self.elo = elo
        self.delta = 0
        self.last_delta = 0.0

    def update_elo(self):
        self.last_delta = self.delta
        self.elo += self.delta
        self.delta = 0

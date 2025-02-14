import random

# --- Player Classes ---
class Player:
    def __init__(self, name, game=None):
        self.name = name
        self.game = game
        self.wins = 0
        self.losses = 0

    @property
    def nb_games(self):
        return self.wins + self.losses

    @staticmethod
    def play():
        return random.randint(1, 3)

    def win(self):
        self.wins += 1

    def lose(self):
        self.losses += 1

class Human(Player):
    def play(self):
        return int(input(f"{self.name}, combien d'allumettes prenez-vous (1-3) ? "))
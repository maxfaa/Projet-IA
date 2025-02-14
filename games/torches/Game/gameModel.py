import random

class GameModel:
    def __init__(self, nb_matches, player1, player2, display=True):
        self.original_nb = nb_matches
        self.nb = nb_matches
        self.player1 = player1
        self.player2 = player2
        self.displayable = display
        self.current_player = None
        
        self.player1.game = self
        self.player2.game = self
        
        self.shuffle()

    def shuffle(self):
        self.current_player = random.choice([self.player1, self.player2])

    def reset(self):
        self.nb = self.original_nb
        self.shuffle()

    def display(self):
        if self.displayable:
            print(f"Allumettes restantes: {self.nb}")

    def step(self, action):
        if 1 <= action <= 3:
            self.nb -= action

    def play(self):
        while self.nb > 0:
            self.display()
            action = self.current_player.play()
            self.step(action)
            if self.nb <= 0:
                self.current_player.win()
                self.get_loser().lose()
                print(f"{self.current_player.name} gagne !")
                break
            self.switch_player()

    def switch_player(self):
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2

    def is_game_over(self):
        return self.nb <= 0

    def get_current_player(self):
        return self.current_player

    def get_winner(self):
        return self.current_player if self.is_game_over() else None

    def get_loser(self):
        return self.player1 if self.get_winner() == self.player2 else self.player2
    
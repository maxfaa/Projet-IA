import random

class GameModel:
    def __init__(self, nb_torch, players, display=True):
        self.original_nb = nb_torch
        self.nb = nb_torch
        self.players = players
        self.displayable = display
        self.current_player = None
        
        for player in self.players:
            player.game = self
        
        self.shuffle()

    def shuffle(self):
        self.current_player = random.choice(self.players)

    def reset(self):
        self.nb = self.original_nb
        self.shuffle()

    def display(self):
        if self.displayable:
            print(f"Allumettes restantes: {self.nb}")

    def step(self, action):
        self.nb -= action

    def is_game_over(self):
        return self.nb <= 0

    def play(self): 
        while self.nb > 0:
            self.display()
            self.step(self.current_player.play())
            if self.nb <= 0:
                self.current_player.lose()
            self.switch_player()
        self.current_player.win()

    def switch_player(self):
        #self.current_player = self.players[0] if self.current_player == self.players[1] else self.players[1]
        if self.current_player == self.players[1]:
            self.current_player = self.players[0]
        else:
            self.current_player = self.players[1]
            
    def get_current_player(self):
        return self.current_player

    def get_winner(self):
        if self.is_game_over():
            return self.players[0] if self.current_player == self.players[1] else self.players[1]
        else:
            return None
    
    def get_loser(self):
        return self.current_player if self.is_game_over() else None
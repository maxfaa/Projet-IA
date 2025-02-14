# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 16:48:05 2025

@author: hugop
"""
import random
from tkinter import *
from tkinter import messagebox

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


# --- Game Model ---
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
    
    

   # --- Game View ---
class GameView(Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Jeu des allumettes")
        
        self.message_label = Label(self, text="", font=("Arial", 14))
        self.message_label.pack()
        
        self.canvas = Canvas(self, width=800, height=400)
        self.canvas.pack()
        
        self.buttons_frame = Frame(self)
        self.buttons_frame.pack()
        
        self.buttons = []
        for i in range(1, 4):
            button = Button(self.buttons_frame, text=f"Prendre {i}", command=lambda n=i: self.controller.handle_human_move(n))
            button.pack(side="left")
            self.buttons.append(button)
        
        self.update_view()
    
    def update_view(self):
        self.canvas.delete("all")
        self.draw_matches(self.controller.get_nb_matches())
        self.message_label.config(text=self.controller.get_status_message())
    
    def draw_matches(self, count):
        for i in range(count):
            x = 20 + i * 30
            self.canvas.create_line(x, 50, x, 150, width=10, fill='brown')
            self.canvas.create_rectangle((x, 50), (x, 50), width=10, outline='red')
            
    def end_game(self): 
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
        reset_button = Button(self.buttons_frame, text="Recommencer", command=self.controller.reset_game)
        reset_button.pack()
    
    def reset(self):
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
        self.buttons = []
        for i in range(1, 4):
            button = Button(self.buttons_frame, text=f"Prendre {i}", command=lambda n=i: self.controller.handle_human_move(n))
            button.pack(side="left")
            self.buttons.append(button)
        self.update_view()


# --- Game Controler ---
class GameControler:
    def __init__(self, player1, player2, nb_matches=15):
        if not isinstance(player1, Human) and not isinstance(player2, Human):
            raise ValueError("Il doit y avoir au moins un joueur humain.")
        
        self.model = GameModel(nb_matches, player1, player2)
        self.view = GameView(self)
        
        if isinstance(self.model.get_current_player(), Player) and not isinstance(self.model.get_current_player(), Human):
            self.handle_ai_move()

    def start(self):
        self.view.mainloop()
    
    def get_nb_matches(self):
        return self.model.nb

    def get_status_message(self):
        if self.model.is_game_over():
            return f"{self.model.get_winner().name} a gagné !"
        return f"{self.model.get_current_player().name}"
    
    def reset_game(self):
        self.model.reset()
        self.view.reset()
        if isinstance(self.model.get_current_player(), Player) and not isinstance(self.model.get_current_player(), Human):
            self.handle_ai_move()

    def handle_human_move(self, count):
        if isinstance(self.model.get_current_player(), Human):
            self.model.step(count)
            if self.model.is_game_over():
                self.handle_end_game()
            else:
                self.model.switch_player()
                if isinstance(self.model.get_current_player(), Player) and not isinstance(self.model.get_current_player(), Human):
                    self.handle_ai_move()
            self.view.update_view()

    def handle_ai_move(self):
        action = self.model.get_current_player().play()
        self.model.step(action)
        if self.model.is_game_over():
            self.handle_end_game()
        else:
            self.model.switch_player()
        self.view.update_view()

    def handle_end_game(self):
        winner = self.model.get_winner()
        loser = self.model.get_loser()
        winner.win()
        loser.lose()
        self.view.end_game()


if __name__ == "__main__":
    player1 = Human("Player 1")
    player2 = Player("AI")
    game = GameControler(player1, player2)
    game.start()
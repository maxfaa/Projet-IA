from Game.gameModel import *
from Game.gameView import *
from Players.players import *

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
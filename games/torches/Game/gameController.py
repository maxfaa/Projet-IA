from Game.gameModel import *
from Game.gameView import *
from Players.players import *

class GameControler:
    def __init__(self, players: List[str], nb_matches:int =15)-> None:
        if not isinstance(players[0], Human) and not isinstance(players[1], Human):
            raise ValueError("Il doit y avoir au moins un joueur humain.")
        
        self.model = GameModel(nb_matches, players)
        self.view = GameView(self)
        
        if isinstance(self.model.get_current_player(), Player) and not isinstance(self.model.get_current_player(), Human):
            self.handle_ai_move()

    def start(self)-> None:
        self.view.mainloop()
    
    def get_nb_matches(self)-> int:
        return self.model.nb

    def get_status_message(self)-> str:
        if self.model.is_game_over():
            return f"{self.model.get_winner().name} a gagné !"
        return f"Au tour du grand : {self.model.get_current_player().name}"
    
    def reset_game(self)-> None:
        self.model.reset()
        self.view.reset()
        if isinstance(self.model.get_current_player(), Player) and not isinstance(self.model.get_current_player(), Human):
            self.handle_ai_move()

    def handle_human_move(self, count: int)-> None:
        if isinstance(self.model.get_current_player(), Human):
            self.model.step(count)
            if self.model.is_game_over():
                self.handle_end_game()
            else:
                self.model.switch_player()
                if isinstance(self.model.get_current_player(), Player) and not isinstance(self.model.get_current_player(), Human):
                    self.handle_ai_move()
            self.view.update_view()

    def handle_ai_move(self)-> None:
        action = self.model.get_current_player().play()
        self.model.step(action)
        if self.model.is_game_over():
            self.handle_end_game()
        else:
            self.model.switch_player()
        self.view.update_view()

    def handle_end_game(self)-> None:
        winner = self.model.get_winner()
        winner.win()
        loser = self.model.get_loser()
        loser.lose()
        self.view.end_game()
from Game.gameController import *

if __name__ == "__main__":
    p1 = Human('test')
    p2 = Human("zeokf")
    
    game = GameControler([p1, p2])
    game.start()
import sys, random
import board  
import mcts

class HumanPlayer(object):
    """Object queried by ConnectFourGame to get human player's move."""
    def __init__(self, name="Human", color=None):
        self.name = name
        self.color = color 
        self.isHuman = True

    def setColor(self, color):
        self.color = color 

    def getMove(self, board):
        return input("Enter column number for move: ")

class RandomPlayer(object):
    def __init__(self, name="Random", color=None, board=None):
        self.name = name
        self.color = color 
        self.isHuman = True
        self.board = board

    def setColor(self, color):
        self.color = color 

    def setBoard(self, board):
        self.board = board 

    def getMove(self, board):
        col = random.randint(0, 6)
        while not self.board.isLegalMove(col):
            col = random.randint(0, 6)
        return col

class MctsPlayer(object):
    def __init__(self, name="MCTS", color=None, budget=1000):
        self.name = name
        self.budget = budget
        self.mcts_game = mcts.ConnectFour(height=6, width=7, target=4)
        self.mcts_state = ((),) * 7
        self.mcts_budget = budget
        self.color = color

    def setColor(self, color):
        self.color = color

    def setMove(self, columnNumber, color):
        if color != self.color:
            player = self.mcts_game.players[0] if color == "R" else self.mcts_game.players[1]
            print("updating mcts game: %d, playa %d" % (columnNumber, player))
            self.mcts_state = self.mcts_game.result(self.mcts_state, columnNumber, player)

    def getMove(self, board):
        player = self.mcts_game.players[0] if self.color == "R" else self.mcts_game.players[1]
        action = mcts.mcts_uct(self.mcts_game, self.mcts_state, player, self.mcts_budget)
        self.mcts_state = self.mcts_game.result(self.mcts_state, action, player)
        print("MCTS playing action %d, playa %d" % (action, player))
        return action

    def reset(self):
        self.mcts_game = mcts.ConnectFour(height=6, width=7, target=4)
        self.mcts_state = ((),) * 7
        

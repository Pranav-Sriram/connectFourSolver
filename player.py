import sys, random
import board  

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

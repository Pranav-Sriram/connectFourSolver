import sys
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

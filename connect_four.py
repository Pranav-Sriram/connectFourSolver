from __future__ import print_function 
import sys
from board import ConnectFourBoard 
from player import HumanPlayer
from agent import ConnectFourAgent

class ConnectFourGame(object):

	def __init__(self, firstPlayer, secondPlayer, boardHeight=6, boardWidth=7):
		self.board = ConnectFourBoard(boardHeight, boardWidth)	
		self.firstPlayer = firstPlayer 
		self.firstPlayer.setColor("R")
		self.secondPlayer = secondPlayer
		self.secondPlayer.setColor("B")
		self.gameOver = False

	def playMove(self, player):
		move = player.getMove(self.board)
		valid = self.board.addPiece(move, player.color)
		if not valid:
			print("Illegal Move. ")
			self.playMove(player)
		self.board.display()
		self.checkIfGameEnded()

	def checkIfGameEnded(self):
		winner = self.board.containsFourInARow()
		if winner is not None:
			if (winner == "R" and self.firstPlayer.isHuman) or (winner == "B" and self.secondPlayer.isHuman):
				print("Congratulations! " + self.firstPlayer.name + " Won.")		
			elif winner == "R":
				print("Game Over. " + self.firstPlayer.name + " Won.")		
			else:
				print("Game Over. " + self.secondPlayer.name + " Won.")
			exit(0)

		if self.board.isFull():  # Draw
			print("Game over. It's a Draw! ")
			exit(0)

	def play(self):
		while True:
			self.playMove(self.firstPlayer)
			self.playMove(self.secondPlayer)

if __name__=="__main__":
	firstPlayer = HumanPlayer(name="Human")
	secondPlayer = ConnectFourAgent(name="Computer", color="B", algorithm="alphabeta")
	game = ConnectFourGame(firstPlayer=firstPlayer, secondPlayer=secondPlayer)
	game.play()

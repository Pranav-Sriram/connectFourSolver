import tensorflow as tf 
import numpy as np
import random
import copy
from ConnectFourSolver import connectFourGame
from board import ConnectFourBoard

class TemporalDifferenceLearner(object):

	def __init__(self, gamma=0.999, height=6, width=7):
		self.gamma = gamma
		self.height = height
		self.width = width
		self.board = None 
		self.pieceToValue = {"R": 1.0, "B": -1.0, "O": 0.0}

	def boardToMatrix(self, board):
		arr = np.zeros((self.height, self.width))
		for row in range(self.height):
			for col in range(self.width):
				arr[self.height-1-row][col] = self.pieceToValue(board.columns[col][row])
		return arr 
		
	def evaluateBoard(self):
		boardMatrix = self.boardToMatrix(self.board)
		return 0.0  # TODO - forward pass 

	def train(self, numGames):
		self.results = {"R": 0, "B": 0, "Draw": 0}
		for it in range(numGames):
			self.playVirtualGame()

	def getBestMove(self, color):
		"""Reflex policies based on current value function."""
		legalMoves = self.board.getLegalMoves()
		if len(legalMoves) == 0: return None

		bestMove = None
		bestValue = -float("inf") if color == "R" else float("inf")  # Red maximizes, black minimizes value
		for move in legalMoves:
			board.addPiece(move, color)
			value = self.evaluateBoard()
			if (value > bestValue and color == "R") or (value < bestValue and color == "B"):
				bestValue = value 
				bestMove = move 
			board.undoMove()  # important! This undoes scratch work 
		return bestMove, bestValue

	def move(self, color): 	
		winner = self.board.containsFourInARow()
		if winner:
			target = 10.0 if winner == "R" else -10.0
			self.gameIsOver = True
			self.gameResult = winner
		elif self.board.isFull()
			target = 0.0 
			self.gameIsOver = True
			self.gameResult = "Draw"
		else:  # regular move, game has not ended
			bestMove, bestValue = self.getBestMove(color)
			board.addPiece(bestMove, color)
			target = bestValue * self.gamma

		curValue = self.evaluateBoard()  # "prediction" - evaluation of current board state (red's perspective always)
		loss = 0.5 * (curValue - target) ** 2  # implicit TD-learning target. Note - target treated as constant, curValue is for training.
		# backprop - TODO


	def playVirtualGame(self):
		self.board = ConnectFourBoard(boardHeight=self.height, boardWidth=self.width)
		self.gameIsOver = False
		self.gameResult = None
		while not self.gameIsOver:
			self.move("R")
			if not self.gameIsOver(): self.move("B")
		self.results[self.gameResult] += 1

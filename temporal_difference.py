# import tensorflow as tf 
import numpy as np
import random
import time
import copy
import agent 
from connect_four import ConnectFourGame
from player import HumanPlayer
from board import ConnectFourBoard


class TemporalDifferenceLearner(object):

	def __init__(self, color, gamma=0.999, height=6, width=7, 
		eta=0.05, weightsFile=None, outputWeightsFile=None):
		self.gamma = gamma
		self.height = height
		self.width = width
		self.eta = eta
		self.board = None 
		self.pieceToValue = {"R": 1.0, "B": -1.0, "O": 0.0}
		self.color = color 

		self.linearWeights = np.random.normal(
			scale=1.0, size=(height, width)) if weightsFile is None else np.load(weightsFile)

		self.outputWeightsFile = "tdWeights.npy" if outputWeightsFile is None else outputWeightsFile

	def boardToMatrix(self, board):
		arr = np.zeros((self.height, self.width))
		for row in range(self.height):
			for col in range(self.width):
				arr[self.height-1-row][col] = self.pieceToValue[board.columns[col][row]]
		return arr 
		
	def evaluateBoard(self):
		boardMatrix = self.boardToMatrix(self.board)
		return np.sum(self.linearWeights * boardMatrix) / 42.0 # TODO - replace with deep convolutional network

	def updateWeights(self, target):
		curValue = self.evaluateBoard()  # forward pass or "prediction" - evaluation of current board state (red's perspective always)
		gradient = (curValue - target) * self.boardToMatrix(self.board)
		self.linearWeights -= self.eta * gradient

	def getBestMove(self, color, epsilon=0.05):
		"""Reflex policies based on current value function, with epsilon-greedy."""
		legalMoves = self.board.getLegalMoves()
		if len(legalMoves) == 0: return None
		random.shuffle(legalMoves)

		# epsilon-greedy
		if random.random() < epsilon:
			randomMove = legalMoves[random.randint(0, len(legalMoves)-1)]
			self.board.addPiece(randomMove, color)
			randomValue = self.evaluateBoard()
			self.board.undoMove()
			return randomMove, randomValue 

		# Reflex policy
		bestMove = None
		bestValue = -float("inf") if color == "R" else float("inf")  # Red maximizes, black minimizes value
		for move in legalMoves:
			self.board.addPiece(move, color)
			value = self.evaluateBoard()
			if (value > bestValue and color == "R") or (value < bestValue and color == "B"):
				bestValue = value 
				bestMove = move 
			self.board.undoMove()  # important! This undoes scratch work done by looking ahead
		return bestMove, bestValue

	def makeMove(self, color): 	
		winner = self.board.containsFourInARow()
		if winner:
			target = 10.0 if winner == "R" else -12.0
			self.gameIsOver = True
			self.gameResult = winner
		elif self.board.isFull():
			target = -1.0 
			self.gameIsOver = True
			self.gameResult = "Draw"
		else:  # regular move, game has not ended
			bestMove, bestValue = self.getBestMove(color)
			self.board.addPiece(bestMove, color)
			target = bestValue * self.gamma 

		self.updateWeights(target)

	def playVirtualGame(self, display=False, epsilon=0.05):
		self.board = ConnectFourBoard(boardHeight=self.height, boardWidth=self.width)
		self.gameIsOver = False
		self.gameResult = None
		while not self.gameIsOver:
			self.makeMove("R")
			if display: self.display()
			if not self.gameIsOver: 
				self.makeMove("B")
				if display: self.display()
		# print "Game ended with result: ", self.gameResult
		self.results[self.gameResult] += 1

	def train(self, numGames):
		self.results = {"R": 0, "B": 0, "Draw": 0}
		for it in range(numGames):
			if it % 1000 == 0 or it == numGames-1:
				print "Weights: ", self.linearWeights
				print "Results: ", self.results
			self.playVirtualGame()
		np.save(self.outputWeightsFile, self.linearWeights)  # save weights
		
	def display(self):
		self.board.display()
		time.sleep(1.5)

	def setColor(self, color):
		"""Required in order to Interface with ConnectFourGame objects."""
		self.color = color

	def getMove(self, board):
		"""Interface to ConnectFourGame objects."""
		self.board = copy.copy(board)
		bestMove, bestValue = self.getBestMove(color=self.color, epsilon=0.0)
		return bestMove

	
def playAgainstHuman(humanColor, weightsFile):

	agentColor = "R" if humanColor == "B" else "B"

	if humanColor == "R":
		firstPlayer = HumanPlayer(name="Human", color="R")
		secondPlayer = TemporalDifferenceLearner(weightsFile, color="B")  
	else:
		firstPlayer = TemporalDifferenceLearner(weightsFile=weightsFile, color="R")
		secondPlayer = HumanPlayer(name="Human", color="B")

	game = ConnectFourGame(firstPlayer, secondPlayer)
	game.play(display=True)

def playAgainstMinimax(opponentColor, weightsFile, nGames=50, depth=1):
	agentColor = "R" if opponentColor == "B" else "B"

	if opponentColor == "R":
		firstPlayer = agent.ConnectFourAgent(name="minimaxAgent", color="R", depth=depth)
		secondPlayer = TemporalDifferenceLearner(weightsFile=weightsFile, color="B")  
	else:
		firstPlayer = TemporalDifferenceLearner(weightsFile=weightsFile, color="R")
		secondPlayer = agent.ConnectFourAgent(name="minimaxAgent", color="B", depth=depth)

	results = {"R": 0, "B": 0, "Draw": 0}

	for it in range(nGames):
		results[(ConnectFourGame(firstPlayer, secondPlayer, silent=True).play(display=False))] += 1
	return results 


if __name__=="__main__":
	# tdLearner = TemporalDifferenceLearner(color="R", outputWeightsFile="tdWeightsTest2.npy")
	# tdLearner.train(numGames=20000)
	results = playAgainstMinimax(opponentColor="R", weightsFile="tdWeightsTest2.npy", depth=3) 
	print "Results: ", results 

	#for it in range(10):
	#	tdLearner.playVirtualGame(display=True, epsilon=0.0)

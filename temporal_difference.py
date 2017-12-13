import tensorflow as tf 
import numpy as np
import random
import time
import copy
import agent 
from connect_four import ConnectFourGame
from player import HumanPlayer
from board import ConnectFourBoard


class TemporalDifferenceLearner(object):

	def __init__(self, color, gamma=0.995, height=6, width=7, 
		lr=0.05, weightsFile=None, outputWeightsFile=None, linearModel=False):
		self.gamma = gamma  # reinforcement learning decay factor
		self.height = height
		self.width = width
		self.lr = lr  # learning rate
		self.board = None 
		self.pieceToValue = {"R": 1.0, "B": -1.0, "O": 0.0}
		self.color = color 

		if linearModel:
			self.linearWeights = np.random.normal(
				scale=1.0, size=(height, width)) if weightsFile is None else np.load(weightsFile)
			self.outputWeightsFile = "tdWeights.npy" if outputWeightsFile is None else outputWeightsFile

		else:
			self.setupNetwork()
			self.sess = tf.InteractiveSession()
			self.sess.run(tf.global_variables_initializer())

	def setupNetwork(self):
		self.setupWeights()
		self.setupNetworkGraph()
		self.setupTrainStep()

	def setupWeights(self):
		self.W1 = tf.get_variable("W1", [42, 20])
		self.W2 = tf.get_variable("W2", [20, 10])
		self.W3 = tf.get_variable("W3", [10, 1])

	def setupNetworkGraph(self):
		self.boardVec = tf.placeholder(tf.float32, shape=(1, 42))
		self.target = tf.placeholder(tf.float32, shape=None)
		hidden1 = tf.nn.relu(tf.matmul(self.boardVec, self.W1))
		hidden2 = tf.nn.relu(tf.matmul(hidden1, self.W2))
		self.out = tf.matmul(hidden2, self.W3)
		self.loss = 0.5 * (self.out - self.target) ** 2.0

	def setupTrainStep(self):
		self.trainStep = tf.train.AdamOptimizer(self.lr).minimize(self.loss)

	def forwardEvaluation(self, boardVec):
		return self.sess.run(self.out, feed_dict={self.boardVec: boardVec})

	def backPropagate(self, boardVec, target):
		self.trainStep.run(feed_dict={self.boardVec: boardVec, self.target: target})

	def boardToMatrix(self, board):
		arr = np.zeros((self.height, self.width))
		for row in range(self.height):
			for col in range(self.width):
				arr[self.height-1-row][col] = self.pieceToValue[board.columns[col][row]]
		return arr 

	def boardToVec(self, board):
		return self.boardToMatrix(board).reshape(1, 42)
		
	def evaluateBoard(self):
		# return np.sum(self.linearWeights * boardMatrix) / 42.0 # TODO - replace with deep convolutional network
		return self.forwardEvaluation(self.boardToVec(self.board))


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

		self.backPropagate(self.boardToVec(self.board), target)

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
			if it % 400 == 0 or it == numGames-1:
				# print "Weights: ", self.linearWeights
				print("Results: ", self.results)
			self.playVirtualGame()
		#np.save(self.outputWeightsFile, self.linearWeights)  # save weights
		
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

	
def playAgainstHuman(humanColor, tdAgent):
	tdAgent.color = "R" if humanColor == "B" else "B" 

	if humanColor == "R":
		firstPlayer = HumanPlayer(name="Human", color="R")
		secondPlayer = tdAgent 
	else:
		firstPlayer = tdAgent
		secondPlayer = HumanPlayer(name="Human", color="B")

	game = ConnectFourGame(firstPlayer, secondPlayer)
	game.play(display=True)

def playAgainstMinimax(opponentColor, tdAgent=None, nGames=50, depth=1):
	tdAgent.color = "R" if opponentColor == "B" else "B"

	if opponentColor == "R":
		firstPlayer = agent.ConnectFourAgent(name="minimaxAgent", color="R", depth=depth)
		secondPlayer = tdAgent  
	else:
		firstPlayer = tdAgent
		secondPlayer = agent.ConnectFourAgent(name="minimaxAgent", color="B", depth=depth)

	results = {"R": 0, "B": 0, "Draw": 0}

	for it in range(nGames):
		results[(ConnectFourGame(firstPlayer, secondPlayer, silent=True).play(display=False))] += 1
	return results 


if __name__=="__main__":
	tdLearner = TemporalDifferenceLearner(color="R")
	tdLearner.train(numGames=4000)
	playAgainstHuman(humanColor="B", tdAgent=tdLearner)
	#results = playAgainstMinimax(opponentColor="R", weightsFile="tdWeightsTest3.npy", depth=3) 
	#print "Results: ", results 

	#for it in range(10):
	#	tdLearner.playVirtualGame(display=True, epsilon=0.0)

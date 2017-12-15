import tensorflow as tf 
import numpy as np
import random
import time
import copy
from connect_four import ConnectFourGame
from player import HumanPlayer
from board import ConnectFourBoard


class TemporalDifferenceLearner(object):

	def __init__(self, color, gamma=0.995, height=6, width=7, 
		lr=0.02, restorePath=None, weightsFile=None, 
		outputWeightsFile=None, linearModel=False):
		self.color = color 
		self.gamma = gamma  # reinforcement learning decay factor
		self.height = height
		self.width = width
		self.lr = lr  # learning rate
		self.restorePath = restorePath

		self.board = None 
		self.trainMode = False 
		self.pieceToValue = {"R": 1.0, "B": -1.0, "O": 0.0}
		self.results = {"R": 0, "B": 0, "Draw": 0}

		if linearModel:
			self.linearWeights = np.random.normal(
				scale=1.0, size=(height, width)) if weightsFile is None else np.load(weightsFile)
			self.outputWeightsFile = "tdWeights.npy" if outputWeightsFile is None else outputWeightsFile

		else:
			self.setupNetwork()
			self.sess = tf.InteractiveSession()
			self.saver = tf.train.Saver()
			if self.restorePath:
				self.saver.restore(self.sess, self.restorePath)
				print(self.W4.eval())  # test
			else:
				self.sess.run(tf.global_variables_initializer())

	def setupNetwork(self):
		self.setupWeights()
		self.setupNetworkGraph()
		self.setupTrainStep()

	def setupWeights(self):
		self.W1 = tf.get_variable("W1", [42, 24])
		self.b1 = tf.get_variable("b1", [24])
		self.W2 = tf.get_variable("W2", [24, 16])
		self.b2 = tf.get_variable("b2", [16])
		self.W3 = tf.get_variable("W3", [16, 8])
		self.b3 = tf.get_variable("b3", [8])
		self.W4 = tf.get_variable("W4", [8, 1])
		self.b4 = tf.get_variable("b4", [1])

	def setupNetworkGraph(self):
		self.boardVec = tf.placeholder(tf.float32, shape=(1, 42))
		self.target = tf.placeholder(tf.float32, shape=None)
		hidden1 = tf.nn.relu(tf.matmul(self.boardVec, self.W1)) + self.b1
		hidden2 = tf.nn.relu(tf.matmul(hidden1, self.W2)) + self.b2
		hidden3 = tf.nn.relu(tf.matmul(hidden2, self.W3)) + self.b3
		self.evaluation = tf.matmul(hidden3, self.W4) + self.b4 
		self.loss = 0.5 * (self.evaluation - self.target) ** 2.0

	def setupTrainStep(self):
		self.trainStep = tf.train.AdamOptimizer(self.lr).minimize(self.loss)

	def forwardEvaluation(self, boardVec):
		return self.sess.run(self.evaluation, feed_dict={self.boardVec: boardVec})

	def backPropagate(self, boardVec, target, endOfGame=False):
		#print("Target: ", target)
		#print("Value: ", self.forwardEvaluation(boardVec))  # TEST
		numIters = 5 if endOfGame else 1
		if endOfGame and self.trainIter % 2000 == 0:
			print("Iter: ", self.trainIter)
			print("Target: ", target)
			print("Evaluation: ", self.forwardEvaluation(boardVec))
		for it in range(numIters):
			self.trainStep.run(feed_dict={self.boardVec: boardVec, self.target: target})
		if endOfGame and self.trainIter % 2000 == 0:
			print("Evaluation after train steps: ", self.forwardEvaluation(boardVec))

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

	def updateLinearWeights(self, target):
		curValue = self.evaluateBoard()  # forward pass or "prediction" - evaluation of current board state (red's perspective always)
		gradient = (curValue - target) * self.boardToMatrix(self.board)
		self.linearWeights -= self.eta * gradient

	def getBestMove(self, color, epsilon):
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

	def makeMove(self, color, epsilon): 	
		winner = self.board.containsFourInARow()
		if winner:
			target = 10.0 if winner == "R" else -12.0
			self.gameIsOver = True
			self.gameResult = winner
			self.seenReward = True
		elif self.board.isFull():
			target = -1.0 
			self.gameIsOver = True
			self.gameResult = "Draw"
			self.seenReward = True 
		else:  # regular move, game has not ended
			bestMove, bestValue = self.getBestMove(color, epsilon)
			self.board.addPiece(bestMove, color)
			target = bestValue * self.gamma 

		if self.trainMode and (self.trainIter > 1000 or self.gameIsOver):  # Don't backprop until we see some rewards
			self.backPropagate(self.boardToVec(self.board), target, endOfGame=self.gameIsOver)

	def playVirtualGame(self, display=False, epsilon=0.02):
		self.board = ConnectFourBoard(boardHeight=self.height, boardWidth=self.width)
		self.gameIsOver = False
		self.gameResult = None
		while not self.gameIsOver:
			self.makeMove("R", epsilon)
			if display: self.display()
			if not self.gameIsOver: 
				self.makeMove("B", epsilon)
				if display: self.display()
		# print "Game ended with result: ", self.gameResult
		self.results[self.gameResult] += 1

	def train(self, startIter=0, endIter=20000):
		self.trainMode = True 
		if startIter == 0:
			self.results = {"R": 0, "B": 0, "Draw": 0}
		for it in range(startIter, endIter):
			if it % 2000 == 0 or it == endIter-1:
				# print "Weights: ", self.linearWeights
				print("Results: ", self.results)
			self.trainIter = it 
			epsilon = 0.05 if it < 40000 else max(0, 0.04 - it / (3.0 * 1e6))
			self.playVirtualGame(epsilon=epsilon)   # anneals epsilon based on iteration
		savePath = self.saveModel(path="./model_ckpt" + str(endIter))
	
	def saveModel(self, path="model_ckpt"):
		return self.saver.save(self.sess, path)

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
		print("Value: ", bestValue)  # TEST
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




if __name__=="__main__":

	tdLearner = TemporalDifferenceLearner(color="R", restorePath="./model_ckpt20000")
	tdLearner.train(startIter=20000, endIter=100000)
	tdLearner.train(startIter=100000, endIter=200000)
	tdLearner.train(startIter=200000, endIter=400000)
	tdLearner.playVirtualGame(display=True, epsilon=0.0)
	playAgainstHuman(humanColor="B", tdAgent=tdLearner)

	# tdLearner = TemporalDifferenceLearner(color="R")
	# tdLearner.train(endIter=500)
	# tdLearner.train(startIter=500, endIter=5000)
	# playAgainstHuman(humanColor="B", tdAgent=tdLearner)
	# tdLearner.train(startIter=5000, endIter=20000)
	#results = playAgainstMinimax(opponentColor="R", weightsFile="tdWeightsTest3.npy", depth=3) 
	#print "Results: ", results 

	#for it in range(10):
	#	tdLearner.playVirtualGame(display=True, epsilon=0.0)

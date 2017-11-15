import sys
import board 

class ConnectFourAgent(object):
	"""
	Our Connect Four AI Agent. Like HumanPlayer, it is queried by ConnectFourGame for moves. It 
	is passed a ConnectFourBoard object during this query, which encapsulates the game state. 

	The ConnectFourAgent uses the ConnectFourBoard to perform algorithms such as minimax and 
	alpha-beta pruning in order to choose its move. 
	"""
	
	def __init__(self, name="Computer", color=None, algorithm="naive"):
		self.name = name
		self.color = color
		self.opponentColor = "R" if color == "B" else "B"
		self.algorithm = algorithm
		self.isHuman = False


	def setColor(self, color):
		self.color = color 


	def getMove(self, board=None):
		if self.algorithm == "naive":
			return self.naiveMove(board)
		elif self.algorithm == "minimax":
			return self.minimaxMove(board)
		elif self.algorithm == "alphaBetaMove":
			return self.alphaBetaMove(board)
		else:
			raise NameError("Unrecognized algorithm name. ")
		

	def naiveMove(self, board): 
		prevHumanMove = board.getPrevMove()
		moveNumber = board.getNumMoves()
		if moveNumber % 4 < 2:
			priorityList = [prevHumanMove-1, prevHumanMove, prevHumanMove+1]
		else:
			priorityList = [prevHumanMove+1, prevHumanMove, prevHumanMove-1]

		for move in priorityList:
			if board.isLegalMove(move): return move

		for i in range(self.board.width):
			if board.isLegalMove(i): return i 


	def minimaxMove(self, board):
		pass


	def alphaBetaMove(self, board):
		pass 
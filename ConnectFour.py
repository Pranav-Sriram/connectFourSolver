
import sys

class ConnectFourBoard(object):

	def __init__(self, boardHeight=6, boardWidth=7):
		self.width = boardWidth
		self.height = boardHeight

		self.columns = [['O' for h in range(self.height)] for col in range(self.width)] 
		self.columnFillHeights = [0 for col in range(self.width)]  # tracks number of pieces in each column
		self.prevHumanMove = None


	def getRow(self, rowNumber):
		assert(rowNumber >= 0 and rowNumber < self.height)
		return [column[rowNumber] for column in self.columns]


	def isFull(self):
		for i in range(self.width):
			if self.columnFillHeights[i] < self.height:
				return False
		return True


	def addPiece(self, columnNumber, color):
		if columnNumber < 0 or columnNumber >= self.width:  # column numbers should be in (0, 1, ..., self.width-1)
			return False  # illegal move

		columnHeight = self.columnFillHeights[columnNumber]
		if columnHeight == self.height:  # filled, illegal move
			return False

		self.columns[columnNumber][columnHeight] = color
		self.columnFillHeights[columnNumber] += 1
		return True


	def scan(self, line):
		"""
		line: A list of elements in a row, column, or diagonal for 4 in a rwo
		"""
		lineStr = "".join(line)
		if lineStr.find("RRRR") >= 0: return "R"
		if lineStr.find("BBBB") >= 0: return "B"
		return None


	def containsFourInARow(self):
		""" Returns "R", "B", or None, depending on whether there are
		4 in a row R's, B's, or neither"""

		for rowNum in range(self.height):
			winningColor = self.scan(self.getRow(rowNum))
			if winningColor is not None: return winningColor
		for column in self.columns:
			winningColor = self.scan(column)
			if winningColor is not None: return winningColor
		return None 
		# TODO - scan diagonals


	def display(self):
		print "Displaying board: "
		for i in range(self.height-1, -1, -1):   # Iterate over rows from top to bottom
			rowString = ""
			for column in self.columns:
				rowString = rowString + column[i] + " "
			print rowString

		


class ConnectFourGame(object):

	def __init__(self, boardHeight=6, boardWidth=7, humanStarts=True):
		self.board = ConnectFourBoard(boardHeight, boardWidth)
		self.humanStarts = True
		self.gameOver = False
		self.humanColor = "R" if humanStarts else "B"
		self.computerColor = "B" if humanStarts else "R"
		self.moveNumber = 0


	def getHumanMove(self):
		columnNumber = input("Enter column number for move: ")
		if self.board.addPiece(columnNumber, self.humanColor):
			self.prevHumanMove = columnNumber
			return  # success
		else:
			return  # TODO - error handle


	def playComputerMove(self):
		# for now, use a very dumb strategy 
		print "Playing Computer's move: "
		self.moveNumber += 1
		prevHumanMove = self.prevHumanMove
		if self.moveNumber % 2 == 0:
			priorityList = [prevHumanMove-1, prevHumanMove, prevHumanMove+1]
		else:
			priorityList = [prevHumanMove+1, prevHumanMove, prevHumanMove-1]

		for move in priorityList:
			if self.board.addPiece(move, self.computerColor):
				return 

		for i in range(self.board.width):
			if self.board.addPiece(i, self.computerColor):
				return 


	def playMove(self, player):
		if player == "Human":
			self.getHumanMove()	
		else:
			self.playComputerMove()
		self.board.display()
		self.checkIfGameEnded()


	def checkIfGameEnded(self):
		winner = self.board.containsFourInARow()
		if winner is not None:
			if (winner == "R" and self.humanStarts) or (winner == "B" and not self.humanStarts):
				print "Congratulations! Human Won. "
				exit(0)
			else:
				print "Game Over. Computer Won. "
				exit(0)

		if self.board.isFull():  # Draw
			print "Game over. It's a Draw! "
			exit(0)



	def play(self):
		if self.humanStarts:
			while True:
				self.playMove("Human")
				self.playMove("Computer")
		else:
			while True:
				self.playMove("Computer")
				self.playMove("Human")


if __name__=="__main__":
	game = ConnectFourGame()
	game.play()

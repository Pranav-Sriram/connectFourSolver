class ConnectFourBoard(object):
	"""Encapsulates a connect four board.

	Maintains a self.height x self.width grid, implemented as a list of columns. 
	Each column is a list of length self.height, and there are self.width columns. 
	Each square of the grid contains either "R" (a red piece), "B" (a black piece), or "0" (no piece). 
	The board also keeps track of other aspects of game state, such as the sequence and number of moves played,
	and is able to check if the game has ended (i.e. there are four in a row/column/diagonal of some color).

	For full generality, although the board implements ordinary connect 4 on a 6 x 7 board by default,
	the board also supports more general games of connect K on an M x N board. 
	"""

	def __init__(self, boardHeight=6, boardWidth=7, connectK=4):
		self.width = boardWidth
		self.height = boardHeight
		self.connectK = connectK
		self.columns = [['O' for h in range(self.height)] for col in range(self.width)] 
		self.columnFillHeights = [0 for col in range(self.width)]  # tracks number of pieces in each column
		self.moves = []  # list of moves made 
		self.redString = "".join(["R"] * connectK)  # scan board for this pattern to see if red has won
		self.blackString = "".join(["B"] * connectK)

	def getRow(self, rowNumber):
		assert(rowNumber >= 0 and rowNumber < self.height)
		return [column[rowNumber] for column in self.columns]	
	
	def getRows(self):
		return [self.getRow(rowNumber) for rowNumber in range(self.height)]
	
	def getDiagonal(self, yIntercept, slope):
		diagonal = []
		for x in range(self.width):
			y = yIntercept + slope * x
			if y >= 0 and y < self.height:
				diagonal.append(self.columns[x][y])
		return diagonal
				
	def getDiagonals(self):
		diagonals = []
		for coordinateSum in range(self.height+self.width-1):
			diagonals.append(self.getDiagonal(yIntercept=coordinateSum, slope=-1))
		for coordinateDiff in range(1-self.width, self.height):
			diagonals.append(self.getDiagonal(yIntercept=coordinateDiff, slope=1))
		return diagonals	

	def isFull(self):
		return len(self.moves) == self.width * self.height

	def isEmpty(self):
		return len(self.moves) == 0

	def isLegalMove(self, columnNumber):
		"""Checks if a potential move is valid."""
		if columnNumber < 0 or columnNumber >= self.width: return False  # column out of bounds
		if self.columnFillHeights[columnNumber] == self.height:  return False  # column full 
		return True

	def getLegalMoves(self):
		return [x for x in range(self.width) if self.isLegalMove(x)]

	def addPiece(self, columnNumber, color):
		"""Adds piece of given color to given column if legal."""
		if not self.isLegalMove(columnNumber): return False
		self.columns[columnNumber][self.columnFillHeights[columnNumber]] = color
		self.columnFillHeights[columnNumber] += 1
		self.moves.append(columnNumber)
		return True

	def scan(self, line):
		"""Scans a list of elements in a row, column, or diagonal for 4 in a row (or K in a row in general case)."""
		lineStr = "".join(line) 
		if lineStr.find(self.redString) >= 0: return "R"
		if lineStr.find(self.blackString) >= 0: return "B"
		return None

	def containsFourInARow(self):
		"""Searches for four in row/column/diagonal R's or B's."""
		lines = self.columns + self.getRows() + self.getDiagonals()
		for line in lines:
			winningColor = self.scan(line)
			if winningColor is not None: return winningColor
		return None
			
	def display(self):
		"""Simple function to display board in the terminal."""
		print("Displaying board now: ")
		for i in range(self.height-1, -1, -1):   # Iterate over rows from top to bottom
			rowString = ""
			for column in self.columns:
				rowString = rowString + column[i] + " "
			print(rowString)

	def getPrevMove(self):
		return 3 if len(self.moves) == 0 else self.moves[len(self.moves)-1]

	def undoMove(self):
		if len(self.moves) == 0: return 
		prevColumn = self.moves.pop()  # remove move from self.moves
		self.columnFillHeights[prevColumn] -= 1
		self.columns[prevColumn][self.columnFillHeights[prevColumn]] = 'O'

	def getNumMoves(self):
		return len(self.moves)

	def getState2dArray(self):
		state = []
		for i in range(0, self.height):   # Iterate over rows from top to bottom
			row = []
			for j, column in enumerate(self.columns):
				row.append(column[i])
			state.append(row)
		return state


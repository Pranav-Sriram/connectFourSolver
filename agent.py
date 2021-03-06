import sys
import copy
import board
from minimax import Minimax
from td_alpha_beta import TDAlphaBeta

class ConnectFourAgent(object):
    """
    Our Connect Four AI Agent. Like HumanPlayer, it is queried by ConnectFourGame for moves. It 
    is passed a ConnectFourBoard object during this query, which encapsulates the game state. 

    The ConnectFourAgent uses the ConnectFourBoard to perform algorithms such as minimax and 
    alpha-beta pruning in order to choose its move. 
    """

    def __init__(self, name="Computer", color=None, depth=3, algorithm="minimax", mcts_budget=1000, tdEvaluator=None, evalfn="simple"):

        self.name = name
        self.color = color
        self.opponentColor = "R" if color == "B" else "B"
        self.algorithm = algorithm
        self.isHuman = False
        self.minimax_depth = depth

        if algorithm == "TDAlphaBeta":
            self.tdAlphaBetaSolver = TDAlphaBeta(tdEvaluator)
        else:
            self.minimaxSolver = Minimax(evalfn)
        
    def setColor(self, color):
        self.color = color 

    def getMove(self, board=None):
        if self.algorithm == "naive":
            return self.naiveMove(board)
        elif self.algorithm == "minimax":
            return self.minimaxMove(board)
        elif self.algorithm == "alphabeta":
            return self.alphaBetaMove(board)
        elif self.algorithm == "expectimax":
            return self.expectimaxMove(board)
        elif self.algorithm == "mcts":
            return self.mctsMove(board)
        elif self.algorithm == "TDAlphaBeta":
            return self.tdAlphaBetaMove(board)
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

        for i in range(board.width):
            if board.isLegalMove(i): return i

    def minimaxMove(self, board):
        return self.minimaxSolver.bestMove(self.minimax_depth, copy.deepcopy(board), self.color)

    def alphaBetaMove(self, board):
        return self.minimaxSolver.bestMove(self.minimax_depth, copy.deepcopy(board), self.color, True)

    def expectimaxMove(self, board):
        return self.minimaxSolver.bestMove(self.minimax_depth, board.getState2dArray(), self.color, True)

    def tdAlphaBetaMove(self, board):
        return self.tdAlphaBetaSolver.bestMove(self.minimax_depth, copy.deepcopy(board), self.color)

    def getAction(self, board):
        pass 


__author__ = 'pranavsriram'
import copy
import board
import random, sys
import temporal_difference

neg_inf = float('-inf')
inf = float('inf')

# Note: all evaluation done from perspective of red, the maximizer

class TDAlphaBeta(object):
    """ Combines alpha-beta search with learned TD evaluation function."""

    def __init__(self, tdEvaluator):
        self.tdEvaluator = tdEvaluator

    def bestMove(self, depth, board, curr_player):
        """ Returns the best move (as a column number) and the associated alpha
        """
        if board.isEmpty(): return 3  # hard code first move

        maximizer = (curr_player == "R")  # Red maximizes, black minimizes

        # determine opponent's color
        opp_player = "B" if curr_player == "R" else "R"

        # enumerate all legal moves
        allowed_moves = board.getLegalMoves()
        moveValues = {} # will map legal moves to their alpha values
        for col in allowed_moves:
            # make the move in column 'col' for curr_player
            boardCopy = copy.deepcopy(board)
            boardCopy.addPiece(col, curr_player)
            moveValues[col] = self.search_alpha_beta(depth-1, boardCopy, opp_player, neg_inf, inf, (not maximizer))
              
        
        best_move = None
        moves = list(moveValues.items())
        random.shuffle(moves)
        if maximizer:
            best_alpha = neg_inf
            for move, alpha in moves:
                if alpha >= best_alpha:
                    best_alpha = alpha
                    best_move = move

        else:
            best_beta = inf
            for move, beta in moves:
                if beta <= best_beta:
                    best_beta = beta
                    best_move = move
        return best_move
    
    # Search with alpha-beta pruning
    def search_alpha_beta(self, depth, board, curr_player, a, b, maximizing_player):
        """ Searches the tree at depth 'depth'
            curr_player is whoever called this search
            Returns the alpha value 
        """

        legalMoves = board.getLegalMoves()
        opp_player = "B" if curr_player == "R" else "B"
        
        # Handle terminal nodes and depth=0 
        if board.isFull():  # Draw
            return 0.0

        winner = board.containsFourInARow()
        if winner:
            return (20.0 + depth) if winner == "R" else -(depth+20.0)  # win early, lose late

        if depth == 0:
            return self.evaluate(board)  # return heuristic value 

        # Otherwise 

        if maximizing_player:
            v = neg_inf
            for move in legalMoves:
                newBoard = copy.deepcopy(board)
                newBoard.addPiece(move, curr_player)
                childVal = self.search_alpha_beta(depth-1, newBoard, opp_player, a, b, False)
                v = max(v, childVal)
                a = max(a, v)
                if b <= a:
                    break
            return v
        else:
            v = inf
            for move in legalMoves:
                newBoard = copy.deepcopy(board)
                newBoard.addPiece(move, curr_player)
                childVal = self.search_alpha_beta(depth-1, newBoard, opp_player, a, b, True)
                v = min(v, childVal)
                b = min(b, v)
                if b <= a:
                    break
            return v

    def evaluate(self, board):
        boardVec = self.tdEvaluator.boardToVec(board)
        return self.tdEvaluator.forwardEvaluation(boardVec)

    
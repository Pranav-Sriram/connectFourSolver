
__author__ = 'catherinaxu'

import board

import random, sys

neg_inf = float('-inf')
inf = float('inf')

class Minimax(object):
    """ Minimax object that takes a current connect four board state
    """
    color = None

    def __init__(self):
        # copy the board to self.board
        pass

    def bestMove(self, depth, board, curr_player, alpha_beta=False):
        """ Returns the best move (as a column number) and the associated alpha
            Calls search()
        """
        state = board.getState2dArray()

        # determine opponent's color
        opp_player = "B" if curr_player == "R" else "R"

        # enumerate all legal moves
        legal_moves = {} # will map legal move states to their alpha values
        for col in range(7):
            # if column i is a legal move...
            if self.isLegalMove(col, state):
                # make the move in column 'col' for curr_player
                temp = self.makeMove(state, col, curr_player)
                if alpha_beta:
                    legal_moves[col] = -self.search_alpha_beta(depth-1, temp, opp_player, neg_inf, inf)
                else:
                    legal_moves[col] = -self.search_alpha_beta(depth-1, temp, opp_player, neg_inf, inf)
        best_alpha = neg_inf
        best_move = None
        moves = list(legal_moves.items())
        random.shuffle(moves)
        for move, alpha in moves:
            if alpha >= best_alpha:
                best_alpha = alpha
                best_move = move
        return best_move

    def search(self, depth, state, curr_player):
        """ Searches the tree at depth 'depth'
            By default, the state is the board 2d array, and curr_player is whomever
            called this search
            Returns the alpha value
        """

        # enumerate all legal moves from this state
        legal_moves = []
        for i in range(7):
            # if column i is a legal move...
            if self.isLegalMove(i, state):
                # make the move in column i for curr_player
                temp = self.makeMove(state, i, curr_player)
                legal_moves.append(temp)

        # if this node (state) is a terminal node or depth == 0...
        if depth == 0 or len(legal_moves) == 0 or self.gameIsOver(state):
            # return the heuristic value of node
            return self.value(state, curr_player)

        # determine opponent's color
        opp_player = "B" if curr_player == "R" else "R"

        alpha = float('-inf')
        for child in legal_moves:
            if child == None:
                print("child == None (search)")
            alpha = max(alpha, -self.search(depth-1, child, opp_player))
        return alpha

    # Search with alpha-beta pruning
    def search_alpha_beta(self, depth, state, curr_player, a, b):
        """ Searches the tree at depth 'depth'
            By default, the state is the board, and curr_player is whomever
            called this search
            Returns the alpha value
        """

        # enumerate all legal moves from this state
        legal_moves = []
        for i in range(7):
            # if column i is a legal move...
            if self.isLegalMove(i, state):
                # make the move in column i for curr_player
                temp = self.makeMove(state, i, curr_player)
                legal_moves.append(temp)

        # if this node (state) is a terminal node or depth == 0...
        if depth == 0 or len(legal_moves) == 0 or self.gameIsOver(state):
            # return the heuristic value of node
            return self.value(state, curr_player)

        # determine opponent's color
        opp_player = "B" if curr_player == "R" else "B"

        alpha = float('-inf')
        for child in legal_moves:
            if child == None:
                print("child == None (search)")
            child = -self.search_alpha_beta(depth-1, child, opp_player, a, b)
            alpha = max(alpha, child)
            a = max(a, alpha)
            if b <= a:
                return child
        return alpha

    def isLegalMove(self, column, state):
        """ Boolean function to check if a move (column) is a legal move
        """
        for i in range(6):
            if state[i][column] == 'O':

                # once we find the first empty, we know it's a legal move
                return True

        # if we get here, the column is full
        return False

    def gameIsOver(self, state):
        if self.checkForStreak(state, "R", 4) >= 1:
            return True
        elif self.checkForStreak(state, "B", 4) >= 1:
            return True
        else:
            return False


    def makeMove(self, state, column, color):
        """ Change a state object to reflect a player, denoted by color,
            making a move at column 'column'
            Returns a copy of new state array with the added move
        """

        temp = [x[:] for x in state]
        for i in range(6):
            if temp[i][column] == 'O':
                temp[i][column] = color
                return temp

    def value0(self, state, color):
        """ Simple heuristic to evaluate board configurations
            Heuristic is (num of 4-in-a-rows)*99999 + (num of 3-in-a-rows)*100 +
            (num of 2-in-a-rows)*10 - (num of opponent 4-in-a-rows)*99999 - (num of opponent
            3-in-a-rows)*100 - (num of opponent 2-in-a-rows)*10
        """
        if color == 'R':
            o_color = 'B'
        else:
            o_color = 'R'

        my_fours = self.checkForStreak(state, color, 4, 0)
        my_threes = self.checkForStreak(state, color, 3, 0)
        my_twos = self.checkForStreak(state, color, 2, 0)
        opp_fours = self.checkForStreak(state, o_color, 4, 0)
        #opp_threes = self.checkForStreak(state, o_color, 3)
        #opp_twos = self.checkForStreak(state, o_color, 2)
        if opp_fours > 0:
            return -100000
        else:
            return my_fours * 100000 + my_threes * 100 + my_twos

    def value(self, state, color):
        """ Simple heuristic to evaluate board configurations
            Heuristic is (num of 4-in-a-rows)*99999 + (num of 3-in-a-rows)*100 +
            (num of 2-in-a-rows)*10 - (num of opponent 4-in-a-rows)*99999 - (num of opponent
            3-in-a-rows)*100 - (num of opponent 2-in-a-rows)*10
        """
        if color == 'R':
            o_color = 'B'
        else:
            o_color = 'R'

        my_fours = self.checkForStreak(state, color, 4, 0)
        my_threes = self.checkForStreak(state, color, 3, 0)
        my_twos = self.checkForStreak(state, color, 2, 0)
        opp_fours = self.checkForStreak(state, o_color, 4, 0)
        opp_threes = self.checkForStreak(state, o_color, 3)
        opp_twos = self.checkForStreak(state, o_color, 2)

        my_fours_one_space = self.checkForStreak(state, color, 4, 1)
        my_threes_one_space = self.checkForStreak(state, color, 3, 1)
        my_fours_two_space = self.checkForStreak(state, color, 4, 2)
        opp_fours_one_space = self.checkForStreak(state, o_color, 4, 1)
        opp_threes_one_space = self.checkForStreak(state, o_color, 3, 1)
        opp_fours_two_space = self.checkForStreak(state, o_color, 4, 2)

        undefeatable_streak = self.checkForSurroundedStreak(state, color, 'O')
        opp_undefeatable_streak = self.checkForSurroundedStreak(state, o_color, 'O')

        my_threes_useless = self.checkForSurroundedStreak(state, color, o_color)
        opp_threes_useless = self.checkForSurroundedStreak(state, o_color, color)

        if opp_fours > 0:
            return -100000
        else:
            return my_fours * 100000 + (my_threes + my_fours_one_space) * 100 + (my_twos + my_threes_one_space)

    # Check for a 3-in-a-row with empty spaces on both sides :0
    def checkForSurroundedStreak(self, state, color, surrounding_color):
        count = 0
        for i in range(6):
            for j in range(7):
                # ...that is of the color we're looking for...
                if state[i][j] == 'O':
                    if self.verticalStreak(i, j, state, 3, 0):
                        next_row = i+1
                        if next_row < 6 and state[next_row][j] == surrounding_color:
                            count += 1
                    if self.horizontalStreak(i, j, state, 3, 0):
                        next_col = j+1
                        if next_col < 7 and state[i][next_col] == surrounding_color:
                            count += 1
                    if self.horizontalStreak(i, j, state, 3, 0):
                        next_col = j+1
                        if next_col < 7 and state[i][next_col] == surrounding_color:
                            count += 1
                    for end_diag in self.diagonalCheck(i, j, state, 3, 0):
                        if end_diag[0] < 6 and end_diag[1] < 7 and end_diag[0] >= 0 and end_diag[1] >= 0:
                            if state[end_diag[0]][end_diag[1]] == surrounding_color:
                                count += 1
        return count

    # Returns the number of streaks of length `streak_len`, with `num_empty_allowed` empty spaces allowed in the middle at the end of streaks.
    def checkForStreak(self, state, color, streak_len, num_empty_allowed=0):
        count = 0
        # for each piece in the board...
        for i in range(6):
            for j in range(7):
                # ...that is of the color we're looking for...
                if state[i][j].lower() == color.lower() or (num_empty_allowed > 0 and state[i][j] == 'O'):
                    # check if a vertical streak starts at (i, j)
                    count += self.verticalStreak(i, j, state, streak_len, num_empty_allowed)

                    # check if a horizontal four-in-a-row starts at (i, j)
                    count += self.horizontalStreak(i, j, state, streak_len, num_empty_allowed)

                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    count += len(self.diagonalCheck(i, j, state, streak_len, num_empty_allowed))
        # return the sum of streaks of length 'streak'
        return count

    def verticalStreak(self, row, col, state, streak, num_empty_allowed):
        consecutiveCount = 0
        emptyCount = 0
        for i in range(row, 6):
            if state[i][col].lower() == state[row][col].lower():
                consecutiveCount += 1
            elif emptyCount < num_empty_allowed and state[i][col] == 'O':
                emptyCount += 1
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= streak:
            return 1
        else:
            return 0

    def horizontalStreak(self, row, col, state, streak, num_empty_allowed):
        consecutiveCount = 0
        emptyCount = 0
        for j in range(col, 7):
            if state[row][j].lower() == state[row][col].lower():
                consecutiveCount += 1
            elif emptyCount < num_empty_allowed and state[row][j] == 'O':
                emptyCount += 1
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= streak:
            return 1
        else:
            return 0

    # Return list of (r, c) cells where the diagonal ends
    def diagonalCheck(self, row, col, state, streak, num_empty_allowed):

        streaks = []
        # check for diagonals with positive slope
        consecutiveCount = 0
        emptyCount = 0
        j = col
        i = 0
        for i in range(row, 6):
            if j > 6:
                break
            elif state[i][j].lower() == state[row][col].lower():
                consecutiveCount += 1
            elif emptyCount < num_empty_allowed and state[i][j] == 'O':
                emptyCount += 1
                consecutiveCount += 1
            else:
                break
            j += 1 # increment column when row is incremented

        if consecutiveCount >= streak:
            streaks.append((i, j))

        # check for diagonals with negative slope
        consecutiveCount = 0
        emptyCount = 0
        j = col
        i = 0
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif state[i][j].lower() == state[row][col].lower():
                consecutiveCount += 1
            elif emptyCount < num_empty_allowed and state[i][j] == 'O':
                emptyCount += 1
                consecutiveCount += 1
            else:
                break
            j += 1 # increment column when row is incremented

        if consecutiveCount >= streak:
            streaks.append((i, j))

        return streaks

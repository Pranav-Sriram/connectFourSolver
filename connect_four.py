from __future__ import print_function 
import sys
from optparse import OptionParser
from board import ConnectFourBoard 
from player import HumanPlayer, RandomPlayer
from agent import ConnectFourAgent

class ConnectFourGame(object):

    def __init__(self, firstPlayer, secondPlayer, boardHeight=6, boardWidth=7):
        self.board = ConnectFourBoard(boardHeight, boardWidth)  
        self.firstPlayer = firstPlayer 
        self.firstPlayer.setColor("R")
        self.secondPlayer = secondPlayer
        self.secondPlayer.setColor("B")
        self.gameOver = False
        self.numMoves = 0

    def playMove(self, player, display=True):
        move = player.getMove(self.board)
        valid = self.board.addPiece(move, player.color)
        if not valid:
            print("Illegal Move, try again. ")
            self.playMove(player, display)
        if display: self.board.display()
        self.numMoves += 1
        return self.checkIfGameEnded()

    def checkIfGameEnded(self):
        winner = self.board.containsFourInARow()
        if winner is not None:
            return winner
        if self.board.isFull():  # Draw
            return 'Draw'

    def play(self, display):
        players = [self.firstPlayer, self.secondPlayer]
        player_index = 0
        while True:
            winner = self.playMove(players[player_index], display)
            if winner is not None:
                if winner == 'Draw':
                    print('Draw.')
                else:
                    print(winner + " won.")
                return winner
            player_index = (player_index + 1) % 2

def getParserOptions():
    parser = OptionParser()
    parser.add_option("-f", action="store_true", dest="computerFirst")  # makes computer start instead of human
    parser.add_option("-a", action="store_true", dest="alphaBeta")  # uses alpha-beta pruning
    parser.add_option("-d", action="store_true", dest="display")  # displays board after each move
    parser.add_option("-t", type="int", dest="numTrials")  # simulate against random player for numTrials      
    parser.add_option("--depth", type="int", dest="depth")           
    return parser.parse_args()

if __name__=="__main__":
    flags, args = getParserOptions()
    
    algorithm = "minimax" if not flags.alphaBeta else "alphabeta" 
    depth = 3 if not hasattr(flags, "depth") else flags.depth               

    if flags.numTrials is None:
        if flags.computerFirst:
            firstPlayer = ConnectFourAgent(name="Computer", color="R", algorithm=algorithm, depth=depth)
            secondPlayer = HumanPlayer(name="Human")
        else:
            firstPlayer = HumanPlayer(name="Human")
            secondPlayer = ConnectFourAgent(name="Computer", color="B", algorithm=algorithm, depth=depth)

        game = ConnectFourGame(firstPlayer=firstPlayer, secondPlayer=secondPlayer)
        game.play(display=bool(flags.display))
					  
    else:
        results = {}

        #to conduct analysis on the 'significance' of the win or loss, store (num_aggregate_moves, num_instances) pairs
        #more moves = good if you are losing more
        #more moves = neutral if you are calling a draw
        #more moves = bad if you are winning more

        RWin_tuple = [0, 0]
        BWin_tuple = [0, 0]

        for i in range(flags.numTrials):
            firstPlayer = ConnectFourAgent(name="Computer1", color="R", algorithm="minimax", depth=4)
            secondPlayer = ConnectFourAgent(name="Computer2", color="B", algorithm="minimax", depth=3)
            game = ConnectFourGame(firstPlayer=firstPlayer, secondPlayer=secondPlayer)
            winner = game.play(display=False)
            if winner not in results.keys():
                results[winner] = 0
            results[winner] += 1
            print(game.numMoves)
            if winner == 'R':
                RWin_tuple[0] += game.numMoves
                RWin_tuple[1] += 1
            elif winner == 'B':
                BWin_tuple[0] += game.numMoves
                BWin_tuple[1] += 1

        print("Results after %d trials: %s" % (flags.numTrials, str(results)))
        if RWin_tuple[1] != 0:
            print("Average moves in R wins (lower -> better): %.2f" % (float(RWin_tuple[0]) / float(RWin_tuple[1])))
        if BWin_tuple[1] != 0:
            print("Average moves in B wins (lower -> better): %.2f" % (float(BWin_tuple[0]) / float(BWin_tuple[1])))

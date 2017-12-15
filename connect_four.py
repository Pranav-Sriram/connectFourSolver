from __future__ import print_function 
import sys
from optparse import OptionParser
from board import ConnectFourBoard 
from player import HumanPlayer, RandomPlayer, MctsPlayer, VelengPlayer
from agent import ConnectFourAgent

class ConnectFourGame(object):


    def __init__(self, firstPlayer, secondPlayer, boardHeight=6, boardWidth=7, mcts_enabled=False, mctsPlayer=None, mcts_budget=1000, silent=False):
        self.board = ConnectFourBoard(boardHeight, boardWidth)
        self.firstPlayer = firstPlayer 
        self.firstPlayer.setColor("R")
        self.secondPlayer = secondPlayer
        self.secondPlayer.setColor("B")
        self.silent = silent 
        self.gameOver = False
        self.numMoves = 0

    def playMove(self, player, display=True, mctsPlayerToUpdate=None):
        move = player.getMove(self.board)
        valid = self.board.addPiece(move, player.color)
        if not valid:
            print("Illegal Move: " + str(move))
            self.playMove(player, display)
            #self.board.update_mtcs_game(move, player.color)
        if mctsPlayerToUpdate is not None:
            mctsPlayerToUpdate.setMove(move, player.color)
        if display: self.board.display()
        self.numMoves += 1
        return self.checkIfGameEnded()

    def checkIfGameEnded(self):
        winner = self.board.containsFourInARow()
        if winner is not None:
            return winner
        if self.board.isFull():  # Draw
            return 'Draw'

    def play(self, display, mctsPlayerToUpdate=None):
        players = [self.firstPlayer, self.secondPlayer]
        player_index = 0
        while True:
            winner = self.playMove(players[player_index], display, mctsPlayerToUpdate)
            if winner is not None:
                if winner == 'Draw':
                    if not self.silent: print('Draw.')
                else:
                    if not self.silent: print(winner + " won.")
                return winner
            player_index = (player_index + 1) % 2


def simulate(numTrials, firstPlayer, secondPlayer, mctsPlayerToUpdate=None):
    for i in range(flags.numTrials):
        game = ConnectFourGame(firstPlayer=firstPlayer, secondPlayer=secondPlayer)
        win_color = game.play(display=False, mctsPlayerToUpdate=mctsPlayerToUpdate)
        if firstPlayer.color == win_color:
            winner = firstPlayer.name
        else:
            winner = secondPlayer.name
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
        if mctsPlayerToUpdate is not None:
            mctsPlayerToUpdate.reset()

    print("Results after %d trials: %s" % (flags.numTrials, str(results)))
    if RWin_tuple[1] != 0:
        print("Average moves in R wins (lower -> better): %.2f" % (float(RWin_tuple[0]) / float(RWin_tuple[1])))
    if BWin_tuple[1] != 0:
        print("Average moves in B wins (lower -> better): %.2f" % (float(BWin_tuple[0]) / float(BWin_tuple[1])))


def getParserOptions():
    parser = OptionParser()
    parser.add_option("-f", action="store_true", dest="computerFirst")  # makes computer start instead of human
    parser.add_option("-a", action="store_true", dest="alphaBeta")  # uses alpha-beta pruning
    parser.add_option("-d", action="store_true", dest="display")  # displays board after each move
    parser.add_option("-t", type="int", dest="numTrials")  # simulate against random player for numTrials      
    parser.add_option("--depth", type="int", dest="depth")           

    # MCTS flags
    parser.add_option("-m", action="store_true", dest="mctsEnabled")
    parser.add_option("-b", type="int", dest="mctsBudget")

    # Veleng flags
    parser.add_option("-v", action="store_true", dest="velengEnabled")

    parser.add_option("-r", action="store_true", dest="reverseOrder")
    parser.add_option("-e", action="store_true", dest="compareEvals")
    return parser.parse_args()

if __name__=="__main__":
    flags, args = getParserOptions()
    
    algorithm = "minimax" if not flags.alphaBeta else "alphabeta" 
    depth = 3 if flags.depth is None else flags.depth               

    mctsPlayer = None

    mcts_budget = 1000
    if flags.mctsBudget is not None:
        mcts_budget = flags.mctsBudget

    if flags.numTrials is None:
        # Human v. Computer

        if flags.computerFirst:
            firstPlayer = ConnectFourAgent(name="Computer", color="R", algorithm=algorithm, depth=depth)
            if flags.mctsEnabled is not None:
                firstPlayer = MctsPlayer(color="R", budget=mcts_budget)
            secondPlayer = HumanPlayer(name="Human")
            mctsPlayer = firstPlayer
        else:
            firstPlayer = HumanPlayer(name="Human")
            secondPlayer = ConnectFourAgent(name="Computer", color="B", algorithm=algorithm, depth=depth)
            if flags.mctsEnabled is not None:
                secondPlayer = MctsPlayer(color="B", budget=mcts_budget)
            mctsPlayer = secondPlayer

        game = ConnectFourGame(firstPlayer=firstPlayer, secondPlayer=secondPlayer, mcts_enabled=flags.mctsEnabled, mctsPlayer=mctsPlayer)
        game.play(display=bool(flags.display))
            
    else:
        # Computer v. Computer for t trials

        results = {}

        #to conduct analysis on the 'significance' of the win or loss, store (num_aggregate_moves, num_instances) pairs
        #more moves = good if you are losing more
        #more moves = neutral if you are calling a draw
        #more moves = bad if you are winning more

        RWin_tuple = [0, 0]
        BWin_tuple = [0, 0]

        firstPlayer = ConnectFourAgent(name="Computer1", color="R", algorithm="minimax", depth=4)
        secondPlayer = None
        mctsPlayer = None
        if flags.mctsEnabled:
            secondPlayer = MctsPlayer(color="B", budget=mcts_budget)
            mctsPlayer = secondPlayer
        elif flags.velengEnabled:
            secondPlayer = VelengPlayer(color="B")
        elif flags.compareEvals:
            secondPlayer = ConnectFourAgent(name="Computer2", color="B", algorithm="minimax", depth=4, evalfn="complex")
        else:
            secondPlayer = ConnectFourAgent(name="Computer2", color="B", algorithm="minimax", depth=3)
        if flags.reverseOrder:
            simulate(flags.numTrials, secondPlayer, firstPlayer, mctsPlayerToUpdate=mctsPlayer)
        else:
            simulate(flags.numTrials, firstPlayer, secondPlayer, mctsPlayerToUpdate=mctsPlayer)

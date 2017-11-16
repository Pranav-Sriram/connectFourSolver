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

    def playMove(self, player, display=True):
        move = player.getMove(self.board)
        valid = self.board.addPiece(move, player.color)
        if not valid:
            print("Illegal Move. ")
            self.playMove(player, display)
        if display: self.board.display()
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

if __name__=="__main__":
    parser = OptionParser()
    parser.add_option("-t", type="int", dest="num_trials")
    parser.add_option("-a", dest="alpha_beta")
    (flags, args) = parser.parse_args()

    if flags.num_trials is None:
        firstPlayer = HumanPlayer(name="Human")
        secondPlayer = ConnectFourAgent(name="Computer", color="B", algorithm="minimax")
        if flags.alpha_beta is not None:
            secondPlayer = ConnectFourAgent(name="Computer", color="B", algorithm="alphabeta")
        game = ConnectFourGame(firstPlayer=firstPlayer, secondPlayer=secondPlayer)
        game.play()
    else:
        results = {}
        for i in xrange(flags.num_trials):
            firstPlayer = RandomPlayer(name="Random")
            secondPlayer = ConnectFourAgent(name="Computer", color="B", algorithm="alphabeta")
            game = ConnectFourGame(firstPlayer=firstPlayer, secondPlayer=secondPlayer)
            firstPlayer.setBoard(game.board)
            winner = game.play(False)
            if winner not in results:
                results[winner] = 0
            results[winner] += 1
        print("Results after %d trials: %s" % (flags.num_trials, str(results)))

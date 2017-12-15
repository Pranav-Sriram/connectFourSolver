from temporal_difference import TemporalDifferenceLearner
from agent import ConnectFourAgent
from player import HumanPlayer
from connect_four import ConnectFourGame

def playAgainstHuman(agentColor, humanColor):
	tdLearner = TemporalDifferenceLearner(color=agentColor, restorePath="./model_ckpt100000")
	agent = ConnectFourAgent(color=humanColor, depth=6, algorithm="TDAlphaBeta", tdEvaluator=tdLearner)
	human = HumanPlayer()

	if agentColor == "R":
		game = ConnectFourGame(firstPlayer=agent, secondPlayer=human)
	else: 
		game = ConnectFourGame(firstPlayer=human, secondPlayer=agent)
	game.play(display=True)

def playAgainstMinimax(numGames, tdColor, minimaxColor):
	tdLearner = TemporalDifferenceLearner(color="R", restorePath="./model_ckpt100000")

	results = {"R": 0, "B": 0, "Draw": 0}

	for i in range(numGames):
		tdAlphaBetaAgent = ConnectFourAgent(color="tdColor", depth=4, algorithm="TDAlphaBeta", tdEvaluator=tdLearner)
		minimaxAgent = ConnectFourAgent(color="minimaxColor", depth=4, algorithm="minimax")
		game = ConnectFourGame(firstPlayer=tdAlphaBetaAgent, secondPlayer=minimaxAgent)
		results[game.play(display=False)] += 1

	print(results)


if __name__=="__main__":
	#playAgainstHuman(agentColor="B", humanColor="R")
	playAgainstMinimax(50, "R", "B")
	playAgainstMinimax(50, "B", "R")
	


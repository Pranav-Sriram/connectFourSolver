import temporal_difference 
import agent 
import connect_four 
from player import HumanPlayer

def playAgainstHuman(agentColor, humanColor, restorePath, depth):
	tdLearner = temporal_difference.TemporalDifferenceLearner(color=agentColor, restorePath=restorePath)
	tdAlphaBetaAgent = agent.ConnectFourAgent(color=humanColor, depth=depth, algorithm="TDAlphaBeta", tdEvaluator=tdLearner)
	human = HumanPlayer()

	if agentColor == "R":
		game = connect_four.ConnectFourGame(firstPlayer=tdAlphaBetaAgent, secondPlayer=human)
	else: 
		game = connect_four.ConnectFourGame(firstPlayer=human, secondPlayer=tdAlphaBetaAgent)
	game.play(display=True)

def playAgainstMinimax(numGames, tdColor, minimaxColor, restorePath, depth):
	tdLearner = temporal_difference.TemporalDifferenceLearner(color="R", restorePath=restorePath)

	results = {"R": [0, 0], "B": [0, 0], "Draw": [0, 0]}  # [numWins, numMoves]

	for i in range(numGames):
		tdAlphaBetaAgent = agent.ConnectFourAgent(color="tdColor", depth=depth, algorithm="TDAlphaBeta", tdEvaluator=tdLearner)
		minimaxAgent = agent.ConnectFourAgent(color="minimaxColor", depth=depth, algorithm="minimax")

		if tdColor == "R":
			game = connect_four.ConnectFourGame(firstPlayer=tdAlphaBetaAgent, secondPlayer=minimaxAgent)
		else:
			game = connect_four.ConnectFourGame(firstPlayer=minimaxAgent, secondPlayer=tdAlphaBetaAgent)

		winner = game.play(display=False)
		results[winner][0] += 1
		results[winner][1] += game.numMoves

	print(results)
	
def playTDAgainstMinimax(opponentColor, tdAgent=None, nGames=50, depth=1):
	"""Pure td learning against minimax."""
	tdAgent.color = "R" if opponentColor == "B" else "B"

	if opponentColor == "R":
		firstPlayer = agent.ConnectFourAgent(name="minimaxAgent", color="R", depth=depth)
		secondPlayer = tdAgent  
	else:
		firstPlayer = tdAgent
		secondPlayer = agent.ConnectFourAgent(name="minimaxAgent", color="B", depth=depth)

	results = {"R": 0, "B": 0, "Draw": 0}

	for it in range(nGames):
		results[(ConnectFourGame(firstPlayer, secondPlayer, silent=True).play(display=False))] += 1
	return results 

if __name__=="__main__":
	restorePath = "./model_ckpt400000"
	#playAgainstHuman(agentColor="R", humanColor="B", restorePath=restorePath, depth=3)
	playAgainstMinimax(10, "B", "R", restorePath, depth=6)
	#playAgainstMinimax(20, "R", "B", restorePath, depth=5)
	# playAgainstMinimax(10, "B", "R", restorePath) 

	# Results
	# depth 1, td Red results: {'R': [58, 780], 'B': [42, 662], 'Draw': [0, 0]}
	# depth 1, td Black: {'R': [53, 653], 'B': [47, 660]}
	


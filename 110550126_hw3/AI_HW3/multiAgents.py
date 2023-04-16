from util import manhattanDistance
from game import Directions
import random, util
from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        minGhostDistance = min([manhattanDistance(newPos, state.getPosition()) for state in newGhostStates])

        scoreDiff = childGameState.getScore() - currentGameState.getScore()

        pos = currentGameState.getPacmanPosition()
        nearestFoodDistance = min([manhattanDistance(pos, food) for food in currentGameState.getFood().asList()])
        newFoodsDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        newNearestFoodDistance = 0 if not newFoodsDistances else min(newFoodsDistances)
        isFoodNearer = nearestFoodDistance - newNearestFoodDistance

        direction = currentGameState.getPacmanState().getDirection()
        if minGhostDistance <= 1 or action == Directions.STOP:
            return 0
        if scoreDiff > 0:
            return 8
        elif isFoodNearer > 0:
            return 4
        elif action == direction:
            return 2
        else:
            return 1


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (Part 1)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        # Begin your code (Part 1)
        
        
        def minimax(state,depth,agent):
            if depth==0 or state.isLose() or state.isWin():
                return 0,self.evaluationFunction(state)
            
            next_depth = depth
            next_agent = (agent+1) % state.getNumAgents()
            if agent == state.getNumAgents()-1:
                next_depth = depth -1

            legal_act = state.getLegalActions(agent)
            next_state = [state.getNextState(agent, act) for act in legal_act]
            next_value = [minimax(nextstate,next_depth,next_agent)[1] for nextstate in next_state]

            if agent ==0: #pacman
                ans_value = max(next_value)
            else: #ghost
                ans_value = min(next_value)
            possible_index = []
            for i in range(len(next_value)):
                if next_value[i]==ans_value:
                    possible_index.append(i)
            ans_index = random.choice(possible_index)
            
            return legal_act[ans_index] , ans_value
        return minimax(gameState,self.depth,0)[0]
        # End your code (Part 1)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (Part 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        
        # Begin your code (Part 2)
        
        def alphabeta(state,depth,agent,alpha,beta):
            if depth==0 or state.isLose() or state.isWin():
                return 0,self.evaluationFunction(state)

            next_agent = (agent+1) % state.getNumAgents()
            next_depth = depth
            if agent == state.getNumAgents()-1:
                next_depth = depth -1

            legal_act = state.getLegalActions(agent)
            if agent ==0:
                ans_value = float('-Inf')
                for action  in legal_act:
                    next_state = state.getNextState(agent, action)
                    next_value = alphabeta(next_state,next_depth,next_agent,alpha,beta)[1]
                    if ans_value < next_value:
                        ans_value = next_value
                        ans_action = action
                    if ans_value > beta:
                        return  action,ans_value
                    alpha = max(alpha,ans_value)
                return ans_action, ans_value
                
            else:
                ans_value = float('Inf')
                for action  in legal_act:
                    next_state = state.getNextState(agent, action)
                    next_value = alphabeta(next_state,next_depth,next_agent,alpha,beta)[1]
                    if ans_value > next_value:
                        ans_value = next_value
                        ans_action = action
                    if ans_value < alpha:
                        return  action,ans_value
                    beta = min(beta,ans_value)
                return ans_action, ans_value
            """
            
            next_value = []
            next_action = []
            
            
            
            
            
            if agent == 0:
                ans_value = float('-Inf')
            else:
                ans_value = float('Inf')
            for action in legal_act:
                next_state = state.getNextState(agent, action)
                next_value = alphabeta(next_state,next_depth,next_agent,alpha,beta)[1]
                if agent == 0:
                    if next_value >beta:
                        return action,beta
                
                    alpha = max(next_value,alpha)
                    if next_value >ans_value:
                        ans_value = next_value
                        ans_action = action
                else:
                    if next_value <alpha:
                        return action,alpha
                    
                    beta  = min(beta,next_value)
                    
                    if next_value < ans_value:
                        ans_value=  next_value
                        ans_action = action
            return ans_action, ans_value"""
                        
                            
            """   next_value.append(value)
                next_action.append(action)
            if agent ==0:
                ans_value = max(next_value)
            else:
                ans_value = min(next_value)
            possible_index = []
            for i in range(next_value):
                if next_value[i]==ans_value:
                    possible_index.append(i)
            ans_index = random.choice(possible_index)
            return next_action[ans_index], ans_value         """        
        return alphabeta(gameState,self.depth,0,float('-Inf'),float('Inf'))[0]
        # End your code (Part 2)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (Part 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        # Begin your code (Part 3)
        raise NotImplementedError("To be implemented")
        # End your code (Part 3)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (Part 4).
    """
    # Begin your code (Part 4)
    raise NotImplementedError("To be implemented")
    # End your code (Part 4)

# Abbreviation
better = betterEvaluationFunction

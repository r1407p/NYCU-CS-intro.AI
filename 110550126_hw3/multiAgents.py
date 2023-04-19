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
class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (Part 1)
    """
    def getAction(self, gameState):
        # Begin your code (Part 1)
        """
        we should return the action that the pacman will take.
        
        the architecture of my implement is use recurrsive dfs method to build an search tree.
        
        we construct a function of minimax with parameters: state, depth, agent.
        and return the value and which action should take (construct the tree need value, answer need action)
        
        first we detect the tree is finish or not depand on depth or the game is end, 
        and return action(stop,value)
        
        second, we compute the next parameters that need to pass into next iterate function,
        
        based on the agent (pacman or ghost)
        we chooose the max value or min value in all possible state
        and we return the value with its correesponding action.
        """    
        
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
        """
        we should return the action that the pacman will take.
        
        the architecture of my implement is use recurrsive dfs method to build an search tree.
        
        we construct a function of alphabeta with parameters: state, depth, agent, alpha beta.
        and return the value and which action should take (construct the tree need value, answer need action)
        
        first we detect the tree is finish or not depand on depth or the game is end, 
        and return action(stop,value)
        
        second, we compute the next parameters that need to pass into next iterate function,
        
        based on the agent (pacman or ghost)
        
        if the agent is pacman(want to make value bigger)
        we initial the answer value be -inf
        for every next state, we can update alpha, beta and answer
        if next state value > answer, make answer =next state value
        if answer > upper bound(beta) return value and action
        update the lower bound(alpha)
        if the iteration finish return the answer value and action
        
        if the agent is ghost(want to make value bigger)
        we initial the answer value be inf
        for every next state, we can update alpha, beta and answer
        if next state value < answer, make answer =next state value
        if answer < lower bound(alpha) return value and action
        update the upper bound(beta)
        if the iteration finish return the answer value and action
        """    
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
                        ans_action = [action]
                    elif ans_value ==next_value:
                        ans_action.append(action)
                    if ans_value > beta:
                        return  action,ans_value
                    alpha = max(alpha,ans_value)
                return random.choice(ans_action), ans_value            
            else:
                ans_value = float('Inf')
                for action  in legal_act:
                    next_state = state.getNextState(agent, action)
                    next_value = alphabeta(next_state,next_depth,next_agent,alpha,beta)[1]
                    if ans_value > next_value:
                        ans_value = next_value
                        ans_action = [action]
                    elif ans_value==next_value:
                        ans_action.append(action)
                    if ans_value < alpha:
                        return  action,ans_value
                    beta = min(beta,ans_value)
                return random.choice(ans_action), ans_value
                    
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
        """ 
        we construct a function of expectimax with parameters: state, depth, agent.
        and return the value and which action should take (construct the tree need value, answer need action)
        
        first we detect the tree is finish or not depand on depth or the game is end, 
        and return action(stop,value)
        
        second, we compute the next parameters that need to pass into next iterate function,
        
        based on the agent (pacman or ghost)
        if the agent is pacman the process is same as the part1
        
        but for the ghost, since the ghosts' action is random we need to return the average value 
        to simulate the real action of ghost
        """
        def expectimax(state,depth,agent):
            if depth ==0 or state.isWin() or state.isLose():
                return 0,self.evaluationFunction(state)
            
            next_agent = (agent+1)%state.getNumAgents()
            next_depth  = depth
            if agent == state.getNumAgents()-1:
                next_depth = depth -1
            
            legal_act = state.getLegalActions(agent)
            
            next_state = [state.getNextState(agent, act) for act in legal_act]
            next_value = [expectimax(nextstate,next_depth,next_agent)[1] for nextstate in next_state]
            if agent ==0:
                ans_value = max(next_value)
                for i in range(len(next_value)):
                    if next_value[i] == ans_value:
                        return legal_act[i], ans_value
            else:
                return 0, sum(next_value)/len(next_value)
            
        return expectimax(gameState,self.depth,0)[0]
    
        # End your code (Part 3)


def betterEvaluationFunction(currentGameState):
    
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (Part 4).
    """
    """
    first, from the gamestate, wecan get information about the food, pac-man and ghost
    calculate the score of the state from three part
    1.ghost score:
        if ghost is scared: we want to eat the ghost -> the closer to ghost, the higher score
        if ghost is not scared: we want to leave the ghost -> the farer to ghost, the higher score
    2.food score:
        the more food is on the map the lower score we get
        the closer to food the higher score we get
    3.capsules score:
        the more food is on the map the lower score we get
        the closer to food the higher score we get
        note that the weight of capsules is greater than food
    """
    
    # Begin your code (Part 4)
    pac_pos = currentGameState.getPacmanPosition()
    
    
    ghost_states = currentGameState.getGhostStates()
    ghost_pos = currentGameState.getGhostPositions()
    
    scared_times = [g_s.scaredTimer for g_s in ghost_states]
    ghost_distance = [util.manhattanDistance(pac_pos,g_p)for g_p in ghost_pos]
    
    ghost_score = 0
    scared_time = sum(scared_times)
    min_ghost_distance = min(ghost_distance)

    if scared_time > 1:
        if min_ghost_distance==0:
            ghost_score+=600
        else:
            ghost_score +=300/min_ghost_distance
    else:
        if min_ghost_distance==0:
            ghost_score -=100
        elif min_ghost_distance<5:
            ghost_score -= 20/min_ghost_distance
    
    food = currentGameState.getFood()
    food = food.asList()
    food_distance = [util.manhattanDistance(pac_pos,f_p) for f_p in food]
    
    food_score = -5*len(food_distance)
    if len(food_distance)>0:
        min_food_distance = min(food_distance)
        food_score +=10/min_food_distance+10    
        
    capsules = currentGameState.getCapsules()
    #print(capsules_distance)
    capsules_score = len(capsules)*(-100)
    return food_score+ghost_score+currentGameState.getScore()+capsules_score
    # End your code (Part 4)

# Abbreviation
better = betterEvaluationFunction

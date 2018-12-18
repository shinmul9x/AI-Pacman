# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        foodPos = newFood.asList() #get food position
        foodCount = len(foodPos) #get num of food
        closestDistance = 1e6
        for i in xrange(foodCount):
          distance = manhattanDistance(foodPos[i],newPos) + foodCount*100
          if distance < closestDistance:
            closestDistance = distance
        if foodCount == 0 :
          closestDistance = 0
        score = -closestDistance

        for i in xrange(len(newGhostStates)):
          ghostPos = successorGameState.getGhostPosition(i+1)
          if manhattanDistance(newPos,ghostPos)<=1 :
            score -= 1e6

        # return successorGameState.getScore()
        return score

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
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
      """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
          Returns a list of legal actions for an agent
          agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
          Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
          Returns the total number of agents in the game
      """
      "*** YOUR CODE HERE ***"

      # apply for pacman
      def maxValue(state, depth):
        value = -999999
        if state.isWin() or state.isLose() or (depth + 1) == self.depth: 
          return self.evaluationFunction(state)
        actions = state.getLegalActions(0)
        for action in actions:
          successor = state.generateSuccessor(0, action)
          value = max(value, minValue(successor, depth + 1, 1))
        return value
      
      # apply for all ghost
      def minValue(state, depth, agentIndex):
        value = 999999
        if state.isWin() or state.isLose():
          return self.evaluationFunction(state)
        actions = state.getLegalActions(agentIndex)
        for action in actions:
          successor = state.generateSuccessor(agentIndex, action)
          if agentIndex == (state.getNumAgents() - 1):
            value = min(value, maxValue(successor, depth))
          else:
            value = min(value, minValue(successor, depth, agentIndex + 1))
        return value
      
      actions = gameState.getLegalActions(0)
      value = -999999
      for action in actions:
        nextState = gameState.generateSuccessor(0, action)
        score = minValue(nextState, 0, 1)
        if score > value:
          returnAction = action
          value = score
      return returnAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
      """
        Returns the minimax action using self.depth and self.evaluationFunction
      """
      "*** YOUR CODE HERE ***"

      def maxValue(gameState, depth, alpha, beta):
        value = -999999
        if gameState.isWin() or gameState.isLose() or (depth + 1)==self.depth:
          return self.evaluationFunction(gameState)
        actions = gameState.getLegalActions(0)
        _alpha = alpha
        for action in actions:
          successor = gameState.generateSuccessor(0, action)
          value = max(value, minValue(successor, depth + 1, 1 , _alpha, beta))
          if value > beta:
            return value
          _alpha = max(_alpha, value)
        return value

      def minValue(gameState, depth, agentIndex, alpha, beta):
        value = 999999
        if gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState)
        actions = gameState.getLegalActions(agentIndex)
        _beta = beta
        for action in actions:
          successor = gameState.generateSuccessor(agentIndex, action)
          if agentIndex == (gameState.getNumAgents() - 1):
            value = min(value, maxValue(successor, depth, alpha, _beta))
            if value < alpha:
              return value
            _beta = min(_beta,value)
          else:
            value = min(value, minValue(successor, depth, agentIndex + 1, alpha, _beta))
            if value < alpha:
              return value
            _beta = min(_beta, value)
        return value

      actions = gameState.getLegalActions(0)
      value = -999999
      alpha = -999999
      beta = 999999
      for action in actions:
        nextState = gameState.generateSuccessor(0, action)
        score = minValue(nextState, 0, 1, alpha, beta)
        if score > value:
          returnAction = action
          value = score
        if score > beta:
          return returnAction
        alpha = max(alpha, score)
      return returnAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
      """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
      """
      "*** YOUR CODE HERE ***"
      def maxValue(gameState, depth):
        if gameState.isWin() or gameState.isLose() or depth + 1 == self.depth:
          return self.evaluationFunction(gameState)
        value = -999999
        actions = gameState.getLegalActions(0)
        for action in actions:
          successor = gameState.generateSuccessor(0, action)
          value = max(value, expectValue(successor, depth + 1, 1))
        return value
      
      def expectValue(gameState, depth, agentIndex):
        if gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState)
        actions = gameState.getLegalActions(agentIndex)
        totalvalue = 0
        numberofactions = len(actions)
        if numberofactions == 0:
          return  0
        for action in actions:
          successor= gameState.generateSuccessor(agentIndex,action)
          if agentIndex == (gameState.getNumAgents() - 1):
            value = maxValue(successor, depth)
          else:
            value = expectValue(successor, depth, agentIndex+1)
          totalvalue += value
        return float(totalvalue)/float(numberofactions)
      
      actions = gameState.getLegalActions(0)
      value = -999999
      for action in actions:
        nextState = gameState.generateSuccessor(0, action)
        score = expectValue(nextState, 0, 1)
        if score > value:
          returnAction = action
          value = score
      return returnAction

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    
    foodList = newFood.asList()
    from util import manhattanDistance
    foodDistance = [0]
    for pos in foodList:
      foodDistance.append(manhattanDistance(newPos,pos))

    ghostPos = []
    for ghost in newGhostStates:
      ghostPos.append(ghost.getPosition())
    ghostDistance = [0]
    for pos in ghostPos:
      ghostDistance.append(manhattanDistance(newPos,pos))

    numberofPowerPellets = len(currentGameState.getCapsules())
    score = 0
    numberOfNoFoods = len(newFood.asList(False))           
    sumScaredTimes = sum(newScaredTimes)
    sumGhostDistance = sum (ghostDistance)
    reciprocalfoodDistance = 0
    if sum(foodDistance) > 0:
      reciprocalfoodDistance = 1.0 / sum(foodDistance) 
    score += currentGameState.getScore()  + reciprocalfoodDistance + numberOfNoFoods
    if sumScaredTimes > 0:    
      score +=   sumScaredTimes + (-1 * numberofPowerPellets) + (-1 * sumGhostDistance)
    else :
      score +=  sumGhostDistance + numberofPowerPellets
    return score

# Abbreviation
better = betterEvaluationFunction


# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

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

  def calculateDistance(self,p1,p2):
      return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

  def closestGhostDistance(self, pacman, ghosts):
      dist = 99999
      for ghost in ghosts:
          newDist = calculateDistance(pacman, ghost)
          if newDist < dist:
              dist = newDist
      return dist

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    currentPos = currentGameState.getPacmanPosition()
    newPos = successorGameState.getPacmanPosition()
    newX, newY = newPos
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    ghostPositions = currentGameState.getGhostPositions()
    caps = currentGameState.getCapsules()
    foodList = oldFood.asList()
    oldamountOfFood = currentGameState.getNumFood()
    newamountOfFood = successorGameState.getNumFood()
    "*** YOUR CODE HERE ***"

    def calculateDistance(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def closestGhostValue(pacman, ghosts):
        dist = 99999
        for ghost in ghosts:
            newDist = calculateDistance(pacman, ghost)
            if newDist < dist:
                dist = newDist
        if dist < 3:
            return -999999
        else:
            return dist


    def furthestFood():
        maxDist = 0
        for f in foodList:
            d = calculateDistance(newPos, f)
            if d > maxDist:
                maxDist = d
        return maxDist

    def closestFood():
        minDist = 99999
        for f in foodList:
            d = calculateDistance(newPos, f)
            if d < minDist:
                minDist = d
        return minDist

    def eatFood():
        if not (oldamountOfFood - newamountOfFood) == 0:
            return 1000
        else:
            return 0


    closestGhost = closestGhostValue(newPos, ghostPositions)
    furthestFood = furthestFood()
    closestFood = closestFood()
    hungry = eatFood()
    value = closestGhost + furthestFood*0.1 - closestFood*20000 + hungry

    print("closest ghost: " + str(closestGhost) + "     closest food: " + str(closestFood) + "     furthestFood: " + str(furthestFood) + "     amount of food left: " + str(newamountOfFood) + "     value: " + str(value))

    return value

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
    Your minimax agent for one opponent (assignment 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """

    def minimax(node, depth, pacmansturn):
        if node.isWin() or node.isLose():
            terminal = True
        else:
            terminal = False

        if depth == 0 or terminal:
            return self.evaluationFunction(node)

        if pacmansturn:
            bestVal = -99999
            legalActions = node.getLegalPacmanActions()
            successors = []
            for action in legalActions:
                successors.append(node.generatePacmanSuccessor(action))

            for successor in successors:
                value = minimax(successor, depth-1, False)
                bestVal = max(bestVal,value)

            return bestVal

        else:
            bestVal = 99999
            legalActions = node.getLegalActions(1)
            successors = []
            for action in legalActions:
                successors.append(node.generateSuccessor(1, action))

            for successor in successors:
                value = minimax(successor, depth-1, True)
                bestVal = min(bestVal, value)
            return bestVal

    legalActions = gameState.getLegalPacmanActions()
    bestAction = None
    bestUtility = -99999

    for action in legalActions:
        successor = gameState.generatePacmanSuccessor(action)
        utility = minimax(successor, self.depth, False)
        if utility > bestUtility:
            bestUtility = utility
            bestAction = action

    print (bestUtility)
    return bestAction

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning for one ghost (assignment 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    #using pseudocode for alpha beta with cutoff depth from wikipedia
    def alphabeta(node, a, b, depth, maxNode):
        if node.isWin() or node.isLose():
            terminal = True
        else:
            terminal = False

        if depth == 0 or terminal:
            return self.evaluationFunction(node)

        elif maxNode:
            #a = -99999
            #generate Successors:
            legalActions = node.getLegalPacmanActions()
            successors = []
            for action in legalActions:
                successors.append(node.generatePacmanSuccessor(action))

            for successor in successors:
                a = max(a, alphabeta(successor, a, b, depth-1, False))
                if b <= a:
                    return b
                    #break
            return a

        else:
            #b = 99999

            # generate Successors:
            legalActions = node.getLegalPacmanActions()
            successors = []
            for action in legalActions:
                successors.append(node.generatePacmanSuccessor(action))

            for successor in successors:
                b = min(b, alphabeta(successor, a, b, depth-1, True))
                if b <= a:
                    return a
                    #break
            return b

    legalActions = gameState.getLegalPacmanActions()
    bestAction = None
    bestUtility = -99999

    for action in legalActions:
        successor = gameState.generatePacmanSuccessor(action)
        utility = alphabeta(successor, -99999, 99999, self.depth, False)
        if utility > bestUtility:
            bestUtility = utility
            bestAction = action
    print(bestUtility)
    return bestAction

class MultiAlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning for several ghosts (Extra credit assignment B)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()    

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (not used in this course)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function for one ghost (extra credit assignment A).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest (not used in this course)
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


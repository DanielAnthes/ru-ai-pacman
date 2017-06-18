# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance, nearestPoint
from game import Directions, Agent
import random, util
import distanceCalculator


class CompetitionAgent(Agent):
    """
    A base class for competition agents.  The convenience methods herein handle
    some of the complications of the game.
  
    Recommended Usage:  Subclass CompetitionAgent and override getAction.
    """

    #############################
    # Methods to store key info #
    #############################

    def __init__(self, index=0, timeForComputing=.1):
        """
        Lists several variables you can query:
        self.index = index for this agent
        self.distancer = distance calculator (contest code provides this)
        self.timeForComputing = an amount of time to give each turn for computing maze distances
            (part of the provided distance calculator)
        """
        # Agent index for querying state, N.B. pacman is always agent 0
        self.index = index

        # Maze distance calculator
        self.distancer = None

        # Time to spend each turn on computing maze distances
        self.timeForComputing = timeForComputing

        # Access to the graphics
        self.display = None

        # useful function to find functions you've defined elsewhere..
        # self.usefulFunction = util.lookup(usefulFn, globals())

    def registerInitialState(self, gameState):
        """
        This method handles the initial setup of the
        agent to populate useful fields.
        
        A distanceCalculator instance caches the maze distances 
        between each pair of positions, so your agents can use:
        self.distancer.getDistance(p1, p2)
        """
        self.distancer = distanceCalculator.Distancer(gameState.data.layout)

        # uncomment this line to use maze-distances (instead of manhattan distances as default.)
        self.distancer.getMazeDistances()
        print("calculated distances")

        #TODO rewrite this function, it's ugly
        def surroundingWalls(xpos, ypos, width, height):
            walls = gameState.getWalls()
            numberOfWalls = 0
            #if coordinates belong to point in the border return immediately
            if xpos == 0 or xpos == width-1 or ypos == 0 or ypos == height-1:
                return 999
            else:
                if walls[xpos][ypos-1] == True:
                    numberOfWalls+=1

                if walls[xpos][ypos+1] == True:
                    numberOfWalls+=1

                if walls[xpos+1][ypos] == True:
                    numberOfWalls += 1

                if walls[xpos-1][ypos] == True:
                    numberOfWalls+=1

                return numberOfWalls


        def findKeyPositions():
            walls = gameState.getWalls()
            wallgridHeight = walls.height
            wallgridWidth = walls.width
            # initialize deadends and crossroads with False for every position
            deadends = []
            crossroads = []

            crossroadlist = []

            for x in range(wallgridWidth): # THIS NEVER EVALUATES CORRECTLY! IS IT POSSIBLE THAT THE GRID IS NOT FILLED CORRECTLY? X is still not incremented correctly, only increments once
                deadendscol = []
                crossroadscol = []
                for y in range(wallgridHeight):
                    numberOfWalls = surroundingWalls(x,y, wallgridWidth,wallgridHeight)
                    if numberOfWalls > 2:
                        deadendscol.append(True)

                    else:
                        deadendscol.append(False)
                    if numberOfWalls < 2:
                        crossroadscol.append(True)
                        if not walls[x][y]:
                            crossroadlist.append((x,y))
                    else:
                        crossroadscol.append(False)

                deadends.append(deadendscol)
                crossroads.append(crossroadscol)

            # in one pass over the map calculate the number of walls next to each position and update crossroads and deadends
            #for x in range(wallgridWidth):
            #    for y in range(wallgridHeight):
            #        if surroundingWalls(x, y) < 2:
            #            deadends[x][y] = True
            #        elif surroundingWalls(x, y) > 2:  # you reversed the conditions
            #            crossroads[x][y] = True
                        # add x,y to list of crossroads
            print("initial calculations completed")
            return crossroads, deadends, crossroadlist

        self.crossroads, self.deadends, self.crossroadslist = findKeyPositions()

        import __main__
        if '_display' in dir(__main__):
            self.display = __main__._display

    #################
    # Action Choice #
    #################



    def getAction(self, gameState):
        """
        Override this method to make a good agent. It should return a legal action within
        the time limit (otherwise a random legal action will be chosen for you).
        """
        util.raiseNotDefined()

    #######################
    # Convenience Methods #
    #######################

    def getFood(self, gameState):
        """
        Returns the food you're meant to eat. This is in the form of a matrix
        where m[x][y]=true if there is food you can eat (based on your team) in that square.
        """
        return gameState.getFood()

    def getCapsules(self, gameState):
        return gameState.getCapsules()

    def getScore(self, gameState):
        """
        Returns how much you are beating the other team by in the form of a number
        that is the difference between your score and the opponents score.  This number
        is negative if you're losing.
        """
        return gameState.getScore()

    def getMazeDistance(self, pos1, pos2):
        """
        Returns the distance between two points; These are calculated using the provided
        distancer object.
    
        If distancer.getMazeDistances() has been called, then maze distances are available.
        Otherwise, this just returns Manhattan distance.
        """
        d = self.distancer.getDistance(pos1, pos2)
        return d


class BaselineAgent(CompetitionAgent):
    """
      This is a baseline reflex agent to see if you can do better.
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.
    """

    def getAction(self, gameState):
        """
        getAction chooses among the best options according to the evaluation function.
    
        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """

        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # try each of the actions and pick the best one
        scores = []
        for action in legalMoves:
            successorGameState = gameState.generatePacmanSuccessor(action)
            scores.append(self.evaluationFunction(successorGameState))

        # get the best action
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"
        return legalMoves[chosenIndex]

    def evaluationFunction(self, state):
        # Useful information you can extract from a GameState (pacman.py)
        return state.getScore()


class TimeoutAgent(Agent):
    """
    A random agent that takes too much time. Taking
    too much time results in penalties and random moves.
    """

    def __init__(self, index=0):
        self.index = index

    def getAction(self, state):
        import random, time
        time.sleep(2.0)
        return random.choice(state.getLegalActions(self.index))










###TODO OUR AGENT###

###TODO Change Back max startup time in pacman.py, currently set to infinity for testing
class MyPacmanAgent(CompetitionAgent):
    """
    This is going to be your brilliant competition agent.
    You might want to copy code from BaselineAgent (above) and/or any previos assignment.
    """

    # The following functions have been declared for you,
    # but they don't do anything yet (getAction), or work very poorly (evaluationFunction)

    def getAction(self, gameState):
        """
        getAction chooses among the best options according to the evaluation function.
        Just like in the previous projects, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}.
        """



        if len(gameState.getGhostStates())>3:
            self.depth = 2
        else:
            self.depth = 1

        a = self.minimax(gameState, True, self.depth, gameState)
        return a[1]

    def isTrapped(self, currentGameState):
        pacman = currentGameState.getPacmanPosition()
        walls_around_pacman = 0
        for x in range(3):
            for y in range(3):
                if currentGameState.getWalls()[pacman[0] - x + 1][pacman[1] - y + 1] and (x - 1 == 0 or y - 1 == 0):
                    walls_around_pacman += 1
        if walls_around_pacman >= 3:
            return True
        else:
            return False

    def isTerminal(self, gameState):
        return gameState.isWin() or gameState.isLose()

    def getSenarios(self, actionslist):
        if actionslist == []:
            return [[]]
        else:
            list = self.getSenarios(actionslist[1:])
            list3 = []
            # i = 0
            for a in actionslist[0]:
                list2 = []
                for l in list:
                    list2.append([])
                    for item in l:
                        list2[list2.__len__() - 1].append(item)
                for i in range(list2.__len__()):
                    list2[i].append(a)
                for item in list2:
                    list3.append(item)
            return list3

    def getSuccessor(self, gameState, actions):
        successor = gameState
        for action in actions:
            successor = successor.generateSuccessor(action[1], action[0])
            if self.isTerminal(successor):
                return successor
        return successor

    def minimax(self, gameState, maxi, depth, initialGameState):
        if self.isTerminal(gameState) or depth == 0:
            return (self.evaluationFunction(gameState, initialGameState), Directions.STOP)

        childeren = util.PriorityQueue()
        if maxi:
            actions = gameState.getLegalActions(0)
            for a in actions:
                succsorGamestate = gameState.generateSuccessor(0, a)
                child = self.minimax(succsorGamestate, not maxi, depth - 1, initialGameState)
                childeren.push((child[0], a), -child[0])
        if not maxi:
            actionslists = []
            for i in range(gameState.getNumAgents() - 1):
                actionsghost = []
                for a in gameState.getLegalActions(i + 1):
                    actionsghost.append((a, i + 1))
                actionslists.append(actionsghost)
            actions = self.getSenarios(actionslists)
            for a in actions:
                succsorGamestate = self.getSuccessor(gameState, a)
                child = self.minimax(succsorGamestate, not maxi, depth, initialGameState)
                childeren.push((child[0], a), child[0])
        return childeren.pop()








    def evaluationFunction(self, state, initialState):



        ###gather information for later use###

        #game state, food, pacman position
        currentGameState = state
        Pos = currentGameState.getPacmanPosition()
        oldPos = initialState.getPacmanPosition()
        Food = currentGameState.getFood()

        #amount of food in old + new game state
        newFoodCount = currentGameState.getNumFood()
        oldFoodCount = initialState.getNumFood()


        #amount of capsules in old and new state
        oldCapsuleCount = len(initialState.getCapsules())
        newCapsuleCount = len(currentGameState.getCapsules())


        #distances to ghosts and scared ghosts  in old and new states
        GhostStates = currentGameState.getGhostStates()
        ghostDistance = [ self.distancer.getDistance(Pos, ghost.configuration.pos) for ghost in GhostStates if
                         ghost.scaredTimer == 0]

        ghostPositions = [ghost.configuration.pos for ghost in GhostStates if ghost.scaredTimer == 0]

        scaredDistance = [ self.distancer.getDistance(Pos, ghost.configuration.pos) for ghost in GhostStates if
                          ghost.scaredTimer != 0]

        oldGhostStates = initialState.getGhostStates()
        oldGhostDistance = [self.distancer.getDistance(Pos, ghost.configuration.pos) for ghost in oldGhostStates if
                         ghost.scaredTimer == 0]
        oldScaredDistance = [self.distancer.getDistance(Pos, ghost.configuration.pos) for ghost in oldGhostStates if
                          ghost.scaredTimer != 0]


        #distances to crossroads, sorted by increasing distance
        crossRoadDistance =[(self.distancer.getDistance(Pos, crossroad),crossroad) for crossroad in self.crossroadslist]
        crossRoadDistance.sort(key=lambda tup: tup[0])


        #amount of ghosts and scared ghosts
        amountOfGhosts = len(ghostDistance)
        amountOfScaredGhosts = len(scaredDistance)

        oldAmountOfGhosts = len(oldGhostDistance)
        oldAmountOfScaredGhosts = len(oldScaredDistance)


        if scaredDistance:
            closestScared = min(scaredDistance)
        else:
            closestScared = 999

        if ghostDistance:
            closestGhost = min(ghostDistance)
        else:
            closestGhost = 999




        ###calculations###


        dangerousCorridor = 0
        #check if pacman currently is on a crossroad position
        if oldPos in self.crossroadslist:
            onCrossroad = True
        else:
            onCrossroad = False

        #calculate distance to the next crossroad (excluding the one pacman is currently on)

        if onCrossroad:
            ghosts = 0
            nextCrossroad = crossRoadDistance[1][1]
            distMeCrossroad = self.distancer.getDistance(Pos, nextCrossroad)
            for ghost in ghostPositions:
                distMeGhost = self.distancer.getDistance(Pos, ghost)
                distGhostCrossroad = self.distancer.getDistance(ghost, nextCrossroad)
                if (distMeGhost + distGhostCrossroad) == distMeCrossroad:
                    ghosts+=1
            if ghosts > 0:
                dangerousCorridor = 9000


        #ghosts eaten in this step
        numberOfEatenGhosts = (oldAmountOfScaredGhosts - amountOfScaredGhosts)
        if numberOfEatenGhosts > 0:
            numberOfEatenGhosts = float("Inf")

        #TODO dont go for capsules if ghost in path

        #sum of distances to all ghosts
        if ghostDistance:
            sumOfGhosts = sum(ghostDistance)
        else:
            sumOfGhosts = 99999

        #sum of distance to all scared ghosts and the closest scared ghost, if the closest scared ghost is closer than 10 steps closeScared is set to 1 and closestScared increases as pacman gets closer to the scared ghost
        if scaredDistance:
            sumOfScared = sum(scaredDistance)


            if closestScared < 10:
                closeScared = 1
                closestScared = (10 - closestScared)*5000
                #additional modifier if a ghost is dangerously close
                if closestGhost < 3:
                    closestScared = closestScared - 40000

            else:
                closeScared = 0
        else:
            sumOfScared = 0
            closeScared = 0

        #value that evaluates states better if ghosts are far away and scared ghosts are close
        ghostDistances = sumOfGhosts - sumOfScared


        #evaluate whether we ate a capsule
        if not ((oldCapsuleCount - newCapsuleCount) == 0):
            ateCapsule = True
        else:
            ateCapsule = False

        huntGhosts = 0


        #nearbyGhost=
        #for ghost in GhostStates:
        #    if dist(pos,ghost) < nearbyGhost
        #        nearbyGhos=ghost

        #TODO add cumulative dist to all ghosts


        #distances to capsules
        capsuleDist = [ self.distancer.getDistance(Pos, capsule) for capsule in currentGameState.getCapsules()]


        #list of positions with food
        foodlist = []
        for h in range(Food.height):
            for w in range(Food.width):
                if Food[w][h]:
                    foodlist.append((w, h))
        foodDist = [ self.distancer.getDistance(Pos, food) for food in foodlist]


        #calculate furthest distance to food
        if foodDist:
            furthestFood = max(foodDist)
        else:
            furthestFood = 0


        #calculate closest food
        if foodDist:
            closestFood = min(foodDist)
        else:
            closestFood = 0

        #closest ghost
        if ghostDistance:
            closestGhost = min(ghostDistance)
            if closestGhost < 5:
                (5-closestGhost)*-10000000

        else:
            closestGhost = 99999

        #if its closer than say 5 just do 5 - closest and multiply it by a high value
            # if closestGhost < 2:
            # closestGhost = -float("Inf")

        #if we can eat a capsule and ghosts are close, eat the capsule
        if scaredDistance:
            closestScaredGhost = min(scaredDistance)
            if (closestScaredGhost < 8) and ateCapsule:
                huntGhosts = 500000
        else:
            huntGhosts = 0

        # first setup for 'trapped' function. We could play around with
        # Ghostdistance
        # the amount of food left for when you want pacman to be balsy (last pellet, last two?)
        trapped=0
        if (closestGhost<3) and (self.isTrapped(state)):
                if not newFoodCount<3:
                    trapped=-float("Inf")

        #Code from baseline agent. Seems pretty useless but hey, why not?
        if currentGameState.isLose():
            return -float("Inf")

        foodValue = (oldFoodCount - newFoodCount)

        #TODO @win: I added the current gameScore to the eval function. Discuss if this is valuable or not
        return -closestFood*10 + closestGhost + furthestFood*0.1 + foodValue*5000 + ghostDistances*2 + huntGhosts + numberOfEatenGhosts + currentGameState.getScore() + closeScared*closestScared - dangerousCorridor + trapped




    def evaluationFunctionBaseline(self, state):
        """
        A very poor evsaluation function. You can do better!
        """
        # print ("test")
        currentGameState = state
        Pos = currentGameState.getPacmanPosition()
        Food = currentGameState.getFood()
        GhostStates = currentGameState.getGhostStates()
        ghostDistance = [util.manhattanDistance(Pos, ghost.configuration.pos) for ghost in GhostStates if
                         ghost.scaredTimer == 0]
        scaredDistance = [util.manhattanDistance(Pos, ghost.configuration.pos) for ghost in GhostStates if
                          ghost.scaredTimer != 0]
        capsuleDist = [util.manhattanDistance(Pos, capsule) for capsule in currentGameState.getCapsules()]
        foodlist = []
        for h in range(Food.height):
            for w in range(Food.width):
                if Food[w][h]:
                    foodlist.append((w, h))
        foodDist = [util.manhattanDistance(Pos, food) for food in foodlist]

        if foodDist == []:
            return float("Inf")
        if currentGameState.isLose():
            return -float("Inf")
        if currentGameState.isWin():
            return 100000000
            #  return -min(ghostDistance) - random.choice(range(4))
        if self.isTrapped(currentGameState):
            return -float("Inf")
        if ghostDistance == []:
            return - min(foodDist) - min(scaredDistance) + currentGameState.getScore() - 100 * len(
                capsuleDist) + random.choice(range(10))
        return - min(foodDist) + min(ghostDistance) + currentGameState.getScore() - 100 * len(
            capsuleDist) + random.choice(range(10))

        return min(foodDist) * currentGameState.getScore() * min(ghostDistance)

# MyPacmanAgent=BaselineAgent

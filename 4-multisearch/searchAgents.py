# searchAgents.py
# ---------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
This file contains all of the agents that can be selected to
control Pacman.  To select an agent, use the '-p' option
when running pacman.py.  Arguments can be passed to your agent
using '-a'.  For example, to load a SearchAgent that uses
depth first search (dfs), run the following command:

> python pacman.py -p SearchAgent -a fn=depthFirstSearch

Commands to invoke other search strategies can be found in the
project description.

Please only change the parts of the file you are asked to.
Look for the lines that say

"*** YOUR CODE HERE ***"

The parts you fill in start about 3/4 of the way down.  Follow the
project description for details.

Good luck and happy searching!
"""

from existingSearchAgents import *
from existingSearchAgents import SearchAgent

'''#################################################

    This file contains mostly functions that you
    will write or complete. Be sure to check out
    the file 'existingSearchAgents.py' as it
    contains many classes that are used in this
    file, with explanation in comments. It might
    help you to understand what is happening!

    Be sure to also read the file 'util.py', as
    it contains a number of classes that will
    prove useful when implementing the
    solutions to the assignments.

#################################################'''


class CornersProblem(search.SearchProblem):
    """
    This search problem finds paths through all four corners of a layout.

    You must select a suitable state space and successor function
    """

    def __init__(self, startingGameState):
        """
        Stores the walls, pacman's starting position and corners.
        """
        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()
        top, right = self.walls.height - 2, self.walls.width - 2
        self.corners = ((1, 1), (1, top), (right, 1), (right, top))
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                print(('Warning: no food in corner ' + str(corner)))
        self._expanded = 0  # Number of search nodes expanded

        "*** YOUR CODE HERE ***"

    def getStartState(self):
        "Returns the start state (in your state space, not the full Pacman state space)"
        "A State contains the Pacman position, Direction, step cost, path cost and a list of unexplored corners"  # change description if we change the code
        cornerList = []
        for corner in self.corners:
            cornerList.append(corner)
        # startState = (self.startingPosition, None, 0, 0, cornerList) # I changed the start state: it should indeed probably not include None, 0 0
        startState = (self.startingPosition, cornerList)
        return startState

    def isGoalState(self, state):
        "Returns whether this search state is a goal state of the problem"
        # if not state[4]:  # this might not work?
        if not state[1]:
            return True
        else:
            return False

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """

        def isCrossroad(node):
            nrOfSuccessors = 0
            for action in [Directions.NORTH, Directions.SOUTH,
                           Directions.EAST, Directions.WEST]:
                x, y = node
                dx, dy = Actions.directionToVector(action)
                nextx, nexty = int(x + dx), int(y + dy)
                if not self.walls[nextx][nexty]:
                    nrOfSuccessors += 1
            if nrOfSuccessors > 2:
                return True
            else:
                return False

        def updateCorners(node):
            corners = list(state[1])
            # corners=map(list,state[1]) # what does 'state' precisely refer to here?
            if node in corners:
                # print("found corner: ", node)
                corners.remove(node)
            return tuple(corners)
            # return map(tuple,corners)

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH,
                       Directions.EAST, Directions.WEST]:
            # Add a successor state to the successor list if the action is legal
            # Here's a code snippet for figuring out whether a new position hits a wall:
            #   x,y = currentPosition
            #   dx, dy = Actions.directionToVector(action)
            #   nextx, nexty = int(x + dx), int(y + dy)
            #   hitsWall = self.walls[nextx][nexty]

            x, y = state[0]
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)

            foundSuccessor = False
            current = (x, y)

            while not foundSuccessor:
                # check if next node has wall
                if not self.walls[nextx][nexty]:
                    # check for crossroad
                    if not isCrossroad((nextx, nexty)):
                        current = (nextx, nexty)
                        nextx, nexty = int(nextx + dx), int(nexty + dy)
                    else:
                        newPos = (nextx, nexty)
                        unexploredCorners = updateCorners(newPos)
                        dist = abs(newPos[0] - x) + abs(newPos[1] - y)
                        successorState = ((newPos, unexploredCorners), action, dist)
                        successors.append(successorState)
                        foundSuccessor = True
                # going into this direction would cause pacman to collide with a wall
                else:
                    # check if newState is different from parameter
                    if not current == state[0]:
                        unexploredCorners = updateCorners(current)
                        newPos = current
                        dist = abs(newPos[0] - x) + abs(newPos[1] - y)
                        successorState = ((newPos, unexploredCorners), action, dist)
                        successors.append(successorState)
                        foundSuccessor = True
                    # if there is no successor in this direction
                    else:
                        foundSuccessor = True



        self._expanded += 1
        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999.  This is implemented for you.
        """
        if actions is None:
            return 999999
        x, y = self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
        return len(actions)


def cornersHeuristic(state, problem):
    """
        A heuristic for the CornersProblem that you defined.

          state:   The current search state
                   (a data structure you chose in your search problem)

          problem: The CornersProblem instance for this layout.

        This function should always return a number that is a lower bound
        on the shortest path from the state to a goal of the problem; i.e.
        it should be admissible.  (You need not worry about consistency for
        this heuristic to receive full credit.)
        """

    # Finds the shortest manhattan distance going through all corners using recursion
    corners = list(problem.corners)
    walls = problem.walls
    pos = state[0]

    def allPaths(start, cost):
        if not corners:
            return [cost]
        else:
            solutions = []
            for corner in corners:
                dist = calculateDistance(start, corner)
                corners.remove(corner)
                solutions = solutions + (allPaths(corner, cost + dist))
                corners.append(corner)
            return solutions

    return min(allPaths(pos,0))/2

def cornersHeuristic2(state, problem):


    # Our heuristic recursively finds the closest corner, and returns the total past cost when all corners are visited in this manner
    # Note that we don't actually use this heuristic at the moment. We consider it a bit too greedy.

    corners = problem.corners  # These are the corner coordinates
    # These are the walls of the maze, as a Grid (game.py)
    walls = problem.walls

    pos = state[0]

    def allDistances(pos, corners, totalCost):

        shortestDistance = 9999999999
        closestNode = None
        for corner in corners:
            distance = calculateDistance(pos, corner)
            if distance < shortestDistance:
                shortestDistance = distance
                closestNode = corner

        distance = calculateDistance(pos, closestNode)
        newCorners = list(corners)
        newCorners.remove(closestNode)
        if newCorners:
            newCorners = tuple(newCorners)
            return allDistances(closestNode, newCorners, totalCost + distance)

        else:
            return totalCost + distance

    # return allDistances(pos,corners,0) = 952 nodes, cost 107
    return allDistances(pos,corners,0)


def calculateDistance(pos1, pos2):
        dist = abs(pos2[0] - pos1[0]) + abs(pos2[1] - pos1[1])
        return dist

def foodHeuristic(state, problem):
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come up
    with an admissible heuristic; almost all admissible heuristics will be consistent
    as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the other hand,
    inadmissible or inconsistent heuristics may find optimal solutions, so be careful.

    The state is a tuple ( pacmanPosition, foodGrid ) where foodGrid is a
    Grid (see game.py) of either True or False. You can call foodGrid.asList()
    to get a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the problem.
    For example, problem.walls gives you a Grid of where the walls are.

    If you want to *store* information to be reused in other calls to the heuristic,
    there is a dictionary called problem.heuristicInfo that you can use. For example,
    if you only want to count the walls once and store that value, try:
      problem.heuristicInfo['wallCount'] = problem.walls.count()
    Subsequent calls to this heuristic can access problem.heuristicInfo['wallCount']
    """

    # our heuristic combines two values.
    # 1) the distance to the furthest piece of food (the lower the better)
    # 2) a measure of how much pallets are left that are not on the axis of the candidate node (the lower the better). So basically a measure of how many pellets are easily accessible from the candidate node.

    position, foodGrid = state
    pellets = foodGrid.asList()
    closestDistance=99999999999999
    farthestDistance=0

    if len(pellets)==0:
        return 0

    for pellet in pellets:
        manhattanD = calculateDistance(pellet, position)
        if manhattanD>farthestDistance:
            farthestPellet=pellet
            farthestDistance=manhattanD

        pelletsLeft = 0
        for (x, y) in pellets:
            if x != position[0]:
                pelletsLeft = pelletsLeft + 1
            else:
                if y != position[1]:
                    pelletsLeft = pelletsLeft + 1

    # return 0: nodes=16465, pathcost=60
    # return farthestDistance + pelletsLeft : nodes: 8370, pathcost=60

    return farthestDistance+pelletsLeft


class ClosestDotSearchAgent(SearchAgent):
    "Search for all food using a sequence of searches"

    def registerInitialState(self, state):
        self.actions = []
        currentState = state
        while (currentState.getFood().count() > 0):
            nextPathSegment = self.findPathToClosestDot(
                currentState)  # The missing piece
            self.actions += nextPathSegment
            for action in nextPathSegment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    t = (str(action), str(currentState))
                    raise Exception(
                        'findPathToClosestDot returned an illegal move: %s!\n%s' %
                        t)
                currentState = currentState.generateSuccessor(0, action)
        self.actionIndex = 0
        print(('Path found with cost %d.' % len(self.actions)))

    def findPathToClosestDot(self, gameState):
        "Returns a path (a list of actions) to the closest dot, starting from gameState"
        # Here are some useful elements of the startState
        startPosition = gameState.getPacmanPosition()
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState)

        return search.breadthFirstSearch(problem)


class AnyFoodSearchProblem(PositionSearchProblem):
    """
      A search problem for finding a path to any food.

      This search problem is just like the PositionSearchProblem, but
      has a different goal test, which you need to fill in below.  The
      state space and successor function do not need to be changed.

      The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
      inherits the methods of the PositionSearchProblem.

      You can use this search problem to help you fill in
      the findPathToClosestDot method.
    """

    def __init__(self, gameState):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test
        that will complete the problem definition.
        """
        x, y = state

        return self.food[x][y]


class CrossroadSearchAgent(SearchAgent):
    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH,
                       Directions.EAST, Directions.WEST]:
            # Add a successor state to the successor list if the action is legal
            # Here's a code snippet for figuring out whether a new position hits a wall:
            #   x,y = currentPosition
            #   dx, dy = Actions.directionToVector(action)
            #   nextx, nexty = int(x + dx), int(y + dy)
            #   hitsWall = self.walls[nextx][nexty]
            1

        # Bookkeeping for display purposes
        self._expanded += 1

        "*** YOUR CODE HERE ***"

        return successors


##################
# Mini-contest 1 #
##################


class ApproximateSearchAgent(Agent):
    "Implement your contest entry here.  Change anything but the class name."

    def registerInitialState(self, state):
        "This method is called before any moves are made."
        "*** YOUR CODE HERE ***"

    def getAction(self, state):
        """
        From game.py:
        The Agent will receive a GameState and must return an action from
        Directions.{North, South, East, West, Stop}
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


class AStarCornersAgent(SearchAgent):
    "A SearchAgent for FoodSearchProblem using A* and your cornersHeuristic"

    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(
            prob, cornersHeuristic)
        self.searchType = CornersProblem


class AStarFoodSearchAgent(SearchAgent):
    "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"

    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(
            prob, foodHeuristic)
        self.searchType = FoodSearchProblem

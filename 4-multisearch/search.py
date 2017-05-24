# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def getAction(start, goal):
    if goal[1] is (start[1] + 1):
        return Directions.NORTH
    elif goal[1] is (start[1] - 1):
        return Directions.SOUTH
    elif goal[0] is (start[0] + 1):
        return Directions.EAST
    else:
        return Directions.WEST


def tracePath(node, explored, allCorners):  # node consists of ((position, corners), direction, step, pathcost)
    path = []
    current = node
    while not current[1] is None:
        newSteps = [current[1]] * current[2]
        path = newSteps + path
        # path.insert(0, currentDirection)
        print(current[1], "   ", current[2])
        current = findPreviousNode(current, explored, allCorners)
    return path


def isEqual(t1, t2):
    if t1[0] == t2[0] and sorted(t1[1]) == sorted(t2[1]):
        return True
    else:
        return False


def findPreviousNode(node, explored,
                     allCorners):  # node consists of ((position, corners), direction, stepDistance, pathcost)
    oldPos = (node[0])[0]  # aangepast
    oldCorners = node[0][1]
    # update cornerList
    corns = allCorners
    if oldPos in allCorners:
        c = list(oldCorners)
        c.append(oldPos)
        newCorners = tuple(c)
    else:
        newCorners = oldCorners

    stepDist = node[2]

    if node[1] == 'East':
        newPos = ((oldPos[0] - stepDist), oldPos[1])

    elif node[1] == 'North':
        newPos = (oldPos[0], (oldPos[1] - stepDist))

    elif node[1] == 'West':
        newPos = ((oldPos[0] + stepDist), oldPos[1])

    else:
        newPos = (oldPos[0], (oldPos[1] + stepDist))

    result = None

    newTuple = (newPos, newCorners)
    for e in explored:
        # if e[0] == newTuple: # does not work because corner list is not sorted!
        if isEqual(e[0], newTuple):
            result = e
            return result


def contains(pos, ex):
    for e in ex:
        if isEqual(e[0], pos):
            return True
    return False


def search(frontier, problem):
    explored = []
    start = problem.getStartState()  # @ HEY DAN, this is why the TA probably suggested to make the nodes tuples of the form ( (pos,corner), dir, pathcost, cost) -> Because of the way we call the start state here
    allCorners = start[1]
    frontier.push((start, None, 0, 0))  # look at the position of 'START' here
    while not frontier.isEmpty():
        current = frontier.pop()

        if not contains(current[0], explored):
            if problem.isGoalState(current[0]):
                print(current[0][0], " is the goal: ", problem.isGoalState(current[0]))
                path = tracePath(current, explored, allCorners)
                print("goal path: ", path)
                return path
            successors = problem.getSuccessors(current[0])
            for state, dir in successors:
                # calculate distance to new node
                newPos = state[0]
                oldPos = current[0][0]
                dist = abs(newPos[0] - oldPos[0]) + abs(newPos[1] - oldPos[1])

                newNode = (state, dir, dist, current[3] + 1)
                frontier.push(newNode)
            explored.append(current)
    print("could not find a path")
    return None


def depthFirstSearch(problem):
    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))

    frontier = util.Stack()
    return search(frontier, problem)


def breadthFirstSearch(problem):
    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))

    frontier = util.Queue()
    return search(frontier, problem)


def uniformCostSearch(problem):
    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))

    frontier = util.PriorityQueueWithFunction(getPathCost)
    return search(frontier, problem)


def getPathCost(node):
    return node[3]


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."

    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

    "Bonus assignment: Adjust the getSuccessors() method in CrossroadSearchAgent class"
    "in searchAgents.py and test with:"
    "python pacman.py -l bigMaze -z .5 -p CrossroadSearchAgent -a fn=astar,heuristic=manhattanHeuristic "


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

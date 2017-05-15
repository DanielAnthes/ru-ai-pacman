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
from game import Directions


class SearchNode:
    def __init__(self, pos, parent, cost):
        self.position = pos
        self.parentNode = parent
        self.pathCost = cost

    def getCost(self):
        return self.pathCost

    def getParent(self):
        return self.parentNode

    def getPathCost(self):
        return self.pathCost

    def getPosition(self):
        return self.position


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


# expects two adjacent points in the maze and returns the direction needed to get from start to goal

def getAction(start, goal):
    if goal[1] is (start[1] + 1):
        return Directions.NORTH
    elif goal[1] is (start[1] - 1):
        return Directions.SOUTH
    elif goal[0] is (start[0] + 1):
        return Directions.EAST
    else:
        return Directions.WEST


def tracePath(node, explored):
    path = []
    current = node
    while not current[1] is None:
        path.insert(0, current[1])
        current = findPreviousNode(current, explored)

    return path


def findPreviousNode(node, explored):
    oldPos = node[0]

    if node[1] == 'East':
        newPos = ((oldPos[0] - 1), oldPos[1])

    elif node[1] == 'North':
        newPos = (oldPos[0], (oldPos[1] - 1))

    elif node[1] == 'West':
        newPos = ((oldPos[0] + 1), oldPos[1])

    else:
        newPos = (oldPos[0], (oldPos[1] + 1))

    result = None
    for e in explored:
        if e[0] == newPos:
            result = e
    return result

def contains(pos, ex):
    for e in ex:
        if pos == e[0]:
            return True
    return False


def search(frontier, problem):
    explored = []
    start = problem.getStartState()
    frontier.push((start, None, 0, 0))
    while not frontier.isEmpty():
        current = frontier.pop()
        print("path cost of node: ", current[2])

        if not contains(current[0], explored):
            if problem.isGoalState(current[0]):
                print(current[0], " is the goal: ", problem.isGoalState(current[0]))
                path = tracePath(current, explored)
                print("goal path: ", path)
                return path
            successors = problem.getSuccessors(current[0])
            for pos, dir, stepCost in successors:
                newNode = (pos, dir, stepCost, current[3]+stepCost)
                frontier.push(newNode)
                print(frontier)
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


def aStarSearch(problem, heuristic):
    "Search the node that has the lowest combined cost and heuristic first."

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))

    def calcNodeHeuristic(node):
        return getPathCost(node) + heuristic(node[0],problem)

    frontier = util.PriorityQueueWithFunction(calcNodeHeuristic)
    return search(frontier, problem)

    "Bonus assignment: Adjust the getSuccessors() method in CrossroadSearchAgent class"
    "in searchAgents.py and test with:"
    "python pacman.py -l bigMaze -z .5 -p CrossroadSearchAgent -a fn=astar,heuristic=manhattanHeuristic "


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

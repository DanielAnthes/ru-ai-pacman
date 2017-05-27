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

def isEqual(t1, t2):
    if t1[0] == t2[0] and (t1[1]) == (t2[1]):
        return True
    else:
        return False


def contains(pos, ex):
    for e in ex:
        if isEqual(e[0], pos):
            return True
    return False


def search(frontier, problem):
    explored = []
    start = problem.getStartState()
    allCorners = start[1]
    frontier.push((start, None, 0, 0, []))
    while not frontier.isEmpty():
        current = frontier.pop()

        if not contains(current[0], explored):
            if problem.isGoalState(current[0]):
                print(current[0][0], " is the goal: ", problem.isGoalState(current[0]))
                path = current[4]
                print("goal path: ", path)
                return path
            successors = problem.getSuccessors(current[0])
            for state, dir, stepCost in successors:
                oldPath = current[4]
                newSteps = [dir] * stepCost
                newPath = oldPath + newSteps
                newNode = (state, dir, stepCost, current[3] + 1, newPath)
                frontier.push(newNode)
            explored.append(current)
            #explored.insert(0,current)  # insert in beginning for easier debugging
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

    def calcNodeHeuristic(node):
        heuristicValue=getPathCost(node) + heuristic(node[0],problem)
        print(heuristicValue)
        return heuristicValue

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

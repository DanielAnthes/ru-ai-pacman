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
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """

  # get start state as (x,y) tuple 
  # NOTE: for PositionSearchProblems, the states as returned by
  # getStartState and in getSuccessors are not full GameStates, but
  # just (x,y) positions
  start = problem.getStartState()

  # fringe contains (state,action), where;
  #  state  -- is the fringe state itself
  #  parent -- the state from which we came to get to this state
  #  action -- the action taken to get to this state
  # construct fringe as stack (i.e. last-in / first-out list)
  fringe = util.Stack()   

  # construct visited as dictionary
  # visited has state as the key and contains (parent, action), where
  #  parent -- is the state from which we came from to get to this state
  #  action -- is the action taken to get to this state via the lowest cost route
  visited = {}            

  # add start to fringe. It has no parent, and no associated action and stepCost
  fringe.push( (start,None,None) )

  # Main part: iterate until goal is found (success) or fringe is
  # empty (entire search tree visited without finding goal -> failure)
  while not fringe.isEmpty() :
    # pop next element of fringe, add to visited
    state,parent,action = fringe.pop()
    # check if already expanded

    # Note: this test is needed because a state may be added to the
    # fringe multiple times (as it is reached by different paths).
    # After the first time this state is taken off the fringe and
    # expanded the later version still remain on the fringe and may
    # eventually be taken of it.  However, as this state has by now
    # already been expanded this has little benefit and should be
    # excluded.
    if state in visited : 
      continue
    else:
      visited[state] = (parent,action)
    # if goal state reached, extract path to goal and exit
    if problem.isGoalState(state) :      
      #print "Goal Found! ", state
      # backtrack up the chain of actions stored in visited to extract the path
      path = []
      parent,action = visited[state]
      while action is not None :
        print("Action" + action)
        path.insert(0, action)
        # get state we came from and action taken from visited
        parent,action = visited[parent] 
      return path
    # if not goal state, expand further
    else :
      # N.B. successor is (state, action, stepCost)
      print ("State : " + state)
      for successor in problem.getSuccessors(state) :
        print("Successors :" + successor)
        # add to fringe, but only if not yet visited
        succState, action, cost = successor
        # Note: technically this visited test is *not* necessary as the first one
        # above will prevent re-expansion.  However, it is computational more efficient to *not*
        # waste time adding nodes to the fringe which you already know should never be expanded
        if succState not in visited :
          print("OK")
          fringe.push( (succState, state, action) )

  # if function reaches this point, fringe is empty -> fail
  print("No path found")
  return []   # return empty path

    
def breadthFirstSearch(problem):
  """
  Search the shallowest nodes in the search tree first.
  This code is almost identical to that of the previous function depthFirstSearch
  The ONLY difference is the second line of code which changes the fring from a stack (dfs) into
  a queue (bfs)
  """

  start = problem.getStartState()
  # construct fringe as queue (i.e. first-in / first-out list)
  fringe = util.Queue()   # This line is the only difference with the previous function

  # construct visited as dictionary
  visited = {}            

  # add start to fringe. It has no parent, and no associated action and stepCost
  fringe.push( (start,None,None) )

  # Main part: iterate until goal is found (success) or fringe is
  # empty (entire search tree visited without finding goal -> failure)
  while not fringe.isEmpty() :
    # pop next element of fringe, add to visited
    state,parent,action = fringe.pop()
    if state in visited : # check if already expanded
      continue
    else:
      visited[state] = (parent,action)
    # if goal state reached, extract path to goal and exit
    if problem.isGoalState(state) :      
      # backtrack up the chain of actions stored in visited to extract the path
      path = []
      parent,action = visited[state]
      while action is not None :
        path.insert(0, action)
        parent,action = visited[parent] # action taken to this position
      return path
    # if not goal state, expand further
    else :
      # N.B. successor is (state, action, stepCost)
      for successor in problem.getSuccessors(state) :
        # add to fringe, but only if not yet visited
        succState, action, cost = successor
        if succState not in visited :
          fringe.push( (succState, state, action) )

  # if function reaches this point, fringe is empty -> fail
  print("No path found")
  return []   # return empty path

     
def uniformCostSearch(problem):
  """
  Search the node of least total cost first. 
  This algorithm is very much like the depthFirstSearch algorithm (see above) 
  The differences are:
  1. implementing the fringe as a priority queue instead of a stack, with the total path-sofar cost as priority
  2. adding the pathcost to the tuples that are items in the visited list
  3. checking for shorter paths to visited nodes before adding them to the fringe (efficiency improvement)
  """
  
  start = problem.getStartState()
  # construct fringe as priority queue (i.e. lowest priority first out)
  fringe = util.PriorityQueue()

  # construct visited as dictionary
  # visited has state as the key and contains (parent, action, cost), where
  #  parent -- is the state from which we came from to get to this state
  #  action -- is the action taken to get to this state via the lowest cost route
  #  cost   -- the cost of the path to this state
  visited = {}            

  # fringe contains the tuple (state, action, parent, cost), where;
  #  state  -- is the fringe state itself
  #  action -- action is the action taken to get to the successor
  #  parent -- parent 'fringe-state', i.e. (state action parent cost) tuple.  Used to extract the solution
  #  cost   -- cost to get to this state from this parent
  # add start to fringe. It has no parent, and no associated action and stepCost
  fringe.push( (start, None, None, 0), 0)

  # Main part: iterate until goal is found (success) or fringe is
  # empty (entire search tree visited without finding goal -> failure)
  while not fringe.isEmpty() :
    # pop next element of fringe, add to visited
    state,parent,action,cost = fringe.pop()
    if state in visited and visited[state][2] > cost : #don't re-expand if already visited with cheaper solution
      continue
    else:
      visited[state] = (parent,action,cost)
    # if goal state reached, extract path to goal and exit
    if problem.isGoalState(state) :      
      # backtrack up the chain of actions stored in visited to extract the path
      path = []
      parent,action,cost = visited[state]
      while action is not None :
        path.insert(0, action)
        parent,action,cost = visited[parent] # action taken to this position
      return path
    # if not goal state, expand further
    else :
      # N.B. successor is (state, action, stepCost)
      for successor in problem.getSuccessors(state) :
        #print "Successors :", successor
        # add to fringe, but only if not yet visited
        succState, action, actcost = successor
        succcost = cost + actcost
        # add to fringe, but only if not yet visited at a lower cost
        if succState not in visited or visited[succState][2] > succcost :
          fringe.push( (succState, state, action, succcost), succcost )

  # if function reaches this point, fringe is empty -> fail
  print("No path found")
  return []   # return empty path

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  """
  Search the node that has the lowest combined cost and heuristic first.
  This algorithm is very much like the uniformCostSearch algorithm (see above) 
  The *only* difference is that the priority for the fringe is pathCost+heuristicValue instead of just pathCost 
  N.B.: the visited list still only contains pathCosts, heuristicValue is only used for the fringe
  """
  start = problem.getStartState()
  # construct fringe as priority queue (i.e. lowest priority first out)
  fringe = util.PriorityQueue()

  # construct visited as dictionary
  # visited has state as the key and contains (parent, action, cost), where
  visited = {}            

  # fringe contains the tuple (state, action, parent, cost), where;
  fringe.push( (start, None, None, 0), 0)

  # Main part: iterate until goal is found (success) or fringe is
  # empty (entire search tree visited without finding goal -> failure)
  while not fringe.isEmpty() :
    # pop next element of fringe, add to visited
    state,parent,action,cost = fringe.pop()
    if state in visited and visited[state][2] > cost : #don't re-expand if already visited with cheaper solution
      continue
    else:
      visited[state] = (parent,action,cost)
    # if goal state reached, extract path to goal and exit
    if problem.isGoalState(state) :      
      # backtrack up the chain of actions stored in visited to extract the path
      path = []
      parent,action,cost = visited[state]
      while action is not None :
        path.insert(0, action)
        parent,action,cost = visited[parent] # action taken to this position
      return path
    # if not goal state, expand further
    else :
      # N.B. successor is (state, action, stepCost)
      for successor in problem.getSuccessors(state) :
        #print "Successors :", successor
        # add to fringe, but only if not yet visited
        succState, action, actcost = successor
        succcost = cost + actcost
        # add to fringe, but only if not yet visited at a lower cost
        if succState not in visited or visited[succState][2] > succcost :
          # add to the fringe, but now priority is f-value = g-value + heuristic value
          fringe.push( (succState, state, action, succcost), succcost+heuristic(succState,problem) )

  # if function reaches this point, fringe is empty -> fail
  print("No path found")
  return []   # return empty path

  "Bonus assignment: Adjust the getSuccessors() method in CrossroadSearchAgent class"
  "in searchAgents.py and test with:"
  "python pacman.py -l bigMaze -z .5 -p CrossroadSearchAgent -a fn=astar,heuristic=manhattanHeuristic "
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

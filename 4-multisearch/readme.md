## Topic 4: Multi-goal search in Pacman

### Introduction

In this project, your Pacman agent will find paths through its maze
world to collect food efficiently. Your task is to modify the search
methods from the previous week to work when Pacman wants to visit lots
of equally rewarding goals as efficiently as possible (i.e. in the
minimum number of moves).

Once again, the code for this project consists of several Python files,
some of which you are going to edit, some of which you need to read and
understand, and some of which you can ignore.
**Although many of them are the same as last
week, it's important that you don't re-use last week's files**. Instead,
make a fresh project by downloading all the code.

#### Files you'll edit and submit

* `search.py` where all of your search algorithms will reside.
* `searchAgents.py` where all of your search-based agents, and search problem definitions
will reside.

#### Files you might want to look at (found in the `scripts` folder)

* `pacman.py`, the main file that runs Pacman games. This file describes a Pacman
GameState type, which you use in this project.
* `game.py`, the logic behind how the Pacman world works. This file describes several
supporting types like AgentState, Agent, Direction, and Grid.
* `util.py`, useful data structures for implementing search algorithms.

### Table of Contents

-   [Finding all the Corners](#finding-all-the-corners)
-   [Assignment 1](#assignment-1)
-   [Assignment 2](#assignment-2)
-   [Eating All The Dots](#eating-all-the-dots)
-   [Assignment 3](#assignment-3)
-   [Suboptimal Search](#suboptimal-search)
-   [Assignment 4](#assignment-4)
-   [Bonus assignment](#bonus-assignment)
-   [Object Glossary](#object-glossary)

### Finding all the Corners

The real power of A\* will only be apparent with a more challenging
search problem than last week's. This week, it's time to formulate a new
problem and design a heuristic for it.

In *corner mazes*, there are four dots, one in each corner. Our new
search problem is to find the shortest path through the maze that
touches all four corners (whether the maze actually has food there or
not). Note that for some mazes like
[tinyCorners](layouts/tinyCorners.lay), the shortest path does not
always go to the closest food first! *Hint*: the shortest path through
`tinyCorners` takes 28 steps.

### Assignment 1

Implement the `CornersProblem` search
problem in `searchAgents.py`. You will need to choose a state
representation that encodes all the information necessary to detect
whether all four corners have been reached. Now, your search agent
should solve:

```
python run.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
python run.py -l mediumCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
```

Remember you can also use PyCharm to execute `run.py`.

To receive full credit, you need to define an abstract state
representation that *does not* encode irrelevant information (like the
position of ghosts, where extra food is, etc.). In particular, do not
use a Pacman `GameState` as a search state. Your code will be
very, very slow if you do (and also wrong).

*A Hint:* The only parts of the game state you need to reference in your
implementation are the starting Pacman position and the location of the
four corners.

*A Second Hint:* In the `__init__` function of the
`CornersProblem` class, the corners of the maze are stored as
a tuple (of tuples), because the frontier in the search algorithm uses
tuples. However, a tuple is an *immutable* data type, meaning that its
contents can only be initialized, but not adjusted afterwards. So,
whenever you wish to change something in a tuple, you should convert it
to a list before making adjustments. Do not forget to change it back
again into a tuple before passing it on!

Our implementation of `breadthFirstSearch` expands just under
2000 search nodes on [mediumCorners](layouts/mediumCorners.lay).
However, heuristics (used with A\* search) can reduce the amount of
searching required.

### Assignment 2

Implement a heuristic for the
`CornersProblem` in `cornersHeuristic`. Grading:
inadmissible heuristics will get *no* credit. 1 point for any admissible
heuristic. 1 point for expanding fewer than 1600 nodes. 1 point for
expanding fewer than 1200 nodes. Expand fewer than 800, and you're doing
great!

```
python run.py -l mediumCorners -p AStarCornersAgent -z 0.5
```

*Hint:* Remember, heuristic functions just return numbers, which, to be
admissible, must be lower bounds on the actual shortest path cost to the
nearest goal.

*Note:* `AStarCornersAgent` is a shortcut for
`-p SearchAgent -a fn=aStarSearch,prob=CornersProblem,heuristic=cornersHeuristic`.

### Eating All The Dots

Now we'll solve a hard search problem: eating all the Pacman food in as
few steps as possible. For this, we'll need a new search problem
definition which formalizes the food-clearing problem:
`FoodSearchProblem` in `searchAgents.py`
(implemented for you). A solution is defined to be a path that collects
all of the food in the Pacman world. For the present project, solutions
do not take into account any ghosts or power pellets; solutions only
depend on the placement of walls, regular food and Pacman (of course,
ghosts can ruin the execution of a solution! We'll get to that in the
next project). If you have written your general search methods
correctly, `A*` with a null heuristic (equivalent to
uniform-cost search) should quickly find an optimal solution to
[testSearch](layouts/testSearch.lay) with no code change on your part
(total cost of 7).

```
python run.py -l testSearch -p AStarFoodSearchAgent
```

*Note:* `AStarFoodSearchAgent` is a shortcut for
`-p SearchAgent -a fn=astar,prob=FoodSearchProblem,heuristic=foodHeuristic`.

You should find that UCS starts to slow down even for the seemingly
simple `tinySearch`. As a reference, our implementation takes
2.5 seconds to find a path of length 27 after expanding 4902 search
nodes.

### Assignment 3

Fill in `foodHeuristic` in
`searchAgents.py` with a consistent heuristic for the
`FoodSearchProblem`. Try your agent on the
`trickySearch` board:

```
python run.py -l trickySearch -p AStarFoodSearchAgent
```

Our UCS agent finds the optimal solution in about 13 seconds, exploring
over 16,000 nodes. If your heuristic is admissible, you will receive the
following score, depending on how many nodes your heuristic expands.

<center>
| Fewer nodes than: | Points     |
|:-----------------:|:----------:|
| 15000             | 1          |
| 12000             | 2          |
| 9000              | 3 (medium) |
| 7000              | 4 (hard)   |
</center>

If your heuristic is inadmissible, you will receive **no credit**, so be
careful! Think through admissibility carefully, as inadmissible
heuristics may manage to produce fast searches and even optimal paths.
Can you solve `mediumSearch` in a short time? If so, we're
either very impressed, or your heuristic is inadmissible.

**Admissibility vs. Consistency?** Technically, admissibility isn't enough
to guarantee correctness in graph search -- you need the stronger
condition of consistency. For a heuristic to be consistent, it must hold
that if an action has cost *c*, then taking that action can only cause a
drop in heuristic of at most *c*. If your heuristic is not only
admissible, but also consistent, you will receive 1 additional point for
this question.

Almost always, admissible heuristics are also consistent, especially if
they are derived from problem relaxations. Therefore it is probably
easiest to start out by brainstorming admissible heuristics. Once you
have an admissible heuristic that works well, you can check whether it
is indeed consistent, too. Inconsistency can sometimes be detected by
verifying that your returned solutions are non-decreasing in f-value.
Moreover, if UCS and A\* ever return paths of different lengths, your
heuristic is inconsistent. This stuff is tricky. If you need help, don't
hesitate to ask the course staff!

### Suboptimal Search

Sometimes, even with A\* and a good heuristic, finding the optimal path
through all the dots is hard (i.e. will take long). In these cases, we'd
still like to find a reasonably good path, quickly. In this section,
you'll write an agent that always eats the closest dot.
`ClosestDotSearchAgent` is implemented for you in
`searchAgents.py`, but it's missing a key function that finds
a path to the closest dot.

### Assignment 4

Implement the function
`findPathToClosestDot` in `searchAgents.py`. Our
agent solves this maze (suboptimally!) in under a second with a path
cost of 350:

```
python run.py -l bigSearch -p ClosestDotSearchAgent -z .5
```

*Hint:* The quickest way to complete `findPathToClosestDot` is
to fill in the `AnyFoodSearchProblem`, which is missing its
goal test. Then, solve that problem with an appropriate search function.
The solution should be very short!

Your `ClosestDotSearchAgent` won't always find the shortest
possible path through the maze. (If you don't understand why, ask an
assistant!) In fact, you can do better if you try.

### Bonus assignment

Implement an
`ApproximateSearchAgent` in `searchAgents.py` that
finds a short path through the `bigSearch` layout. Of course,
hard-coding the path is *not* an admissible solution. If your algorithm
finds the shortest path using no more than 30 seconds of computation,
you will get the extra credit points.

```
python run.py -l bigSearch -p ApproximateSearchAgent -z .5 -q
```

We will time your agent using the no graphics option `-q`, and
it must complete in under 30 seconds on our grading machines. Please
describe what your agent is doing in a comment! We reserve the right to
also give extra credit to creative solutions, even if they don't work
that well.

### Object Glossary

Here's a glossary of the key objects in the code base related to search
problems, for your reference:

- `SearchProblem` (`search.py`)

   A SearchProblem is an abstract object that represents the state
    space, successor function, costs, and goal state of a problem. You
    will interact with any SearchProblem only through the methods
    defined at the top of `search.py`

- `PositionSearchProblem` (`searchAgents.py`)

	A specific type of SearchProblem that you will be working with ---
    it corresponds to searching for a single pellet in a maze.

- `CornersProblem` (`searchAgents.py`)

	A specific type of SearchProblem that you will define --- it
    corresponds to searching for a path through all four corners of
    a maze. (next week)

- `FoodSearchProblem` (`searchAgents.py`)

	A specific type of SearchProblem that you will be working with ---
    it corresponds to searching for a way to eat all the pellets in
    a maze.

- Search Function

	A search function is a function which takes an instance of
    SearchProblem as a parameter, runs some algorithm, and returns a
    sequence of actions that lead to a goal. Example of search functions
    are `depthFirstSearch` and `breadthFirstSearch`,
    which you have to write. You are provided `tinyMazeSearch`
    which is a very bad search function that only works correctly on
    `tinyMaze`

- `SearchAgent`

	`SearchAgent` is a class which implements an Agent (an
    object that interacts with the world) and does its planning through
    a search function. The `SearchAgent` first uses the search
    function provided to make a plan of actions to take to reach the
    goal state, and then executes the actions one at a time.

## Topic 6: Pacman Survival Contest!

### IMPORTANT NOTE: 
PLEASE DO AT LEAST ASSIGNMENT 1 OF THE MULTI-AGENT TOPIC (Ch.5) FIRST,
AND HAND IT IN FOR FEEDBACK. YOU DO NEED THAT PRACTICE FOR THE CONTEST!

### Introduction

The course contest involves a single-player survival-horror style
Pacman contest. Pacman must survive as a long as possible with a
sequence of levels of increasing difficulty.

The code base has not changed much from the previous projects, but
please start with a fresh installation, rather than intermingling files.
You can, however, re-use code from your previous solutions in any way
you want.

#### Files you'll edit and submit

* `competitionAgents.py`, specification and helper methods for capture agents.

Note: Please call your agent class `MyPacmanAgent` and
derive it from `CompetitionAgent` so we can automatically run the code
with the following line:

```
python pacman.py -p MyPacmanAgent
```

#### Files you might want to look at

* `pacman.py`, the main file that runs games. This file also describes the new capture the flag GameState type and rules.
* `leaderboard.py, the file that runs all levels multiple times to compute the final leaderboard score for your agent.

#### Supporting files

* `game.py`, the logic behind how the Pacman world works. This file describes several supporting types like AgentState, Agent, Direction, and Grid.
* `util.py`, useful data structures for implementing search algorithms.
* `distanceCalculator.py`, computes shortest paths between all maze positions.
* `graphicsDisplay.py`, graphics for Pacman.
* `graphicsUtils.py`, support for Pacman graphics.
* `textDisplay.py`, ASCII graphics for Pacman.
* `keyboardAgents.py`, keyboard interfaces to control Pacman.
* `layout.py`, code for reading layout files and storing their contents.


### Table of Contents

-   [Rules of Pacman Survival](#rules-of-pacman-survival)
-   [Getting Started](#getting-started)
-   [Official Tournaments](#official-tournaments)
-   [Designing Agents](#designing-agents)
-   [Contest Details](#contest-details)
-   [Grading](#grading)

### Rules of Pacman Survival

**Level Scoring:** When a Pacman eats a food dot, the food is
permanently removed and ten points are scored. The general scoring rules
are:

-   -1 point for every Pacman move

-   +10 points for every food eaten

-   +200 for every ghost eaten

-   +500 for eating all the food in a level. This also ends the level

-   -500 for dying, either through running out of time or being eaten by
    a ghost

A level ends when pacman has eaten all of the food dots (i.e. the
power-capsules do not count as food!). Levels are also limited to 3000
agent moves. If this move limit is reached pacman automatically dies!

**Level Progression:** There are a
series of levels of increasing difficulty, starting from easy open
worlds with lots of food and few ghosts, to the harder final levels
where there is less food and more ghosts. In addition there are 3 ghost
types (see below) and the later levels have more intelligent ghosts
which pacman will find it harder to avoid.

**Final Score:** The tournament runs
automatically over all the levels and the final score is the
average of the scores for each of
the levels. (Note: **Do not** hand-tune your agents for particular levels,
as the final tournament will include some additional levels you have not
seen before.)

**Computation Time:** Each agent has 1 second to return each action.
Each move which does not return within one (1) second will incur a
warning. After three warnings, or any single move taking more than 3
seconds, the game is forfeit (i.e. pacman dies!). There will be an
initial start-up allowance of 15 seconds (use the
`registerInitialState` function). You need to manage your
computation time well! Be careful!

**Ghosts:** There are 3 types of
ghosts in the Pacman survival world, as you have already seen.
The early levels have mainly track-following ghosts, the later (and
harder) levels have more pacman-seeking ghosts.

*Hint:* identifying the type of ghost based on its behavior can be very
useful for building an effective pacman agent. For example, knowing the
track a track-following agent is following allows you to predict where
the ghost will be and hence move round it. Or perhaps staying a few moves away
from a random agent may be a good thing to do.

### Getting Started

By default, the system will run through all the levels in layouts in
turn computing the score for your agent in each layout. Thus to run all
levels with a simple **reactive** `BaselineAgent` that the
staff has provided you can run the following. Note that for the contest we are no longer
using `run.py` but running `pacman.py` directly from the `contest-scripts`
directory.

```
python pacman.py -p BaselineAgent
```

To test with a specific game layout (rather than running through all the
layouts in order) – in this case `level3_4`, the 'hardest' available level:

```
python pacman.py -p BaselineAgent -l level3_4
```

A wealth of options are available to you are shown by:

```
python pacman.py --help
```

To even out issues due to random bad-luck, the actual score of your
agent is computed the average of the average scores over 10 re-runs of
each level (to improve sensitivity in the final scoring the final
leaderboard is computed using 50 re-runs). You can run the same 10
re-runs with the `-n` option. That is:

```
python pacman.py -n 10 -p BaselineAgent
```

(Note: You can use the `-q` option to run the games in *non-graphic*
mode to save CPU time.)

<!--- The below does not actually work because --num=10 tells the script to use student number 10,
which does not work as there are no files present in the 'student solutions' directory,  let alone
with student number 10. Running the command without the --num argument does nothing as this would
mean using all files in the 'student solutions' directory. I've commented out this section until the
script is changed to incorporate this behaviour.

Further to run the same code as used to generate the weekly leaderboards
with your own agent (assuming this is in the `competitionAgents.py` file
in the same directory) you can use:

```
python leaderboard.py --dir=. --num=10 --replay
```

When finished this will make a file called `leaderboard.html` which
contains the complete summary of the results for your agent, in the same
format as used for the leaderboard on blackboard. It also saves a
summary of all the games played in `_games.pk`.

-->

Note: Please call your agent class `MyPacmanAgent` and
derive it from CompetitionAgent so we can automatically run the code
with the following line:

```
python pacman.py -p MyPacmanAgent
```

### Official Tournaments

The actual competitions will be run using automated scoring, with the
final tournament deciding the final contest outcome. To submit your
agent, make sure to properly fill in `competitionAgents.py`and
then submit your code via the BlackBoard assignment. Twice a
week (on Mondays and Wednesdays, for code submitted before midnight) we
will run all submitted agents and update the current score-board on the
blackboard site, so you can see how your agent is doing relative to
the rest of the students.

### Designing Agents

Like in the multi-agent project, your pacman must try to eat as much
food as possible in the minimum number of moves whilst avoiding the
ghosts as much as possible. However, the added time limit of computation
introduces new challenges.

**Baseline Agents:** To kickstart your agent design, we have provided
you with two simple Baseline agents:

-   `BaselineAgent`: This is a simple *reactive* search agent. It simply
    wanders round the world eating food dots and avoiding ghosts. It
    generally dies very fast and does not normally clear even
    `level0_0`.
-   `BaselineSearchAgent` : This is a simple *search based* agent. It
    simply tries to find the shortest path to the nearest food item to
    clear the level as fast as possible. As it completely *ignored*
    ghosts it tends to die very fast and performs pretty poorly as well.

**Interface:** The `GameState` in `pacman.py` should
look familiar. Your interface in `competitionAgents.py`is also
the same as you have used in the multi-agent project.

**Distance Calculation:** To facilitate agent development, we provide
code in `distanceCalculator.py` to supply shortest path maze
distances. This class provides an fast way to get the true distance
between any 2 arbitrary points. In addition it caches previous distance
measurements to speed up later computations.

To get started designing your own agent, we recommend subclassing the
`CompetitionAgent` class. This provides access to several
convenience methods. Some useful methods are:

```py
def getFood(self, gameState):
	"""
	Returns the food you can still eat. This is in the form
	of a matrix where m[x][y]=True if there is food you can
	eat in that square.
	"""

def getScore(self, gameState):
	"""
	Returns your current score in the game.  Note: score is made up of:
		-1 for every move (so complete the level fast!)
		+10 for every food pellet eaten
		+200 for every ghost eaten
		+500 for eating all the food
	"""

def getMazeDistance(self, pos1, pos2):
	"""
	Returns the distance between two points; These are calculated using the provided
	distancer object.

	N.B. You need to call distancer.getMazeDistances() in your registerInitialState() 
		method to get the true distances, otherwise this just returns the Manhattan distance.    
	"""
```

**Restrictions:** You are free to design any agent you want. However,
you will need to respect the provided APIs if you want to participate in
the tournaments. For example, agents which compute during the opponent's turn will be
disqualified (in fact, we do not recommend any sort of multi-threading).

### Contest Details

The contest has two parts: a qualifying round and a final tournament.

**Tournament:** (details subject to change) A final tournament will
be open to the public and run on the final day of the class. During
this event selected entries will be run on a beamer to show the
agents performing well. We will select which agents to show based on
a pre-run the evening before – but will definitely include the 5
best performing agents, and some selected for
'interesting' behaviors. The final competition will be run on
layouts similar to the ones included in your competition pack (but
may be revised to manage difficulty to evoke interesting behavior).

**Important dates (subject to change)**

| Day of week | Date    | Time       | Event                                            |
| ----------  | ------- | :--------: | ------------------------------------------------ |
| Thursday    | June 5  |            | Contest announced and posted                     |
| Monday      | June 9  | (midnight) | Deadline for Tuesday leaderboard                 |
| Tuesday     | June 10 |            | Leaderboard updated                              |
| Wednesday   | June 11 | (midnight) | Deadline for Thursday leaderboard                |
| Thursday    | June 12 |            | Leaderboard updated                              |
| Monday      | June 16 | (midnight) | Deadline for Tuesday leaderboard                 |
| Tuesday     | June 17 |            | Leaderboard updated                              |
| Wednesday   | June 18 | 09:00      | **Competition Submission Deadline**              |
| Thursday    | June 19 | 13:45      | Final contest and Awards ceremony in TvA 4.00.37 |

### Grading

As with the other assignments, the grading consists of 2 main parts;

-   **Code quality** – how readable, clear, and **clever** your code is
    (50% of the marks)

-   **Performance** – how well your agent performs at the given task.
    This will be split into 2 further parts:

	-  **Qualifying** : if you agent performs better than the 'Staff Agent'
		performance then you have qualified and automatically get 50% of the
		performance marks available, i.e. 25% of the competition total.

	-  **Ranking**: the remaining 50% of the performance marks are awarded
		in a proportional fashion based on the ranking of your agent in the
		final tournament. That is if you are ranked first then you get all
		the available marks, if you are ranked last of the qualifying agents
		you get no additional marks, and if you rank in the middle then you
		get half of the marks.

-   **Prizes:** The top three teams will receive awards in class, and
    extra credit points in their final grade, i.e. you could score
    higher than 100%!

    -   First Place: 4% final exam point increase

    -   Second Place: 3% final exam point increase

    -   Third Place: 2% final exam point increase


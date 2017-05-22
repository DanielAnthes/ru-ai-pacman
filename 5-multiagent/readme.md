## Topic 5: Multi-Agent Pacman

### Introduction

Oh No! Now there is a ghost around who for some reason is trying to kill
Pacman (or even, if that's not bad enough, several ghosts)! Pacman needs
some way of planning to achieve his goals of eating the pellets, whilst
avoiding the ghosts. As we don't know how clever the ghosts are, for now
we will assume they are very clever (act optimally to get Pacman).

In this project, you will design agents for the classic version of
Pacman, including ghosts. Along the way, you will implement minimax
search without and with alpha-beta-pruning, and try your hand at evaluation
function design.

#### Files you'll edit and submit

* `multiAgents.py` where all of your multi-agent search agents will reside.

#### Files you might want to look at (found in the `scripts` folder)

* `pacman.py`, the main file that runs Pacman games. This file also describes a Pacman
 `GameState` type, which you will use extensively in this project.
* `game.py`, the logic behind how the Pacman world works. This file describes several
supporting types like AgentState, Agent, Direction, and Grid.
* `util.py`, useful data structures for implementing search algorithms.

### Table of Contents

-   [Multi-Agent Pacman](#multi-agent-pacman)
-   [Assignment 1](#assignment-1)
-   [Assignment 2](#assignment-2)
-   [Assignment 3](#assignment-3)
-   [Better evaluation and/or more opponents](#better-evaluation-andor-more-opponents)
-   [Bonus assignment A](#bonus-assignment-a)
-   [Bonus assignment B](#bonus-assignment-b)

### Multi-Agent Pacman

First, play a game of classic Pacman:

```
python run.py
```

Remember you can also use PyCharm to execute `run.py`.

Now, run the provided `ReflexAgent` in `multiAgents.py`:

```
python run.py -p ReflexAgent
```

Note that it plays quite poorly even on simple layouts:

```
python run.py -p ReflexAgent -l testClassic
```

Inspect its code (in `multiAgents.py`) and make sure you understand what
it's doing.

### Assignment 1

Improve the `ReflexAgent` in `multiAgents.py` to play respectably. The
provided reflex agent code provides some helpful examples of methods
that query the `GameState` for information. In addition, you might find
the following methods useful (but remember that you can get a listing of
all methods for an object by typing `dir(an-object)`).

* `<gameState>.isWin()` returns `True` if the game state is a winning one (all food eaten).
* `<gameState>.isLose()` returns `True` if the game state is a losing one (pacman died).
* `<agentState>.getPosition()` returns an (x,y) tuple with the
current position of the agent (pacman or ghost).
* `<ghostState>.scaredTimer` returns the number of turns that
the ghost will remain scared (0 if it currently isn't).

A capable reflex agent will have to consider both food locations and
ghost locations to perform well. Your agent should easily and reliably
clear the `testClassic` layout:

```
python run.py -p ReflexAgent -l testClassic
```

Try out your reflex agent on the default `mediumClassic` layout with one
ghost or two (and animation off to speed up the display):

```
python run.py --frameTime 0 -p ReflexAgent -k 1
python run.py --frameTime 0 -p ReflexAgent -k 2
```

How does your agent fare? It will likely often die with 2 ghosts on the
default board, unless your evaluation function is quite good.

Note the following:

* You can never have more ghosts than the layout permits. For
[mediumClassic](layouts/mediumClassic.lay) that amount is two. So
`-k 3` will still get you only two ghosts.
* As features, try the reciprocal of important values (such as
distance to food) rather than just the values themselves.
* The evaluation function you're writing is evaluating
state-action pairs; in later parts of this project, you'll be evaluating
states.
* Default ghosts move randomly; you can also play for fun with
slightly smarter directional ghosts using `-g DirectionalGhost`. If the
randomness is preventing you from telling whether your agent is
improving, you can use `-f` to run with a fixed random seed (same random
choices every game). You can also play multiple games in a row with
`-n` (e.g `-n 10` for 10 games). Turn off graphics with `-q` to run lots of games quickly.

We will check that your agent can rapidly clear the `openClassic`
layout ten times without dying more than twice or thrashing around
infinitely (i.e. repeatedly moving back and forth between two positions,
making no progress).

```
python run.py -p ReflexAgent -l openClassic -n 10 -q
```

Don't spend too much time on this question, though, as the meat of the
project lies ahead.

### Assignment 2

Now you will write an adversarial search agent in the provided
`MinimaxAgent` class stub in `multiAgents.py`. For now, your minimax
agent only needs to work with one ghost (extra credit assignment B will
ask you to extend the algorithm to any number of ghosts). You can use
the pseudo-algorithm in *P&M* (page 432) and strip out the alpha-beta
parts.

Your code should expand the game tree to the depth given in the 'depth'
argument, and stored in `self.depth`. Score the leaves of your minimax
tree (i.e. the nodes at the depth limit) with the supplied
`self.evaluationFunction`, which defaults to `scoreEvaluationFunction`.
`MinimaxAgent` extends `MultiAgentAgent`, which gives access to
`self.depth` and `self.evaluationFunction`. Make sure your minimax code
makes reference to these two variables where appropriate as these
variables are populated in response to command line options.

*Important:* A single search ply is considered to be one Pacman move and
the ghost's response, so depth 2 search will involve Pacman and the
ghost each moving two times.

Hints and observations:

-   The evaluation function in this part is already written
    (`self.evaluationFunction`).You shouldn't change this function, but
    recognize that now we're evaluating *states* rather than actions,
    as we were for the reflex agent. Look-ahead agents evaluate future
    states whereas reflex agents evaluate actions from the
    current state.

-   The minimax values of the initial state in the `minimaxClassic`
    layout with one ghost are 9, 8, 7, 536 for depths 1, 2, 3 and
    4 respectively. Note that your minimax agent predicts a win at depth
    4, but still has a low expectation at depth 3, i.e. it does not see
    the win coming at lower depths. This is due to the weakness of the
    provided state evaluation function, which simply evaluates a state
    by its game score.

	```
	python run.py -p MinimaxAgent -l minimaxClassic -a depth=4 -k 1
	```

-   To increase the search depth achievable by your agent, remove the
    `Directions.STOP` action from Pacman's list of possible actions.
    Depth 2 should be pretty quick, but depth 3 or 4 will be slow. Don't
    worry, the next question will speed up the search somewhat.

-   Pacman is always agent 0, and the ghost(s) are agent(s) 1 - n. The
    agents move in order of increasing agent index.

-   All states in minimax should be `GameStates`, either passed in to
    `getAction` or generated via `GameState.generateSuccessor`. In this
    project, you will not be abstracting to simplified states.

-   On larger boards such as `openClassic` and `mediumClassic` (the
    default), you'll find Pacman to be good at not dying, but quite bad
    at winning. He'll often thrash around without making progress. He
    might even thrash around right next to a dot without eating it
    because he doesn't know where he'd go after eating that dot. Don't
    worry if you see this behavior, a better evaluation function (extra
    credit assignment A) will clean up all of these issues.

-   When Pacman believes that his death is unavoidable, he will try to
    end the game as soon as possible because of the constant penalty
    for living. Sometimes, this is the wrong thing to do with random
    ghosts, but minimax agents always assume the worst:

	```
    python run.py -p MinimaxAgent -l trappedClassic -a depth=3 -k 1
	```

    Make sure you understand why Pacman rushes the ghost in this case.


### Assignment 3

Make a new agent that uses alpha-beta pruning to more efficiently
explore the minimax tree, in `AlphaBetaAgent`. In principle this should
be fairly easy, following the *P&M* pseudo-code on page 432, **if only**
that pseudo-code would not be **wrong**: where it says `return β` on
line 13, that should be `return α`, and where it says `return α` on line
19, that should be `return β`. So beware!

You should see a speed-up (perhaps depth 3 alpha-beta will run as fast
as depth 2 minimax). Ideally, depth 3 on `smallClassic` should run in
just a few seconds per move or faster.

```
python run.py -p AlphaBetaAgent -a depth=3 -l smallClassic -k 1
```

The `AlphaBetaAgent` minimax values should be identical to the
`MinimaxAgent` minimax values, although the actions it selects can vary
because of different tie-breaking behavior. Again, the minimax values of
the initial state in the `minimaxClassic` layout are 9, 8, 7 and 536 for
depths 1, 2, 3 and 4 respectively.

### Better evaluation and/or more opponents

There are two bonus assignments. You can choose which one to hand in for
your extra credit points. You will not get double credit points if you
hand in both.

### Bonus assignment A

Write a better evaluation function for pacman in the provided function
`betterEvaluationFunction`. The evaluation function should evaluate
states, rather than actions like your reflex agent evaluation function
did. You may use any tools at your disposal for evaluation, including
your search code (or the example solution code) from the last project.
With depth 2 search, your evaluation function should clear the
`smallClassic` layout with one random ghost most of the times and still
run at a reasonable rate (to get full credit, Pacman should be averaging
around 1000 points when he's winning).

```
python run.py -l smallClassic -p MinimaxAgent -a evalFn=better -q -n 10 -k 1
```

Document your evaluation function! We're very curious about what great
ideas you have, so don't be shy.

Hints and observations:

-   Like for your reflex agent evaluation function, you may want to use
    the reciprocal of important values (such as distance to food) rather
    than the values themselves.

-   One way you might want to write your evaluation function is to use a
    linear combination of features. That is, compute values for features
    about the state that you think are important, and then combine those
    features by multiplying them by different values and adding the
    results together. You might decide what to multiply each feature by
    based on how important you think it is.

### Bonus assignment B

Extend your alpha-beta-minimax algorithm to work with any number of
ghosts, by filling in the `MultiAlphaBetaAgent` class stub. This means
writing an algorithm that is slightly more general than what appears in
P&M. In particular, your minimax tree will have multiple min layers (one
for each ghost) for every max layer, and you should extend the
alpha-beta pruning logic appropriately to multiple minimizer agents.

The minimax values of the initial state in the `minimaxClassic` layout
with two ghost are 9, 8, 7, -492 for depths 1, 2, 3 and 4 respectively.
Note that your minimax agent will now predict a loss at depth 4 (instead
of the win when there was one ghost). But also note that your agent will
in fact often win, despite the dire prediction of depth 4 minimax. This
is, of course, because minimax assumes that all ghost play optimally,
whilst in fact these (default) ghosts move randomly.

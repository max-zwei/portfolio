<h1 align=center><strong>Maze Homework</strong></h1>

This is a simple exercise that lets you visualize the difference between search strategies in a labyrinth search scenario. It is designed to:
1) Illustrate how breadth-first search, depth-first search and heuristic search differ in their search behaviour
2) show you how small the algorithmic changes between the three search algorithms really are.
You will implement all three algorithms just by changing how the search algorithms selects the next node to visit.

# Setup
Project requirements are specified in requirements txt. Install them with *pip install -r requirements.txt*. 

# How to run?
You start the program by starting main.py
The program expects two input parameters:
- The file that contains the maze. The file should be placed in folder mazes. You don't need to include the folder name.
- The search algorithm to run. The search algorithm can be "RS" for random search, "BFS" for breadth-first search, "DFS" for depth-first search and "HS" for heuristic search.

Example usage: *python main.py maze1.txt RS*

# Visualization
The program visualized the maze as in the following Figure:

![Task Illustration](documentation/Task_Illustration.png)

The program illustrates:
1) Start: the position the search originates from
2) Goal: the position that is searched
3) Visited: all positions that have already been searched
4) Open: all positions that could be searched next. This is called the Frontier in source code.

# Task

# Your Task
Your task is twofold:
In the first part you write a function select node (see TODOs in *maze_solver/frontier.py*). This function selects which node from the frontier to search next. You will implement three variations of this function: breadth-first search, depth-first search, and heuristic search. All of this can be achieved by just selecting an appropriate node from the frontier. No other changes are necessary. We implemented random search already as an example.

In the second part please play around with different mazed and try to understand their behaviour.

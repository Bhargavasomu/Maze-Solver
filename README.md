# Maze-Solver
A Maze Path Finder Implemented in Python including both the Terminal Version and User Interface Version
# Terminal Version
This version solves the maze in the terminal itself and prints the maze for each update like visit,add to frontier etc. It uses the basic A* algorithm to solve and the Heuristic is the Manhattan distance from the present state to the goal state. The allowed direction of movement from any state is only North, South, East and West. In other words diagnol movement is not possible.
	Finally after the path has been found the maze is printed in the teminal along with the shortest path denoted by ‘P’ from the start state ‘S’ and the goal state ‘G’. The walls are denoted by ‘W’ . If a block has been visited by the algorithm while exploring the path then it is denoted by ‘V’ . If a block has been added to the frontier but not yet visited, then it is denoted by ‘F’. The rest all blocks are denoted by ‘-’. 

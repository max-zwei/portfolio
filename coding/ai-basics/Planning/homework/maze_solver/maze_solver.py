import sys
from maze_solver.frontier import Frontier
from maze_solver.node import Node


class Maze_Solver:
    """
    Solver for a given maze.
    Allows for implementation of different planning algorithms to find a path from start to goal.
    """
    def __init__(self, filename):

        # Read file and set height and width of maze
        with open("mazes/" + filename) as f:
            contents = f.read()

        # Validate start and goal
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        # Determine height and width of maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Keep track of walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        # Initially, there is no solution path yet
        self.solution = None

        # Initialize an empty explored set
        self.num_explored = 0
        self.explored = set()

        # Initialize frontier with starting node
        self.starting_node = Node(state=self.start, parent=None, action=None)
        self.frontier = Frontier(goal=self.goal, search_algorithm = sys.argv[2])
        self.frontier.add(self.starting_node)

        self.explored.add(self.starting_node)

    def neighbors(self, state):
        """
            Returns all explorable neighbouring fields of a given field in the maze.
        """
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result

    def explore_stepwise(self):
        """
            Executes the next step in the path finding algorithm.
        """
        # If nothing left in frontier, then no path
        if self.frontier.empty():
            return

        # Choose a node from the frontier
        node = self.frontier.pop()
        self.num_explored += 1

        # If node is the goal, then we have a solution
        if node.state == self.goal:
            cells = []
            while node.parent is not None:
                cells.append(node.state)
                node = node.parent
            cells.reverse()
            self.solution = cells
            return

        # Mark node as explored
        self.explored.add(node.state)

        # Add neighbors to frontier
        for action, state in self.neighbors(node.state):
            if not self.frontier.contains_state(state) and state not in self.explored:
                child = Node(state=state, parent=node, action=action)
                self.frontier.add(child)

import random
import math


class Frontier:
    """
    Data structure that stores a frontier of nodes.
    Provides functionality to select and remove nodes according to a search algorithm.
    """
    def __init__(self, goal, search_algorithm):
        self.frontier = []
        self.goal = goal
        self.search_algorithm = search_algorithm

    def add(self, node):
        """
            Add a node to the frontier. 
            New nodes are added to the back.
        """
        self.frontier.append(node)

    def contains_state(self, state):
        """
            Checks whether a node is already in the frontier.
        """
        return any(node.state == state for node in self.frontier)

    def empty(self):
        """
            Checks whether the frontier is empty.
        """
        return len(self.frontier) == 0

    def pop(self):
        """
            Removes a node from the frontier and returns it.
            The returned node is selected by function select_node.
        """
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.select_node()
            self.frontier.remove(node)
            return node

    def select_node(self):
        """
            Selects the next node to extend
        """
        # random search
        if self.search_algorithm == "RS":
            # select a random node from the frontier
            return random.choice(self.frontier)

        # depth-first search
        if self.search_algorithm == "DFS":
            # deepth-first search -> First node in, first node out
            # select the last node
            return self.frontier[len(self.frontier) - 1]
        
        # breadth-first search
        if self.search_algorithm == "BFS":
            # broadth-first search -> Last node in, first node out
            # select the first node
            return self.frontier[0]
        
        # heuristic search
        if self.search_algorithm == "HS":
            # heuristic search -> Lowest heuristic node, first node out
            # use coordinates as the heuristic (tuple of integers)
            # sort list by heuristic
            # select the last node
            heuristic = abs(self.frontier.state - self.goal)
            


class Node:
    """
        Representation of one node in the maze.
    """

    def __init__(self, state, parent, action):
        """
            constructor.
            
            arguments:
            - state: the state of this node. A tuple of integers, representing the coordinates of the state.
            - parent: the parent node this state has been visited from.
            - action: the action that was performed on the parent to get to this node.
        """
        self.state = state
        self.parent = parent
        self.action = action

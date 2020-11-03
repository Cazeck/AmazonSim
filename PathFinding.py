
from Point import Point

"""
    Credit to Nicolas Swift for the algorithmn, found from his article on medium.com
    Made some changes in order for it to produce the result I was looking for and tailor it to the warehouse floor
    layout
    
"""


class Node:
    """
    This is the Node class we use during th aStar path finding algorithm

    Attributes:
        parent: Tuple representing the point location of the parent node (x, y)
        position: Tuple representing the point location of the the node (x, y)
        g: Integer value representing the distance between the current node and start node
        h: Integer value representing the heuristic, the estimated distance from the current node to end node
        f: Integer value representing the total cost of the node

    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def aStar(grid, start, end):
    """
    Returns a list of tuples as a path from the given start to the given end in the given grid

    before we get to the Astar  pathing, I take the layout of the Warehouse Floor and set it up to a grid of ones
    and zeros, (zeros representing occupied space, ones representing a cell already containing an object)

    This grid is generated in antoher function within Floor and then is passed to Astar as the grid value


    Tying to convert the return to a list of Point objects
    """
    # Create start and end node
    # Turns the Point objects received into tuples for the time being and switches
    # x & y position in the tuple
    rev_start = (start.y, start.x)
    rev_end = (end.y, end.x)

    start_node = Node(None, rev_start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None,  rev_end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                # Need to switch the x and y here because it is backwardsn
                # (y, x) switch to (x, y)
                # And create a Point object to add to path
                new_point = Point(current.position[1], current.position[0])
                # path.append(current.position)  # original
                path.append(new_point)
                current = current.parent

            reversed_path = path[::-1]
            return reversed_path[1:]    # Return reversed path without first element (Robot current location)

        # Generate children
        children = []
        adjacent_squares = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for new_position in adjacent_squares:

            # Get node position
            node_position = (current_node.position[0] + new_position[0],
                             current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(grid) - 1) or node_position[0] < 0 \
                    or node_position[1] > (len(grid[len(grid)-1]) - 1) or node_position[1] < 0:
                continue

            # New added to stop loop
            # Check if neighbor is already in the closed list
            if Node(current_node, node_position) in closed_list:
                continue

            # Make sure walkable terrain
            if grid[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    break

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[1] - end_node.position[1]) ** 2)\
                      + ((child.position[0] - end_node.position[0]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g >= open_node.g:
                    break

            # Add the child to the open list
            open_list.append(child)


#def main():

    #maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    #floor = [[1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [1, 1, 0, 0, 0, 1, 1, 1, 1, 1],
    #         [1, 0, 0, 0, 0, 1, 1, 1, 0, 1],
    #         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [1, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    #         [1, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    #         [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 1, 1, 1, 0, 1, 0, 0, 0]]

    #start = Point(5, 9) # (5, 9) robot
    #end = Point(8, 2)   # (8, 2) shelf

    #path = aStar(floor, start, end)

    #print(path)


#if __name__ == '__main__':
#    main()

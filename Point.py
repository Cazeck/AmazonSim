
class Point:
    """
    Point class is used to establish coordinate locations throughout the warehouse

    These points allow us to have an understanding how objects are moving around during the simulation

    Attributes:
        x: Integer representing x coordinate
        y: Integer representing y coordinate
    """

    def __init__(self, x, y):
        """
        Inits Point with x and y values

        Args:
            x: Integer of x location
            y: Integer of y location
        """
        self.x = x
        self.y = y

    # Not in use
    def equals(self, other_point):
        """
        Compares the current point object with another to see if they are in the same location

        Args:
            other_point: Point object to compare location with

                Returns:
            is_same: Boolean determining whether or not the Points are the same position
        """

        is_same = self.x == other_point.x and self.y == other_point.y
        return is_same

    def __repr__(self):
        """
        Unambiguous representation of Shelf object

        Used for debugging and logging

        Returns:
            In the format: Point(x, y)
            Ex: Point(1, 2)
        """
        return "Point('{}', '{}')".format(self.x, self.y)

    def __str__(self):
        """
        Readable representation of Shelf object

        Used for display

        Returns:
            In the format:
            Point x:1 y:2
        """
        return "Point x:{} y:{}".format(self.x, self.y)

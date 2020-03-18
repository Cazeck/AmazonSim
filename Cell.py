# Cell is an extension (subclass) of Point which also has
# possible content (a Robot or Shelf). Floor should be "in charge"
# of having all the Cell objects, and Robot, Orders, Inventory,
# maybe even Belt should update Cell objects using methods of Floor

from Point import Point
from Shelf import Shelf
from Robot import Robot
from Belt import Belt
from Packer import Packer, Package
from Picker import Picker
from Charger import Charger
from DockArea import DockArea
from Bin import Bin

class Cell(Point):
    """
    Cell class is an extension of Point that enables a coordinate location to contain objects

    Each Cell is one square location on the Floor of the warehouse.  This enables us to keep
    track of how objects are interacting with each other as orders are fulfilled. It is also
    very useful for visualizing and displaying the simulation

    Attributes:
        x: Integer representing x coordinate
        y: Integer representing y coordinate
        content: List that will contain an Object if one is at the same Point as Cell
    """

    def __init__(self, point):
        """
        Inits Cell with x and y values from a specified Point

        Cells contain nothing until something is placed inside of it

        Args:
            point: Point object with an x and y coordinate
        """
        self.x = point.x
        self.y = point.y
        self.content = []

    def cellLocation(self):
        """
        Returns the location of the Cell as a Point object

        Returns:
            New Point object that is the Cell's x and y location
        """
        return Point(self.x, self.y)

    def getContents(self):
        """
        Returns whats currently within the Cell

        Returns:
            List of objects within Cell
        """
        return self.content
        # Something was scuffed here earlier, keeping this for the time being
        #if len(self.content) == 1:
        #    return self.content

        #if len(self.content) == 2:
        #    return self.content

        # should be empty List at this point
        #return self.content

    def setContents(self, new_object):
        """
        Adds an object into the Cell

        Args:
            new_object: The object that will now be located at at this Cell
        """
        self.content.append(new_object)

    def removeContent(self, object_to_remove):
        """
        Removes an object from the Cell

        Args:
            object_to_remove: The object that will no longer be at this Cell
        """
        self.content.remove(object_to_remove)

    def __repr__(self):
        """
        Unambiguous representation of Shelf object

        Used for debugging and logging

        Returns:
            In the format: Cell(x, y, content)
            Ex: Cell(7, 3, [object])
        """
        return "Cell('{}', '{}', {})".format(self.x, self.y, self.content)

    def __str__(self):
        """
        Readable representation of Shelf object

        Used for display
        More Complicated than the rest because this was initally used for creating a
        print-out display of the warehouse floor.  Added a bunch of specific cases to
        help display the variety of objects that could be within a Cell in a clear format

        Returns:
            In the format: Cell x:1 y:1 contains Object
        """
        result = "Cell x:{} y:{}".format(self.x, self.y)

        if len(self.content) == 1:

            if isinstance(self.content[0], Shelf):
                result += " contains Shelf"
                return result

            if isinstance(self.content[0], Robot):
                result += " contains Robot"
                return result

            if isinstance(self.content[0], Belt):
                result += " contains Belt"
                return result

            if isinstance(self.content[0], Packer):
                result += " contains Packer"
                return result

            if isinstance(self.content[0], Picker):
                result += " contains Picker"
                return result

            if isinstance(self.content[0], Charger):
                result += " contains Charger"
                return result

            if isinstance(self.content[0], DockArea):
                result += " contains Dock"
                return result

        if len(self.content) == 2:

            if (isinstance(self.content[0], Robot) and isinstance(self.content[1], Shelf))\
                    or (isinstance(self.content[1], Robot) and isinstance(self.content[0], Shelf)):
                result += " contains Robot and Shelf"
                return result

            if (isinstance(self.content[0], Robot) and isinstance(self.content[1], Charger))\
                    or (isinstance(self.content[1], Robot) and isinstance(self.content[0], Charger)):
                result += " contains Robot and Charger"
                return result

            if (isinstance(self.content[0], Belt) and isinstance(self.content[1], Bin))\
                    or (isinstance(self.content[1], Belt) and isinstance(self.content[0], Bin)):
                result += " contains Belt and Bin"
                return result

            if (isinstance(self.content[0], Belt) and isinstance(self.content[1], Package))\
                    or (isinstance(self.content[1], Belt) and isinstance(self.content[0], Package)):
                result += " contains Belt and Package"
                return result

        result += " contains Nothing"
        return result

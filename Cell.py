# Cell is an extension (subclass) of Point which also has
# possible content (a Robot or Shelf). Floor should be "in charge"
# of having all the Cell objects, and Robot, Orders, Inventory,
# maybe even Belt should update Cell objects using methods of Floor

from Point import Point
from Shelf import Shelf
from Robot import Robot

class Cell(Point):

    # What is currently in this cell, could be either a Robot or Shelf
    content = None

    def __init__(self, point):
        self.x = point.x
        self.y = point.y
        content = None

    # Returns whats currently in the cell
    def getContents(self):
        return self.content

    # Adds an object to the cell
    def setContents(self, object):
        self.content = object

    def __repr__(self):
        return "Cell('{}', '{}', {})".format(self.x, self.y, self.content)

    def __str__(self):
        #result = super.__str__(self)

        result = "Cell x:{} y:{}".format(self.x, self.y)

        if isinstance(self.content, Shelf):
            result += " contains Shelf"
            return result

        if isinstance(self.content, Robot):
            result += " contains Robot"
            return result

        result += " contains Nothing"
        return result
        # Might need a clone funct for visualizer


#point1 = Point(5,3)

#point2 = Point(5,2)

#cell1 = Cell(point1)

#shelf1 = Shelf(1, 10)
#print(point1)

#print(point2.below())
#cell1.setContents(shelf1)
#print(cell1.content)
#print(cell1.x)

#print(cell1)

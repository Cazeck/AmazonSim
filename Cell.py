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

    # What is currently in this cell, could be either a Robot or Shelf
    #content = None

    def __init__(self, point):
        self.x = point.x
        self.y = point.y
        self.content = []

    # Returns location of Cell (Point Object)
    def cellLocation(self):
        return Point(self.x, self.y)

    # Returns whats currently in the cell
    def getContents(self):
        if len(self.content) == 1:
            #if isinstance(self.content[0], DockArea):   # Specifically for Dock Area being scuffed right now
                #return self.content
            #else:
            return self.content

        if len(self.content) == 2:
            return self.content

        # should be empty List at this point
        return self.content

    # Adds an object to the cell
    def setContents(self, object):
        self.content.append(object)

    def removeContent(self, object):
        self.content.remove(object)

    def __repr__(self):
        return "Cell('{}', '{}', {})".format(self.x, self.y, self.content)

    def __str__(self):
        #result = super.__str__(self)

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

            if (isinstance(self.content[0], Robot) and isinstance(self.content[1], Shelf)) or (isinstance(self.content[1], Robot) and isinstance(self.content[0], Shelf)):
                result += " contains Robot and Shelf"
                return result

            if (isinstance(self.content[0], Robot) and isinstance(self.content[1], Charger)) or (isinstance(self.content[1], Robot) and isinstance(self.content[0], Charger)):
                result += " contains Robot and Charger"
                return result

            if (isinstance(self.content[0], Belt) and isinstance(self.content[1], Bin)) or (isinstance(self.content[1], Belt) and isinstance(self.content[0], Bin)):
                result += " contains Belt and Bin"
                return result

            if (isinstance(self.content[0], Belt) and isinstance(self.content[1], Package)) or (isinstance(self.content[1], Belt) and isinstance(self.content[0], Package)):
                result += " contains Belt and Package"
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

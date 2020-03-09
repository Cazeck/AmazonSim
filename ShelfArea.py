
from Shelf import Shelf
from Point import Point
from Cell import Cell


# Shelf area has information where every shelf is at all times
# is also used to create and shelves

class ShelfArea:

    # Original init for testing
    #def __init__(self):
    #    self.allShelves = []  # from O riginal testing section
    numofsareas = 0
    numofshelves = 0

    # New values to work on for actually having a floor implemented
    def __init__(self, corner, width):
        self.areacontents = [] # list of cells
        self.randomsource = 1 # SimRandom Object for deterministic randomness
        self.corner = Point(corner.x, corner.y) # Lower left corner of shelf area
        self.width = width
        self.areanumber = ShelfArea.numofsareas + 1
        ShelfArea.numofsareas += 1


        # Trying to build the shelve area cells
        for i in range(corner.y, corner.y + 2):
            #print(i)
            #print("i")
            for j in range(corner.x, corner.x + width):
                #print(j)
                cellToAdd = Cell(Point(j, i))
                self.areacontents.append(cellToAdd)

        self.populate()

    def getCorner(self):
        return self.corner

    # Returns int of Width
    def getWidth(self):
        return self.getWidth()

    # Returns int of 2 (Height will always be 2)
    def getHeight(self):
        return 2

    # Return a point if it is within the shelf area
    def getCell(self, point):
        for i in self.areacontents:
            if i.x == point.x and i.y == point.y:
                return i

        return None # No Point found

    # Fills the ShelfArea with shelf objects in each cell
    # Called by the constructor
    def populate(self):
        #number = 0
        for i in self.areacontents:
            ShelfArea.numofshelves += 1 # So we can have unique shelfNos across multiple areas
            #print("adding shelf no" + str(self.numofshelves))
            # Every Cell gets a Shelf added to it
            i.setContents(Shelf(self.numofshelves, i))

    # Returns a boolean if point is within ShelfArea
    def hasWithin(self, point):
        if point.x < self.corner.x:
            return False

        if point.x >= self.corner.x + self.width:
            return False

        if point.y < self.corner.y :
            return False

        if point.y > self.corner.y + 1:
            return False

        return True

    # Check to see if a cell within the Shelf Area is currently occupied by an object
    # return true has something within it (Robot or Shelf)
    def occupied(self, cell):
        if self.hasWithin(cell) and cell.getContents() is not None:
            return True

        return False

    # Returns a random point within the ShelfArea
    def randomPoint(self):
        column = self.randomsource.randint(self.width)
        row = self.randomsource.randint(2)
        point = Point(self.corner.x + column, self.corner.y + row)
        assert self.hasWithin(point) # Make sure that this point is within, otherwise throw error
        return point

    # Places an object within a cell
    # If Object is None, makes the cell empty
    def setContent(self, cell, object):
        if not self.occupied(cell) and self.hasWithin(cell):
            cell.setContents(object)

    # Returns shelf with matching No
    def findShelf(self, shelfNo):
        # For each cell in
        for i in self.areacontents:
            cellcont = i.getContents()[0]
            if cellcont.getShelfNo() == shelfNo:
            #if i.getContents().getShelfNo() == shelfNo:
                #print("Found shelf at")
                #print(i.getContents())
                return i.getContents()[0]






#sArea = ShelfArea(Point(0,0), 5, SimRandom()) # Creates a 5 x 2 Grid for the shelf area

#print(sArea.areacontents)

#print(sArea.randomPoint())
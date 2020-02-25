from Point import Point
from Cell import Cell
from ShelfArea import ShelfArea
from SimRandom import SimRandom

# Creating a mock floor for testing purposes
class Floor:

    warehousewidth = 20
    warehousedepth = 20

    picker = Point(0, 190)
    packer = Point(0, 50)
    shippingdock = Point(0, 0)
    receivingdock = Point(80, 0)
    charger = Point(20, 20)



    def __init__(self, rand):   # input value of rand for deterministic testing
        self.randogen = rand    # seed for random generation
        self.allpoints = {}     #  A Map of <String, Cell> for all points on the floor each cell is one "square" on floor
        self.shelfareas = []    # will be a list of shelfareas, There can be multiple shelving sections
        self.populateShelfArea()

        for i in range(0, self.warehousewidth):
            for j in range(0, self.warehousedepth):
                point = Point(j,i)  # is the (x,y)  # Ended up switched, but it works like this for now
                # check if this point already has a cell in a shelf area
                # and if so, just use the existing cell
                cell = Cell(point)    # will be the new cell created for this point

                for s in self.shelfareas:
                    if s.hasWithin(point):
                        cell = s.getCell(point)
                        assert cell is not None

                self.allpoints.update({str(point) : cell})  # Adds to the dictionary as {Point: Cell}

    # generates a few shelf areas on the floor
    def populateShelfArea(self):
        self.shelfareas.append(ShelfArea(Point(10, 10), 5, self.randogen))
        self.shelfareas.append(ShelfArea(Point(0, 0), 5, self.randogen))
        #self.shelfareas.append(ShelfArea(Point(20, 160), 10, self.randogen))

    # returns the Cell at a desired Point
    def getCell(self, point):
        return self.allpoints.get(str(point))

    # returns the Cell at a desired Point. but with coordinate values instead of a Point
    def getCellCoord(self, x, y):
        return self.getCell(Point(x,y))

    def getWarehouseWidth(self):
        return self.warehousewidth

    def getWarehouseDepth(self):
        return self.warehousedepth

    def getPicker(self):
        return self.picker

    def getPacker(self):
        return self.packer

    def getShippingDock(self):
        return self.shippingdock

    def getReceivingDock(self):
        return self.receivingdock

    def getCharger(self):
        return self.charger

    def getBeltAra(self):
        beltarea = []
        for i in range(self.picker.x, 0):
            beltarea.add(Point(i,0))
        return beltarea

    # Steal the getPath from RobotController, its better off here
    def getPath(self):
        return None

    def getNumShelfAreas(self):
        return len(self.shelfareas)

    def getShelfArea(self, number):
        return self.shelfareas[number]

    # Returns some random point within a randomly chosen shelfarea
    # might be useful for product distribution on shelves, returning a shelf to the shelf area, etc
    def randomShelfArea(self):
        s = self.randogen.randint(len(self.shelfareas))
        return self.shelfareas[s].randomPoint()

floor = Floor(SimRandom())

print(floor.shelfareas)

#for i in floor.allpoints:
    #print(i)
    #print(floor.allpoints[i])

print(floor.getCell(Point(10,10)))

print(floor.randomShelfArea())
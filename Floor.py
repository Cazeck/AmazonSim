from Point import Point
from Cell import Cell
from ShelfArea import ShelfArea
from BeltArea import BeltArea
from SimRandom import SimRandom

# Creating a mock floor for testing purposes
class Floor:

    warehousewidth = 20
    warehousedepth = 20

    picker = Point(1, 5)
    packer = Point(1, 10)
    shippingdock = Point(1, 19)
    #receivingdock = Point(80, 0)
    charger = Point(19, 19)

    def __init__(self, env):
        self.clock = env
        self.randogen = 1    # seed for random generation
        self.allpoints = {}     #  A Map of <String, Cell> for all points on the floor each cell is one "square" on floor
        self.shelfareas = []    # will be a list of shelfareas, There can be multiple shelving sections
        self.beltAreas = []
        self.populateShelfArea()
        self.populateBeltArea()

        for i in range(0, self.warehousewidth):
            for j in range(0, self.warehousedepth):
                point = Point(j, i)  # is the (x,y)  # Ended up switched, but it works like this for now
                # check if this point already has a cell in a shelf area
                # and if so, just use the existing cell
                cell = Cell(point)    # will be the new cell created for this point

                # Create the ShelfAreas
                for s in self.shelfareas:
                    if s.hasWithin(point):
                        cell = s.getCell(point)
                        #print(f'Cell is: {cell}')
                        assert cell is not None

                # Creating BeltArea
                for b in self.beltAreas:
                    #print(f'checking point: {point}')
                    if b.isWithin(point):
                        #print(f'Point is: {point}')
                        cell = b.getCell(point)
                        #print(f'Cell is: {cell}')
                        assert cell is not None


                self.allpoints.update({str(point) : cell})  # Adds to the dictionary as {Point: Cell}

    # generates a few shelf areas on the floor
    def populateShelfArea(self):
        self.shelfareas.append(ShelfArea(Point(10, 15), 10))
        self.shelfareas.append(ShelfArea(Point(10, 10), 10))
        #self.shelfareas.append(ShelfArea(Point(20, 160), 10, self.randogen))

    # generates the belt are on the floor
    def populateBeltArea(self):
        distance = self.shippingdock.y - self.picker.y + 1
        # Make the beltArea one left of Picker, and all the way to Shipping Dock
        #print(f'BeltArea start points are {self.picker.x - 1} and {self.picker.y} distance {distance}')
        self.beltAreas.append(BeltArea(Point(self.picker.x - 1, self.picker.y), distance))

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

    def getBeltArea(self):
        beltarea = []
        for i in range(self.picker.x, 0):
            beltarea.add(Point(i,0))
        return beltarea

    def getNumShelfAreas(self):
        return len(self.shelfareas)

    def getShelfArea(self, number):
        return self.shelfareas[number]

    # Steal the getPath from RobotController, its better off here

    # Maps a path from the startPoint to the endPoint
    # Will later make sure it doesn't run into anything
    # returns a list of points (the path the robot will take)
    def getPath(self, startpoint, endpoint):
        pathX = []
        pathY = []

        # We will do move Left/Right first (X)
        # Then move Up/Down after (Y)

        # Calculate whether or not we need to Left or Right
        distanceLR = startpoint.x - endpoint.x

        if distanceLR < 0:
            #print("We need to move " + str(abs(distanceLR)) + " units Right")

            for i in range(abs(distanceLR)):
                nextX = startpoint.x + (i + 1)
                currentY = startpoint.y
                # Only moving L/R so Y stays the same
                pathX.append(Point(nextX, currentY))
                # print(pathX)

        if distanceLR > 0:
            #print("We need to move " + str(abs(distanceLR)) + " units Left")

            for i in range(abs(distanceLR)):
                nextX = startpoint.x - (i + 1)
                currentY = startpoint.y
                # Only moving L/R so Y stays the same
                pathX.append(Point(nextX, currentY))
                # print(pathX)

        # Calculate whether or not we need to Up or Down
        distanceUD = startpoint.y - endpoint.y

        if distanceUD < 0:
            #print("We need to move " + str(abs(distanceUD)) + " units Up")

            for i in range(abs(distanceUD)):
                # Use endpoint.x here because we already have pathed out final x location
                currentX = endpoint.x
                nextY = startpoint.y + (i + 1)
                # Only moving U/D so X stays the same
                pathY.append(Point(currentX, nextY))
                # print(pathY)

        if distanceUD > 0:
            #print("We need to move " + str(abs(distanceUD)) + " units Down")

            for i in range(abs(distanceUD)):
                # Use endpoint.x here because we already have pathed out final x location
                currentX = endpoint.x
                nextY = startpoint.y - (i + 1)
                # Only moving U/D so X stays the same
                pathY.append(Point(currentX, nextY))
                # print(pathY)

        # Combine the two Paths, X steps first then Y steps
        fullPath = pathX + pathY

        return fullPath

    # Takes a shelf number as input
    # Returns which shelfarea that shelf can be found in
    def locateShelf(self, shelfnumber):
        for sArea in self.shelfareas:
            for cell in sArea.areacontents:
                shelf = cell.getContents()
                if shelfnumber == shelf.shelfNumber:
                    return sArea

            print("Shelf not in this sArea, checking next")
        print("Cannot find a shelf with that number")
        # Throw an exception here

    # Returns some random point within a randomly chosen shelfarea
    # might be useful for product distribution on shelves, returning a shelf to the shelf area, etc
    def randomShelfArea(self):
        s = self.randogen.randint(len(self.shelfareas))
        return self.shelfareas[s].randomPoint()

#env = "meme"
#floor = Floor(env)
#print(floor.beltAreas[0].areacontents)
#for i in floor.allpoints:
    #print(i)

from Point import Point
from Cell import Cell
from ShelfArea import ShelfArea
from BeltArea import BeltArea
from Robot import Robot
from Shelf import Shelf
from Belt import Belt
from Picker import Picker
from Packer import Packer, Package
from Charger import Charger
from DockArea import DockArea
from Bin import Bin

# Creating a mock floor for testing purposes
class Floor:

    warehousewidth = 20
    warehousedepth = 20

    pickerlocation = Point(1, 5)
    packerlocation = Point(1, 10)
    shippingdock = DockArea([Point(0, 18), Point(1, 18),Point(0, 19), Point(1, 19)])
    shippingdockcorner = Point(0, 18)
    chargers = [Charger(Point(5, 0)), Charger(Point(6, 0)), Charger(Point(7, 0)), Charger(Point(8, 0)), Charger(Point(9, 0))]
    robots = [Robot('A', Point(5, 0)), Robot('B', Point(6, 0)), Robot('C', Point(7, 0)), Robot('D', Point(8, 0)), Robot('E', Point(9, 0))]



    def __init__(self, env):
        self.clock = env
        self.randogen = 1    # seed for random generation
        self.allpoints = {}     #  A Map of <String, Cell> for all points on the floor each cell is one "square" on floor
        self.shelfareas = []    # will be a list of shelfareas, There can be multiple shelving sections
        self.beltAreas = []
        self.picker = Picker(self.pickerlocation)
        self.packer = Packer(self.packerlocation)
        self.populateShelfArea()
        self.populateBeltArea()

        # Create a Cell for each location in Floor
        for y in range(0, self.warehousedepth):
            for x in range(0, self.warehousewidth):
                point = Point(x, y)  # is the (x,y)  # Ended up switched, but it works like this for now
                # check if this point already has a cell in a shelf area
                # and if so, just use the existing cell
                cell = Cell(point)    # will be the new cell created for this point

                # Create the ShelfAreas
                for s in self.shelfareas:
                    if s.hasWithin(point):
                        cell = s.getCell(point)
                        #print(f'Cell is: {cell}')
                        assert cell is not None

                # Create the Cell for Picker
                if self.pickerlocation.x == point.x and self.pickerlocation.y == point.y:
                    cell.setContents(self.picker)
                    #print(f'Picker cell is {cell}')

                # Create the Cell for Packer
                if self.packerlocation.x == point.x and self.packerlocation.y == point.y:
                    cell.setContents(self.packer)

                    #print(f'Packer cell is {cell}')

                # Create the Chargers
                for charger in self.chargers:
                    if charger.location.x == point.x and charger.location.y == point.y:
                        #print("Charger")
                        cell.setContents(charger)
                        #print(cell)

                #for robot in self.robots:
                #    if robot.location.x == point.x and robot.location.y == point.y:
                #        #print("Charger")
                #        cell.setContents(robot)
                #        robot.setCell(cell)
                #        #print(cell)
                #        #print(cell.getContents())

                # Create the Dock Area
                for p in self.shippingdock.points:
                    if p.x == point.x and p.y == point.y:
                        #print("Dock Section")
                        cell.setContents(self.shippingdock)
                        #print(cell)

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
        self.shelfareas.append(ShelfArea(Point(10, 10), 10))
        self.shelfareas.append(ShelfArea(Point(10, 15), 10))
        #self.shelfareas.append(ShelfArea(Point(20, 160), 10, self.randogen))

    # generates the belt are on the floor
    def populateBeltArea(self):
        distance = self.shippingdockcorner.y - self.pickerlocation.y
        # Make the beltArea one left of Picker, and all the way to Shipping Dock
        #print(f'BeltArea start points are {self.picker.x - 1} and {self.picker.y} distance {distance}')
        self.beltAreas.append(BeltArea(self, Point(self.pickerlocation.x - 1, self.pickerlocation.y), distance))

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

    def getPickerLocation(self):
        return self.pickerlocation

    def getPacker(self):
        return self.packer

    def getPackerLocation(self):
        return self.packerlocation

    def getShippingDock(self):
        return self.shippingdockcorner

    def getReceivingDock(self):
        return self.receivingdockcorner

    # HARD CODED FOR THE TIME BEING
    def getChargerLocation(self):
        return Point(5, 0)

    def getBeltArea(self):
        beltarea = []
        for i in range(self.pickerlocation.x, 0):
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
                cellcont = cell.getContents()
                shelf = cellcont[0]
                if shelfnumber == shelf.shelfNumber:
                    return sArea

            #print("Shelf not in this sArea, checking next")
        print("Cannot find a shelf with that number")
        # Throw an exception here

    # Returns some random point within a randomly chosen shelfarea
    # might be useful for product distribution on shelves, returning a shelf to the shelf area, etc
    def randomShelfArea(self):
        s = self.randogen.randint(len(self.shelfareas))
        return self.shelfareas[s].randomPoint()

    # Going to attempt to display areacontents in full
    def printMap(self):
        linePrint = {}
        rowContents = []
        # In reverse to go bottom --> top
        #for i in range(0, self.warehousewidth):
        for i in range(self.warehousewidth - 1, -1, -1):
            yCoord = i
            for j in range(0, self.warehousedepth):
                xCoord = j
                #meme.append(f'Point {xCoord}, {yCoord}')
                cellAtCoord = self.allpoints[f'Point x:{xCoord} y:{yCoord}']
                objList = cellAtCoord.getContents()

                #print(f'At x{xCoord}, y{yCoord} is obj:{objList}')

                # If Contents is empty, move to the next Cell
                if len(objList) == 0:
                    rowContents.append('[      ]')
                    continue


                if len(objList) == 1:
                    objAtCoord = objList[0]

                    if isinstance(objAtCoord, Shelf):
                        rowContents.append(f"Shelf {objAtCoord.shelfNumber}")

                    if isinstance(objAtCoord, Robot):
                        rowContents.append(f"Robot {objAtCoord.robotName}")

                    if isinstance(objAtCoord, Belt):
                        rowContents.append(f"Belt {objAtCoord.id}")

                    if isinstance(objAtCoord, Picker):
                        rowContents.append(f"Picker")

                    if isinstance(objAtCoord, Packer):
                        rowContents.append(f"Packer")

                    if isinstance(objAtCoord, Charger):
                        rowContents.append(f"Charger")

                    if isinstance(objAtCoord, DockArea):
                        rowContents.append(f'Dock')

                # If contents are:
                if len(objList) == 2:

                    # [Charger, Robot]
                    if isinstance(objList[0], Charger) and isinstance(objList[1], Robot):
                        rowContents.append(f'Char/Rob{objList[1].robotName}')

                    # [Robot, Charger]
                    if isinstance(objList[0], Robot) and isinstance(objList[1], Charger):
                        rowContents.append(f'Char/Rob{objList[0].robotName}')

                    # [Shelf, Robot]
                    if isinstance(objList[0], Shelf) and isinstance(objList[1], Robot):
                        rowContents.append(f'Sh{objList[0].shelfNumber}/Rob{objList[1].robotName}')

                    # [Robot, Shelf]
                    if isinstance(objList[0], Robot) and isinstance(objList[1], Shelf):
                        rowContents.append(f'Sh{objList[1].shelfNumber}/Rob{objList[0].robotName}')

                    # [Belt, Bin]
                    if isinstance(objList[0], Belt) and isinstance(objList[1], Bin):
                        rowContents.append(f'Bel{objList[0].id}/Bin{objList[1].binId}')

                    # [Bin, Belt]
                    if isinstance(objList[0], Bin) and isinstance(objList[1], Belt):
                        rowContents.append(f'Bel{objList[1].id}/Bin{objList[0].binId}')

                    # [Belt, Package]
                    if isinstance(objList[0], Belt) and isinstance(objList[1], Package):
                        rowContents.append(f'Bel{objList[0].id}/Package')

                    # [Package, Belt]
                    if isinstance(objList[0], Package) and isinstance(objList[1], Belt):
                        rowContents.append(f'Bel{objList[1].id}/Package')

            linePrint[f'Row {i}'] = rowContents
            # Reset for next row
            rowContents = []

        for row in linePrint:
            #print('\n', row, linePrint[row])
            print(row, linePrint[row])


"""
env = "meme"
floor = Floor(env)
floor.printMap()
picker = floor.getCell(Point(1, 5)).getContents()[0]
packer = floor.getCell(Point(1, 10)).getContents()[0]
#print('\n')
bin1 = Bin()
item1 = 'MEME'
item2 = 'ooi'
bin1.addToBin(item1)
bin1.addToBin(item2)

belt1 = floor.getCell(Point(0, 5)).getContents()[0]
print(belt1)

picker.putOnBelt(bin1, belt1)

floor.printMap()
print('\n\n')
beltArea = floor.beltAreas[0]
beltArea.moveBelt()
#beltArea.moveBelt()
#print(belt1.getBeltLocation())
floor.printMap()

print('\n\n')
beltArea.moveBelt()
beltArea.moveBelt()
beltArea.moveBelt()
beltArea.moveBelt()
floor.printMap()

packer.takeOffBelt(bin1, belt1)

print('\n\n')
floor.printMap()

package = packer.createPackage(bin1, '99 Grove Street')
packer.putOnBelt(package, belt1)

print('\n\n')
floor.printMap()


beltArea.moveBelt()
beltArea.moveBelt()
beltArea.moveBelt()
beltArea.moveBelt()
beltArea.moveBelt()
beltArea.moveBelt()
beltArea.moveBelt()

print('\n\n')
floor.printMap()
"""

#package = packer.createPackage(bin1, '104 memest5re')

#packer.putOnBelt(package)

#robot1 = floor.robots[0]
#print(robot1)
#robot1.setDestination([Point(5, 1), Point(5, 2), Point(5, 3)])


#robot1.moveByOne()
#print(robot1)
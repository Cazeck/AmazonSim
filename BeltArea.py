"""
BeltArea has information about every Belt section at all times
and is also used to create the belt
"""
from Belt import Belt
from Point import Point
from Cell import Cell


class BeltArea:

    belt_sections = 0

    # For now it will just be a straight line
    # Picker --> Packer --> Shipping Dock
    def __init__(self, floor, startpoint, length):
        self.areacontents = []      # List of Cells
        self.belts = []             # List of belts
        self.floor = floor
        self.startpoint = startpoint
        self.length = length
        self.endpoint = Point(startpoint.x, startpoint.y - length)

        # Building BeltArea Cells
        # Going South / North
        for i in range(startpoint.y, startpoint.y - length, -1):

            cellToAdd = Cell(Point(startpoint.x, i))
            self.areacontents.append(cellToAdd)

        self.populate()

    # Fills the BeltArea with Belt objects in each Cell
    # Called by constructor
    def populate(self):
        for i in self.areacontents:
            BeltArea.belt_sections += 1                     # Each belt section has a unique number

            # print(f'Adding  to Cell {i}')
            i.setContents(Belt(self.belt_sections, i))      # Every Cell receives a Belt
            # print(f'Adding {i.getContents()[0]} to Cell {i}')
            # print(i.getContents())
            self.belts.append(i.getContents()[0])              # Add that Belt to the List of Belts

    def getCell(self, point):
        for i in self.areacontents:
            if i.x == point.x and i.y == point.y:
                return i

    # Returns the belt located at the Point Location
    def getBeltAt(self, point):
        if self.isWithin(point):
            for b in self.belts:
                bcoord = b.getBeltCoord()
                if bcoord.x == point.x and bcoord.y == point.y:
                    #print(f'Belt {b} is located at {point}')
                    return b
        else:
            print(f"No Belt located at point {point}")

    # Sorting list so that the first belt location always appear first
    # Sorts by Cell's y Location
    def sortBelt(self):
        self.belts.sort(key=lambda belt: -belt.location.y)


    # Moves every Belt in the Belt Area forward one Cell
    # The last belt is moved to the first position for now
    def moveBelt(self):
        firstBeltLocation = self.startpoint
        lastBeltLocationY = self.startpoint.y - self.length + 1

        # Let BeltArea Know what Floor is so we can call it and change Cells

        #firstCell = self.areacontents[0]
        #newCell = None
        firstCell = self.floor.getCell((self.startpoint))
        firstPoint = firstCell.cellLocation()
        #count = 0

        for belt in self.belts:
            #print(count)

            beltcell = belt.getBeltLocation()
            #print(f'Beltcell is: {beltcell}')

            nextbeltcell = self.floor.getCell(Point(beltcell.x, beltcell.y - 1))
            #print(f'Next Belt is:" {nextbeltcell}')

            # If belt has an object on it
            if belt.content is not None:

                beltcontent = belt.getContent()
                #   print(f'Belt{belt.id} is carrying {beltcontent}')

                # If first Belt
                #if belt.location.y == firstBeltLocation.y:

                # If last belt
                if belt.location.y == lastBeltLocationY:
                    # Need to move this Belt to First
                    firstCell.setContents(belt)
                    belt.setLocation(firstCell)
                    #belt.setLocation(firstCell.cellLocation())
                    # there should not be an item here, but for testing sake
                    firstCell.setContents(beltcontent)

                    # Removing Belt from current Cell
                    beltcell.removeContent(belt)
                    beltcell.removeContent(beltcontent)

                    """
                    # need to move it to the front
                    #print(f'moving {belt} to {firstCell}')
                    belt.location = firstCell
                    count += 1
                    """

                # Any belt that isn't the end
                else:
                    # Adding Belt to next Cell
                    nextbeltcell.setContents(belt)
                    belt.setLocation(nextbeltcell)
                    #belt.setLocation(nextbeltcell.cellLocation())

                    # Adding Item on Belt to next Cell
                    nextbeltcell.setContents(beltcontent)

                    # Removing Belt from current Cell
                    beltcell.removeContent(belt)
                    beltcell.removeContent(beltcontent)

                    """
                    # Move forward one Point
                    newCell = self.belts[count+1].location
                    #print(f'moving {belt} to {newCell}')
                    belt.location = newCell
                    count += 1
                    """

            # If Belt is moving on its own
            else:
                # If last belt
                if belt.location.y == lastBeltLocationY:
                    # Need to move this Belt to First
                    firstCell.setContents(belt)
                    belt.setLocation(firstCell)

                    # Removing Belt from current Cell
                    beltcell.removeContent(belt)


                else:
                    # Adding Belt to next Cell
                    nextbeltcell.setContents(belt)
                    belt.setLocation(nextbeltcell)

                    # Removing Belt from current Cell
                    beltcell.removeContent(belt)

        self.sortBelt()

    # Returns a boolean if Point is within BeltArea
    def isWithin(self, point):
        # if not in same x row as belt
        if point.x is not self.startpoint.x:
            return False

        if point.y <= self.endpoint.y:
            return False

        if point.y > self.startpoint.y:
            return False

        else:
            return True


#beltA = BeltArea(Point(0, 5), 5)
#print(beltA.areacontents)

#print('\n', beltA.belts)

#print(beltA.getCell(Point(0,9)))

"""
beltA = BeltArea(Point(0,0), 5)     # 5 Sections from 0,0 to 0,4
for i in beltA.belts:
    print(i)

#print("Belt One")
beltA.belts[0].addObject('Meme')
#print(beltA.belts[0])

print('\nGoing to move the belt')
beltA.moveBelt()
for i in beltA.belts:
    print(i)

print('\nGoing to move the belt')
beltA.moveBelt()
for i in beltA.belts:
    print(i)

print('\nGoing to move the belt')
beltA.moveBelt()
for i in beltA.belts:
    print(i)

print('\nGoing to move the belt')
beltA.moveBelt()
for i in beltA.belts:
    print(i)

print('\nGoing to move the belt')
beltA.moveBelt()
for i in beltA.belts:
    print(i)
"""
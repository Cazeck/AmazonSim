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
    def __init__(self, startpoint, length):
        self.areacontents = []      # List of Cells
        self.belts = []             # List of belts
        self.startpoint = startpoint
        self.length = length
        self.endpoint = Point(startpoint.x, startpoint.y + length)

        # Building BeltArea Cells
        # Going North / South
        for i in range(startpoint.y, startpoint.y + length):
            cellToAdd = Cell(Point(startpoint.x, i))
            self.areacontents.append(cellToAdd)

        self.populate()

    # Fills the BeltArea with Belt objects in each Cell
    # Called by constructor
    def populate(self):
        for i in self.areacontents:
            BeltArea.belt_sections += 1                     # Each belt section has a unique number
            i.setContents(Belt(self.belt_sections, i))      # Every Cell receives a Belt
            self.belts.append(i.getContents())              # Add that Belt to the List of Belts

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
        self.belts.sort(key=lambda belt: belt.location.y)


    # Moves every Belt in the Belt Area forward one Cell
    # The last belt is moved to the first position for now
    def moveBelt(self):
        firstBeltLocation = self.startpoint
        lastBeltLocationY = self.startpoint.y + self.length - 1

        #firstCell = self.areacontents[0]
        #newCell = None

        count = 0

        for belt in self.belts:
            #print(count)
            # If first Belt
            if belt.location.y == firstBeltLocation.y:
                # Need to save the Cell located at
                firstCell = belt.location
                newCell = self.belts[count + 1].location
                #newCell = self.areacontents[1]
                #print(f'moving {belt} to {newCell}')
                belt.location = newCell
                count += 1

            # If last belt
            elif belt.location.y == lastBeltLocationY:
                # need to move it to the front
                #print(f'moving {belt} to {firstCell}')
                belt.location = firstCell
                count += 1

            else:
                # Move forward one Point
                newCell = self.belts[count+1].location
                #print(f'moving {belt} to {newCell}')
                belt.location = newCell
                count += 1

        self.sortBelt()

    # Returns a boolean if Point is within BeltArea
    def isWithin(self, point):
        # if not in same x row as belt
        if point.x is not self.startpoint.x:
            return False

        if point.y > self.endpoint.y:
            return False

        if point.y < self.startpoint.y:
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

from Point import Point
from Cell import Cell
from Belt import Belt


class BeltArea:
    """
    BeltArea class tracks information about all Belt objects at all times and
    is also responsible for creating and moving the Belt objects

    For now, the BeltArea is simply a straight line to keep things simple. The
    Belt starts next to the Picker and ends at the Shipping Dock. The Belt will
    move from Picker --> Packer --> Shipping Dock

    Class Variables:
        belt_sections: A integer used to count the total number of belt sections

    Attributes:
        area_contents: List of Cells that contain Belt objects
        belts: List of Belt objects within the BeltArea
        floor: Reference to the Floor component of the warehouse
        length: How many Belt sections the Belt area consists of
        start_point: Point location of the first position of the BeltArea
        end_point: Point location of the last position of the BeltArea
    """
    belt_sections = 0

    def __init__(self, floor, start_point, length):
        """
        Inits BeltArea with a starting point and the size of the belt

        Using the start_point and length, we calculate the end_point of the Belt

        With this information, we also create the Cells of the BeltArea during initialization

        Args:
            floor: Floor object, reference to the Floor component
            start_point: A Point object marking where to start the creation of the Belt
            length: Integer representing the number of Belt objects needed
        """
        self.area_contents = []
        self.belts = []
        self.floor = floor
        self.start_point = start_point
        self.length = length
        self.end_point = Point(start_point.x, start_point.y - length)

        # Building BeltArea Cells (South --> North)
        for i in range(start_point.y, start_point.y - length, -1):
            cellToAdd = Cell(Point(start_point.x, i))
            self.area_contents.append(cellToAdd)

        self.populate()

    def populate(self):
        """
        Places a unique Belt object within each Cell of the BeltArea

        Called by the constructor
        """
        for i in self.area_contents:
            BeltArea.belt_sections += 1
            # Every Cell receives a Belt
            i.setContents(Belt(self.belt_sections, i))
            self.belts.append(i.getContents()[0])

    def getCell(self, point):
        """
        Returns the Cell object at a specified point

        Args:
            point: Point object of Cell location

        Returns:
            Cell located at point location
        """
        for cell in self.area_contents:
            if cell.x == point.x and cell.y == point.y:
                return cell

    def getBeltAt(self, point):
        """
        Returns the Belt object at a specified point

        Args:
            point: Point object of belt location

        Returns:
            Belt located at point location

        Raises:
            Exception: No Belt in BeltArea matching point
        """
        if self.isWithin(point):
            for belt in self.belts:
                b_coord = belt.getBeltCoord()
                if b_coord.x == point.x and b_coord.y == point.y:
                    return belt
        else:
            raise Exception(f"No Belt in BeltArea matching point {point}")

    def sortBelt(self):
        """
        Sorts BeltArea's belt list so that the Belt section at starting location always appears first

        The sort is done by the comparing each Cell's y coordinate within the BeltArea
        """
        self.belts.sort(key=lambda belt: -belt.location.y)


    def moveBelt(self):
        """
        Rotates the Belt, moves each Belt section forward one Cell. The last Belt section
        is moved to the front of the Belt
        """
        first_belt_location = self.start_point
        last_belt_location_y = self.start_point.y - self.length + 1
        first_cell = self.floor.getCell(self.start_point)
        first_point = first_cell.cellLocation()

        for belt in self.belts:

            belt_cell = belt.getBeltLocation()
            next_belt_cell = self.floor.getCell(Point(belt_cell.x, belt_cell.y - 1))

            # If belt has an object on it
            if belt.content is not None:
                belt_content = belt.getContent()

                # If last belt section
                if belt.location.y == last_belt_location_y:
                    # Need to move this Belt to first location
                    first_cell.setContents(belt)
                    belt.setLocation(first_cell)

                    # there should not be an item here, but for testing sake
                    first_cell.setContents(belt_content)

                    # Removing Belt from current Cell
                    belt_cell.removeContent(belt)
                    belt_cell.removeContent(belt_content)

                # Any belt section that isn't the last section
                else:
                    # Adding Belt to next Cell
                    next_belt_cell.setContents(belt)
                    belt.setLocation(next_belt_cell)

                    # Adding Item on Belt to next Cell
                    next_belt_cell.setContents(belt_content)

                    # Removing Belt from current Cell
                    belt_cell.removeContent(belt)
                    belt_cell.removeContent(belt_content)

            # If Belt is moving on its own without an object
            else:

                # If last belt
                if belt.location.y == last_belt_location_y:
                    # Need to move this Belt to first location
                    first_cell.setContents(belt)
                    belt.setLocation(first_cell)

                    # Removing Belt from current Cell
                    belt_cell.removeContent(belt)

                else:
                    # Adding Belt to next Cell
                    next_belt_cell.setContents(belt)
                    belt.setLocation(next_belt_cell)

                    # Removing Belt from current Cell
                    belt_cell.removeContent(belt)

        # Sort all of the Belt sections after Belt is finished moving for next time
        self.sortBelt()

    def isWithin(self, point):
        """
        Check to see if a Point is located within BeltArea

        Args:
            point: Point object that is the location we are looking for

        Returns:
            Boolean: Either True or False that the Point is located within BeltArea
        """
        # If not in same x row as Belt
        if point.x is not self.start_point.x:
            return False

        if point.y <= self.end_point.y:
            return False

        if point.y > self.start_point.y:
            return False

        else:
            return True

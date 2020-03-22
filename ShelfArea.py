
from Shelf import Shelf
from Point import Point
from Cell import Cell


class ShelfArea:
    """
    BeltArea class tracks information about all Shelf objects within it's area
    at all times and is responsible for creating Shelf Object

    When created, will make two rows of Shelf objects starting at the specified corner Point

    Class Variables:
        num_of_sareas: Integer used to count the total number of ShelfAreas
        num_of_shelves: Integer used to count the total number of Shelves

    Attributes:
        area_contents: List of Cells within ShelfArea that contain Shelf objects
        random_source: Seed for deterministic randomness
        corner: Point object representing the top-left corner of the ShelfArea
        width: The number of Shelves that will be place in a row
        area_number: Integer to give each ShelfArea a unique id
    """
    num_of_sareas = 0
    num_of_shelves = 0

    def __init__(self, corner, width):
        """
        Inits ShelfArea with a starting point and the width of the rows of Shelves

        With this information, we also create the Cells of the ShelfArea during initialization
        as well as populate each Cell with a unique Shelf object

        Args:
            corner: Point object which is the starting location for the ShelfArea
            width: Integer representing the width of a row of Shelves
        """
        self.area_contents = []
        self.random_source = 1
        self.corner = Point(corner.x, corner.y)
        self.width = width
        self.area_number = ShelfArea.num_of_sareas + 1
        ShelfArea.num_of_sareas += 1

        # Building the ShelfArea Cells
        for i in range(corner.y, corner.y + 2):
            for j in range(corner.x, corner.x + width):
                cellToAdd = Cell(Point(j, i))
                self.area_contents.append(cellToAdd)

        self.populate()

    def getCorner(self):
        """
        Returns the corner location of the ShelfArea

        Returns:
            A Point object of the corner location
        """
        return self.corner

    def getWidth(self):
        """
        Returns the width of the ShelfArea

        Returns:
            A integer of the width
        """
        return self.getWidth()

    def getHeight(self):
        """
        Returns the height of the ShelfArea

        For now the height is always 2

        Returns:
            A integer of the height
        """
        return 2

    def getCell(self, point):
        """
        Returns the Cell at the requested Point

        Returns:
            The Cell object, that is at the specified location
        """
        for cell in self.area_contents:
            if cell.x == point.x and cell.y == point.y:
                return cell

        raise Exception(f"No Cell in ShelfArea matching point {point}")

    def populate(self):
        """
        Places a unique Shelf object within each Cell of the ShelfArea

        Called by the constructor
        """
        for i in self.area_contents:
            # For unique shelf numbers across multiple areas
            ShelfArea.num_of_shelves += 1
            # Every Cell gets a Shelf added to it
            i.setContents(Shelf(self.num_of_shelves, i))

    def hasWithin(self, point):
        """
        Check to see if a Point is located within ShelfArea

        Args:
            point: Point object that is the location we are looking for

        Returns:
            Boolean: Either True or False that the Point is located within ShelfArea
        """
        if point.x < self.corner.x:
            return False

        if point.x >= self.corner.x + self.width:
            return False

        if point.y < self.corner.y :
            return False

        if point.y > self.corner.y + 1:
            return False

        return True

    def occupied(self, cell):
        """
        Check to see if a Cell in the Shelf Area contains an object (Robot or Shelf)

        Args:
            cell: Cell object that we are checking for contents

        Returns:
            Boolean: Either True or False that the Cell contains an object
        """
        if self.hasWithin(cell) and cell.getContents() is not None:
            return True

        return False

    def randomPoint(self):
        """
        Returns a random Point within the ShelfArea

        Returns:
            The Point object, home_location of the shelf object
        """
        column = self.random_source.randint(self.width)
        row = self.random_source.randint(2)
        point = Point(self.corner.x + column, self.corner.y + row)
        if self.hasWithin(point):
            return point
        else:
            raise Exception(f"{point} is not within ShelfArea")

    # Not in Use
    def setContent(self, cell, new_object):
        """
        Places an object within a Cell

        If new_object is none, make the Cell empty

        Args:
            cell: Cell object that is receiving an object
            new_object: object to be added to the cell
        """
        if not self.occupied(cell) and self.hasWithin(cell):
            cell.setContents(new_object)

    def findShelf(self, shelf_no):
        """
        Returns a Shelf with a matching shelf number

        Args:
            shelf_no: Integer representing a shelf number

        Returns:
            Shelf object with a matching shelf number
        """
        for i in self.area_contents:
            cell_cont = i.getContents()[0]
            if cell_cont.getShelfNo() == shelf_no:
                return i.getContents()[0]

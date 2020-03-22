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


class Floor:
    """
    Floor class is the collection of Cells that make the warehouse environment

    Each Cell represents one tile on Floor, and each Cell can contain multiple objects

    Class Variables:
        warehouse_width: Integer representing the width of the warehouse
        warehouse_depth: Integer representing the depth of the warehouse
        picker_location: Point object that will be the location that Picker object will be placed at
        packer_location: Point object that will be the location that Packer object will be placed at
        shipping_dock: DockArea object that will be in the upper-left corner of the warehouse
        shipping_dock_corner: Point object that is within shipping_dock that is next to the Belt
        chargers: List of Charger objects within the warehouse
        robots: List of Robot objects within the warehouse

    Attributes:
        clock: Reference to SimPy simulation environment for deterministic randomness
        random_seed: Seed for random generation
        all_points: A dictionary of {string: Cell} for all points on the floor
        shelf_areas: A list of ShelfArea objects
        belt_areas: A list of BeltArea objects
        picker: The Picker object within the warehouse
        packer: The Packer object within the warehouse

    """
    """         20 x 20
    warehousewidth = 20
    warehousedepth = 20

    pickerlocation = Point(1, 5)
    packerlocation = Point(1, 10)
    shippingdock = DockArea([Point(0, 18), Point(1, 18),Point(0, 19), Point(1, 19)])
    shippingdockcorner = Point(0, 18)
    chargers = [Charger(Point(5, 0)), Charger(Point(6, 0)), Charger(Point(7, 0)), Charger(Point(8, 0)), Charger(Point(9, 0))]
    robots = [Robot('A', Point(5, 0)), Robot('B', Point(6, 0)), Robot('C', Point(7, 0)), Robot('D', Point(8, 0)), Robot('E', Point(9, 0))]
    """
    # 10 x 10
    warehouse_width = 10
    warehouse_depth = 10

    picker_location = Point(1, 7)
    packer_location = Point(1, 4)
    shipping_dock = DockArea([Point(0, 0), Point(1, 0), Point(0, 1), Point(1, 1)])
    shipping_dock_corner = Point(0, 1)
    chargers = [Charger(Point(2, 9)), Charger(Point(3, 9)), Charger(Point(4, 9)), Charger(Point(5, 9)),
                Charger(Point(6, 9))]
    # robots = [Robot('A', Point(2, 9)), Robot('B', Point(3, 9)), Robot('C', Point(4, 9)), Robot('D', Point(5, 9)),
    #          Robot('E', Point(6, 9))]

    def __init__(self, env):
        """
        Inits Floor with the simulation environment

        During initialization, Floor creates all aspects of the warehouse requiring the use of Floor. Floor
        creates each Cell that will be within the warehouse and populates them by creating necessary objects.

        Creates the Picker, Packer, and Charger objects and populates Shelf Areas and Belt Areas with their objects

        Args:
            env: SimPy simulation environment
        """
        self.clock = env
        self.random_seed = 1
        self.all_points = {}
        self.shelf_areas = []
        self.belt_areas = []
        self.picker = Picker(self.picker_location)
        self.packer = Packer(self.packer_location)
        self.populateShelfArea()
        self.populateBeltArea()

        # For each tile in width x depth areas
        for x in range(0, self.warehouse_width):
            for y in range(0, self.warehouse_depth):
                point = Point(x, y)

                # check if this point already has a cell in a shelf area
                # and if so, just use the existing cell
                # will be the new cell created for this point
                cell = Cell(point)

                # Create the ShelfAreas
                for s in self.shelf_areas:
                    if s.hasWithin(point):
                        cell = s.getCell(point)
                        assert cell is not None

                # Create the Cell for Picker
                if self.picker_location.x == point.x and self.picker_location.y == point.y:
                    cell.setContents(self.picker)

                # Create the Cell for Packer
                if self.packer_location.x == point.x and self.packer_location.y == point.y:
                    cell.setContents(self.packer)

                # Create the Chargers
                for charger in self.chargers:
                    if charger.location.x == point.x and charger.location.y == point.y:
                        cell.setContents(charger)

                #for robot in self.robots:
                #    if robot.location.x == point.x and robot.location.y == point.y:
                #        #print("Charger")
                #        cell.setContents(robot)
                #        robot.setCell(cell)
                #        #print(cell)
                #        #print(cell.getContents())

                # Create the Dock Area
                for p in self.shipping_dock.points:
                    if p.x == point.x and p.y == point.y:
                        cell.setContents(self.shipping_dock)

                # Creating BeltArea
                for b in self.belt_areas:
                    if b.isWithin(point):
                        cell = b.getCell(point)
                        assert cell is not None

                # Adds to the dictionary as {Point: Cell}
                self.all_points.update({str(point): cell})

    def populateShelfArea(self):
        """
        Creates two instances of Shelf Areas to place on the Floor

        Current values are for a 10x10 layout
        """
        self.shelf_areas.append(ShelfArea(Point(5, 1), 5))
        self.shelf_areas.append(ShelfArea(Point(5, 5), 5))

    def populateBeltArea(self):
        """
        Creates an instance of Belt Area to place on the Floor

        Current values are for a 10x10 layout
        """
        distance = self.picker_location.y - self.shipping_dock_corner.y

        # Make the Belt Area one left of Picker, and all the way to Shipping Dock
        self.belt_areas.append(BeltArea(self, Point(self.picker_location.x - 1, self.picker_location.y), distance))

    def getCell(self, point):
        """
        Returns the Cell on Floor at a desired Point location

        Args:
            point: Point location we are looking for a Cell

        Returns:
            Cell object located at point
        """
        return self.all_points.get(str(point))

    def getCellCoord(self, x, y):
        """
        Returns the Cell on Floor at a desired Point, but with coordinate values instead of a Point

         Args:
            x: Integer of x coordinate
            y: Integer of y coordinate

        Returns:
            Cell object located at specified coordinate
        """
        return self.getCell(Point(x, y))

    def getWarehouseWidth(self):
        """
        Returns the width of the floor

        Returns:
            Integer representing width
        """
        return self.warehouse_width

    def getWarehouseDepth(self):
        """
        Returns the depth of the floor

        Returns:
            Integer representing depth
        """
        return self.warehouse_depth

    def getPicker(self):
        """
        Returns the Picker object on the Floor

        Returns:
            Picker object
        """
        return self.picker

    def getPickerLocation(self):
        """
        Returns the Picker's location on the Floor

        Returns:
            The Point location of the Picker
        """
        return self.picker_location

    def getPacker(self):
        """
        Returns the Packer object on the Floor

        Returns:
            Packer object
        """
        return self.packer

    def getPackerLocation(self):
        """
        Returns the Packer's location on the Floor

        Returns:
            The Point location of the Packer
        """
        return self.packer_location

    def getShippingDock(self):
        """
        Returns the location of the corner of the Shipping Dock

        Returns:
            The Point location of Shipping Dock
        """
        return self.shipping_dock_corner

    def getChargerLocation(self, robot):
        """
        Returns the Point location of a Robot's home Charger

        Args:
            robot: Robot object looking for Charger

        Returns:
            Point object representing Charger location
        """
        charger_location = robot.getChargerLocation()
        return charger_location

    # Is this needed?
    #def getBeltArea(self):
    #    """
    #    Returns the home location of the Shelf object

    #    Returns:
    #        The Point object, home_location of the shelf object
    #    """
    #    belt_area = []
    #    for i in range(self.picker_location.x, 0):
    #        belt_area.add(Point(i, 0))
    #    return belt_area

    def getNumShelfAreas(self):
        """
        Returns the number of Shelf Areas on Floor

        Returns:
            Integer representing number of Shelf Areas
        """
        return len(self.shelf_areas)

    def getShelfArea(self, number):
        """
        Returns a Shelf Area matching a specified number

        Args:
            number: Integer representing a ShelfArea number

        Returns:
            Shelf Area object matching number
        """
        return self.shelf_areas[number]

    def getPath(self, start_point, end_point):
        """
        Maps a path through the Floor from start_point to end_point without colliding into any other objects

        Args:
            start_point: Point object where the Robot is starting at
            end_point: Point object where the Robot will end up at

        Returns:
            item: A list of Points representing the path the Robot will take (Steps are in order)
        """
        path_x = []
        path_y = []

        # We will do move Left/Right first (X)
        # Then move Up/Down after (Y)

        # Calculate whether or not we need to Left or Right
        distance_lr = start_point.x - end_point.x

        if distance_lr < 0:

            for i in range(abs(distance_lr)):
                next_x = start_point.x + (i + 1)
                current_y = start_point.y
                # Only moving L/R so Y stays the same
                path_x.append(Point(next_x, current_y))

        if distance_lr > 0:

            for i in range(abs(distance_lr)):
                next_x = start_point.x - (i + 1)
                current_y = start_point.y
                # Only moving L/R so Y stays the same
                path_x.append(Point(next_x, current_y))

        # Calculate whether or not we need to Up or Down
        distance_ud = start_point.y - end_point.y

        if distance_ud < 0:

            for i in range(abs(distance_ud)):
                # Use endpoint.x here because we already have pathed out final x location
                current_x = end_point.x
                next_y = start_point.y + (i + 1)
                # Only moving U/D so X stays the same
                path_y.append(Point(current_x, next_y))

        if distance_ud > 0:

            for i in range(abs(distance_ud)):
                # Use endpoint.x here because we already have pathed out final x location
                current_x = end_point.x
                next_y = start_point.y - (i + 1)
                # Only moving U/D so X stays the same
                path_y.append(Point(current_x, next_y))

        # Combine the two Paths, X steps first then Y steps
        full_path = path_x + path_y

        return full_path

    def locateShelf(self, shelf_number):
        """
        Returns a Shelf Area that contains a Shelf matching a specified number

        Args:
            shelf_number: Integer representing a Shelf's number

        Returns:
            s_area: Shelf Area object contain Shelf matching number

        Raises:
            Exception: Shelf cannot be found
        """
        for s_area in self.shelf_areas:
            for cell in s_area.area_contents:
                cell_cont = cell.getContents()
                shelf = cell_cont[0]
                if shelf_number == shelf.getShelfNo():
                    return s_area

        raise Exception(f'Cannot find a Shelf with number {shelf_number}')

    def randomShelfArea(self):
        """
        Returns a random Point within a randomly chosen Shelf Area

        Returns:
            Point object that is located in a Shelf Area
        """
        s = self.random_seed.randint(len(self.shelf_areas))
        return self.shelf_areas[s].randomPoint()

    def printMap(self):
        """
        Prints out every Cell within Floor in a manner that allows us to see layout of the warehouse

        Prints out each row of Cells and changes what is displayed depending on what is in each Cell
        """
        line_print = {}
        row_contents = []

        # Reversed so that Points will match how Display presents  (Top left corner is (0, 0)
        for i in range(0, self.warehouse_depth):
            y_coord = i
            for j in range(0, self.warehouse_width):
                x_coord = j
                cell_at_coord = self.all_points[f'Point x:{x_coord} y:{y_coord}']
                obj_list = cell_at_coord.getContents()

                # If Contents is empty, move to the next Cell
                if len(obj_list) == 0:
                    row_contents.append('[      ]')
                    continue

                # If Cell contains an Object
                if len(obj_list) == 1:
                    obj_at_coord = obj_list[0]

                    if isinstance(obj_at_coord, Shelf):
                        row_contents.append(f"Shelf {obj_at_coord.shelf_number}")

                    if isinstance(obj_at_coord, Robot):
                        row_contents.append(f"Robot {obj_at_coord.getName()}")

                    if isinstance(obj_at_coord, Belt):
                        row_contents.append(f"Belt {obj_at_coord.getBeltNo()}")

                    if isinstance(obj_at_coord, Picker):
                        row_contents.append(f"Picker")

                    if isinstance(obj_at_coord, Packer):
                        row_contents.append(f"Packer")

                    if isinstance(obj_at_coord, Charger):
                        row_contents.append(f"Charger")

                    if isinstance(obj_at_coord, DockArea):
                        row_contents.append(f'Dock')

                # If Cell contains two Objects
                if len(obj_list) == 2:

                    # [Charger, Robot]
                    if isinstance(obj_list[0], Charger) and isinstance(obj_list[1], Robot):
                        rowContents.append(f'Char/Rob{obj_list[1].getName()}')

                    # [Robot, Charger]
                    if isinstance(obj_list[0], Robot) and isinstance(obj_list[1], Charger):
                        rowContents.append(f'Char/Rob{obj_list[0].getName()}')

                    # [Shelf, Robot]
                    if isinstance(obj_list[0], Shelf) and isinstance(obj_list[1], Robot):
                        rowContents.append(f'Sh{obj_list[0].getShelfNo()}/Rob{obj_list[1].getName()}')

                    # [Robot, Shelf]
                    if isinstance(obj_list[0], Robot) and isinstance(obj_list[1], Shelf):
                        rowContents.append(f'Sh{obj_list[1].getShelfNo()}/Rob{obj_list[0].getName()}')

                    # [Belt, Bin]
                    if isinstance(obj_list[0], Belt) and isinstance(obj_list[1], Bin):
                        rowContents.append(f'Bel{obj_list[0].getBeltNo()}/Bin{obj_list[1].binId}')

                    # [Bin, Belt]
                    if isinstance(obj_list[0], Bin) and isinstance(obj_list[1], Belt):
                        rowContents.append(f'Bel{obj_list[1].getBeltNo()}/Bin{obj_list[0].binId}')

                    # [Belt, Package]
                    if isinstance(obj_list[0], Belt) and isinstance(obj_list[1], Package):
                        rowContents.append(f'Bel{obj_list[0].getBeltNo()}/Package')

                    # [Package, Belt]
                    if isinstance(obj_list[0], Package) and isinstance(obj_list[1], Belt):
                        rowContents.append(f'Bel{obj_list[1].getBeltNo()}/Package')

            line_print[f'Row {i}'] = row_contents

            # Reset for next row
            rowContents = []

        for row in line_print:
            print(row, line_print[row])

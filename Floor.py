
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
import PathFinding


class Floor:
    """
    Floor class is the collection of Cells that make the warehouse environment

    Each Cell represents one tile on Floor, and each Cell can contain multiple objects

    Class Variables:
        warehouse_width: Integer representing the width of the warehouse
        warehouse_depth: Integer representing the depth of the warehouse

    Attributes:
        clock: Reference to SimPy simulation environment for deterministic randomness
        random_seed: Seed for random generation
        all_points: A dictionary of {string: Cell} for all points on the floor
        picker: The Picker object within the warehouse
        packer: The Packer object within the warehouse
        chargers: List of Charger objects within the warehouse
        robots: List of Robot objects within the warehouse
        shipping_dock: DockArea object that will be in the upper-left corner of the warehouse
        shipping_dock_corner: Point object that is within shipping_dock that is next to the Belt (bottom-right)
        shelf_areas: A list of ShelfArea objects
        belt_areas: A list of BeltArea objects
    """
    # 10 x 10
    warehouse_width = 10
    warehouse_depth = 10

    def __init__(self, env):
        """
        Inits Floor with the simulation environment

        Floor receives values for all of it's attributes after calling it's own buildFloor method
        which creates and populates every Cell on the Floor

        Args:
            env: SimPy simulation environment
        """
        self.clock = env
        self.random_seed = 1
        self.all_points = {}
        self.picker = None
        self.packer = None
        self.chargers = None
        self.robots = None
        self.shipping_dock = None
        self.shipping_dock_corner = None
        self.shelf_areas = None
        self.belt_areas = None

        self.buildFloor()

    def buildFloor(self):
        """
        Creates a Cell for each location on the floor and creates objects that will initially start
        on the Floor. Initial Point locations for the warehouse Floor are set here.

        Goes through every Point location within Floor and creates a new Cell for it. If there is
        an object that has a matching Point location as the new Cell, that object is added to the
        Cell as well

        Creates Picker, Packer, Robots, Chargers, as well as the DockArea, BeltArea, and ShelveAreas

        Current values are for a 10x10 floor layout

        Called during initialization
        """
        # Set Locations for objects and create instances
        picker_location = Point(1, 7)
        picker = Picker(picker_location)

        packer_location = Point(1, 4)
        packer = Packer(packer_location)

        shipping_dock = DockArea([Point(0, 0), Point(1, 0), Point(0, 1), Point(1, 1)])
        shipping_dock_corner = Point(0, 1)

        chargers = [Charger(Point(2, 9)), Charger(Point(3, 9)), Charger(Point(4, 9)), Charger(Point(5, 9)),
                    Charger(Point(6, 9))]

        robots = [Robot('A', Point(2, 9)), Robot('B', Point(3, 9)), Robot('C', Point(4, 9)), Robot('D', Point(5, 9)),
                  Robot('E', Point(6, 9))]

        shelf_areas = [ShelfArea(Point(5, 1), 5), ShelfArea(Point(5, 5), 5)]

        belt_length = picker_location.y - shipping_dock_corner.y
        belt_areas = [BeltArea(self, Point(picker_location.x - 1, picker_location.y), belt_length)]

        # Once everything has been created, give them to Floor
        self.picker = picker
        self.packer = packer
        self.shipping_dock = shipping_dock
        self.shipping_dock_corner = shipping_dock_corner
        self.chargers = chargers
        self.robots = robots
        self.shelf_areas = shelf_areas
        self.belt_areas = belt_areas

        # For each Point location in the warehouse, create a new Cell and if there is an object
        # that has a matching Point location, add that object to the Cell
        for x in range(0, self.warehouse_width):
            for y in range(0, self.warehouse_depth):
                point = Point(x, y)
                # Create Cell for point location
                cell = Cell(point)

                # Check if Point location matches Picker location
                if picker.getPickLocation().x == point.x and picker.getPickLocation().y == point.y:
                    cell.setContents(self.picker)

                # Check if Point location matched Packer location
                if self.packer.getLocation().x == point.x and packer.getLocation().y == point.y:
                    cell.setContents(self.packer)

                # Check if Point location matched Dock Area location
                for p in self.shipping_dock.points:
                    if p.x == point.x and p.y == point.y:
                        cell.setContents(self.shipping_dock)

                # Check the Chargers to see if any match Point location
                for charger in self.chargers:
                    if charger.location.x == point.x and charger.location.y == point.y:
                        cell.setContents(charger)

                # Check the Robots to see if any match Point location
                for robot in self.robots:
                    if robot.location.x == point.x and robot.location.y == point.y:
                        cell.setContents(robot)
                        robot.setCell(cell)

                # Check the Shelf Areas for Shelves that match Point location
                # Cell are already created within Shelf Area so use those Cells if matching location
                for s in self.shelf_areas:
                    if s.hasWithin(point):
                        cell = s.getCell(point)
                        assert cell is not None

                # Check the Belt Areas for Belts that match Point location
                # Cell are already created within Belt Area so use those Cells if matching location
                for b in self.belt_areas:
                    if b.isWithin(point):
                        cell = b.getCell(point)
                        assert cell is not None

                # Adds to the dictionary as {Point: Cell}
                self.all_points.update({str(point): cell})

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
        return self.picker.getPickLocation()

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
        return self.packer.getLocation()

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

        Keeping this for the time being for display purposes for a later write-up of the project

        Args:
            start_point: Point object where the Robot is starting at
            end_point: Point object where the Robot will end up at

        Returns:
            full_path: A list of Points representing the path the Robot will take (Steps are in order)
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

    def getPath2(self, start_point, end_point):
        """
        Maps a path through the Floor from start_point to end_point

        PathFinding uses an A* algorithm to map out an optimal path

        First calls floorGrid to get a grid layout of the Floor for the path finding algorithm
        Then calls aStar in pathFinding which maps out a path from start_point to end_point without
        colliding with any other objects on the warehouse floor

        Args:
            start_point: Point object where the Robot is starting at
            end_point: Point object where the Robot will end up at

        Returns:
            full_path: A list of Points representing the path the Robot will take (Steps are in order)
        """
        floor_grid = self.floorGrid(start_point, end_point)

        full_path = PathFinding.aStar(floor_grid, start_point, end_point)

        return full_path

    def floorGrid(self, start, end):
        """
        Creates a matrix grid of the warehouse floor layout. If there is an object located there, there will be a 1
        if there is no object, there will be a 0

        The only exception are for the specified start point and end point, which will be switched to 0


        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0]      A grid from (3, 9) to (1, 6) would look like this
        [1, 1, 0, 0, 0, 1, E, 1, 1, 1]      except for the S representing start and the E representing
        [1, 0, 0, 0, 0, 1, 1, 1, 1, 1]      end would be 0's
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        [1, 0, 0, 0, 0, 1, 1, 1, 1, 1]
        [1, 0, 0, 0, 0, 1, 1, 1, 1, 1]
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        [0, 0, 1, S, 1, 1, 1, 0, 0, 0]

        Args
            start: Point object where the path starts
            end: Point object where the path ends

        Returns
            grid: A Matrix for the PathFinding Class
        """
        grid = []
        row_contents = []

        for i in range(0, self.warehouse_depth):
            y_coord = i
            for j in range(0, self.warehouse_width):
                x_coord = j
                cell_at_coord = self.all_points[f'Point x:{x_coord} y:{y_coord}']
                obj_list = cell_at_coord.getContents()

                # If Contents is empty, move to the next Cell
                if len(obj_list) == 0:
                    row_contents.append(0)
                    continue

                # If Cell contains an Object
                if len(obj_list) == 1:
                    # Either the start or end point, place a 0
                    if cell_at_coord.cellLocation().x == start.x and cell_at_coord.cellLocation().y == start.y  \
                            or cell_at_coord.cellLocation().x == end.x and cell_at_coord.cellLocation().y == end.y:
                        row_contents.append(0)
                        continue
                    else:
                        row_contents.append(1)

                # If Cell contains two Objects
                if len(obj_list) == 2:
                    # Either the start or end point, place a 0
                    if cell_at_coord.cellLocation().x == start.x and cell_at_coord.cellLocation().y == start.y  \
                            or cell_at_coord.cellLocation().x == end.x and cell_at_coord.cellLocation().y == end.y:
                        row_contents.append(0)
                        continue
                    else:
                        row_contents.append(1)

            grid.append(row_contents)
            # Reset for next row
            row_contents = []

        # For testing as of now
        # for row in grid:
        #     print(row)

        return grid

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
                        row_contents.append(f'Char/Rob{obj_list[1].getName()}')

                    # [Robot, Charger]
                    if isinstance(obj_list[0], Robot) and isinstance(obj_list[1], Charger):
                        row_contents.append(f'Char/Rob{obj_list[0].getName()}')

                    # [Shelf, Robot]
                    if isinstance(obj_list[0], Shelf) and isinstance(obj_list[1], Robot):
                        row_contents.append(f'Sh{obj_list[0].getShelfNo()}/Rob{obj_list[1].getName()}')

                    # [Robot, Shelf]
                    if isinstance(obj_list[0], Robot) and isinstance(obj_list[1], Shelf):
                        row_contents.append(f'Sh{obj_list[1].getShelfNo()}/Rob{obj_list[0].getName()}')

                    # [Belt, Bin]
                    if isinstance(obj_list[0], Belt) and isinstance(obj_list[1], Bin):
                        row_contents.append(f'Bel{obj_list[0].getBeltNo()}/Bin{obj_list[1].binId}')

                    # [Bin, Belt]
                    if isinstance(obj_list[0], Bin) and isinstance(obj_list[1], Belt):
                        row_contents.append(f'Bel{obj_list[1].getBeltNo()}/Bin{obj_list[0].binId}')

                    # [Belt, Package]
                    if isinstance(obj_list[0], Belt) and isinstance(obj_list[1], Package):
                        row_contents.append(f'Bel{obj_list[0].getBeltNo()}/Package')

                    # [Package, Belt]
                    if isinstance(obj_list[0], Package) and isinstance(obj_list[1], Belt):
                        row_contents.append(f'Bel{obj_list[1].getBeltNo()}/Package')

            line_print[f'Row {i}'] = row_contents

            # Reset for next row
            row_contents = []

        for row in line_print:
            print(row, line_print[row])

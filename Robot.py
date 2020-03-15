
class Robot:
    """
        Robot class represents the robots that move around the warehouse and move shelves from place to place

        Class Variables:
        num_of_robots: A integer used to count the total number of shelves created

        Attributes:
            robot_name: A string representing the name of the robot
            location: Point object that is the current location of the robot
            cell: Cell object that is the robots current location on the Floor and display
            charging: A boolean indicating if the robot is at a charging location
            holding_shelf: A Shelf object that is being carried by the robot
            destination: A list of Point objects that is the path of steps it will take to get to its destination

        """

    num_of_robots = 0

    def __init__(self, name, starting_location):
        """
        Inits Robot with a name and a starting location

        Args:
            name: A string to be used as the name of the Robot (Ex: Robot A)
            starting_location: A Point object marking the robots current location

        """
        self.robot_name = name
        self.location = starting_location
        self.cell = None
        self.charging = True            # Is True because robots start on a charging station
        self.holding_shelf = None
        self.destination = None
        Robot.num_of_robots += 1

    def getDestination(self):
        """
        Returns the path that the robot needs to take to get to its destination

        Returns:
            destination: A list of Points
        """
        return self.destination

    def setCell(self, cell):
        """
        Changes the Cell that Robot is located at to cell and changes Robot's location

        Args:
            cell: A Cell object that the robot's location will be changed to
        """
        self.cell = cell
        self.setLocation(cell.cellLocation())

    def getCell(self):
        """
        Returns the Cell that the robot is located at

        Returns:
            The Cell object containing this Robot
        """
        return self.cell

    def getName(self):
        """
         Returns the name of the Robot object

         Returns:
             The robot_name of the Robot object
         """
        return self.robot_name

    def getLocation(self):
        """
        Returns the point location of the Robot object

        Returns:
            The Point object location of the Robot
        """
        return self.location

    def setLocation(self, new_location):
        """
        Changes the Point that Robot is located at to new_location

        Args:
            new_location: A Point object that the robot's location will be changed to
        """
        self.location = new_location

    def pickUpShelf(self, new_shelf):
        """
        The Robot "picks up" new_shelf by adding it to holding_shelf

        Args:
            new_shelf: A Shelf object which is no longer resting
        """
        self.holding_shelf = new_shelf
        self.holding_shelf.resting = False

    def putDownShelf(self, shelf_held):
        """
        The Robot "puts down" shelf_held by removing it from holding_shelf

        Args:
            shelf_held: A Shelf object which now resting
        """
        self.holding_shelf.resting = True
        self.holding_shelf = None

    def getHoldingShelf(self):
        """
        Returns the Shelf that robot is currently holding

        Returns:
            The holding_shelf of the Robot object
        """
        return self.holding_shelf

    def setDestination(self, new_destination):
        """
        Changes the path that Robot will follow to a destination

        Args:
            new_destination: A list of Point objects
        """
        self.destination = new_destination

    def __repr__(self):
        """
        Unambiguous representation of Robot object

        Used for debugging and logging

        Returns:
            In the format: Robot(robot_name, location, holding_shelf)
            Ex: Robot("C", Point(5, 2), Shelf 4)
        """
        return "Robot('{}', {}, {})".format(self.robot_name, self.location, self.holding_shelf)

    def __str__(self):
        """
        Readable representation of Robot object

        Used for display

        Returns:
            In the format: Robot: "C" - Location: Point(5, 2) - Shelf: 4
        """
        return 'Robot: {} - Location: {} - Shelf Held: {}'.format(self.robot_name, self.location,
                                                                  self.holding_shelf)

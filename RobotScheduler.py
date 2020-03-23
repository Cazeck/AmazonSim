
import random
from Point import Point
from Robot import Robot


class RobotScheduler:
    """
    RobotScheduler is responsible to keeping track of where all Robots are at all times and providing the Robots
    instruction on where they need to go and the path they should take to get there

    Is also responsible to creating each of the Robots in the warehouse

    Attributes:
        clock: Reference to SimPy simulation environment
        floor: Reference to the Floor component
        robot_list: A list of all Robots objects that are within the warehouse
        available_robots: A list of Robot objects which contain Robots that are not currently doing something
    """

    def __init__(self, env, floor):
        """
        Inits Inventory with the simulation environment and a reference to warehouse Floor layout

        During initialization, RobotScheduler call populate() in order to receive all Robots that have been
        placed on the floor

        Args:
            env: SimPy simulation environment
            floor: Floor object so we can communicate with this subset
        """
        self.clock = env
        self.floor = floor
        self.robot_list = []
        self.available_robots = []
        self.populate()

    def numberOfRobots(self):
        """
        Count the total number of Robots the RobotScheduler has control over

        Returns:
            Integer representing the number of Robots within robot_list
        """
        return len(self.robot_list)

    def addRobot(self, robot):
        """
        Adds a Robot object to RobotScheduler

        Args:
            robot: Robot object to be added
        """
        self.robot_list.append(robot)

    def findRobot(self, name):
        """
        Find a Robot with a specified name in RobotScheduler

        Args:
            name: String representing a Robot's name

        Raises:
            Exception: Robot with matching name cannot be found
        """
        for i in self.robot_list:
            if name == i.robot_name:
                return i

        raise Exception(f'Robot with name {name} cannot be found')

    def chargingRobots(self):
        """
        Find all Robots that are currently doing nothing (Charging)

        Returns:
            self.available_robots: List of Robot objects that are not busy
        """
        for robot in self.robot_list:
            if robot.charging == True:
                self.available_robots.append(robot)
            else:
                # This robot is busy, check another
                print(f'robot {robot} is not charging')
                continue

        return self.available_robots

    def findAvailableRobot(self):
        """
        Finds a random Robot that is currently charging for a task

        Returns:
            robot: A Robot object that is not busy
        """
        robot = random.choice(self.available_robots)
        return robot

    def populate(self):
        """
        Takes every Robots that is located on Floor and adds them to robot_list

        After that it checks to see if they are all charging
        """
        floor_robots = self.floor.robots

        for robot in floor_robots:
            self.addRobot(robot)

        # Check if new robots are charging
        self.chargingRobots()

    def robotPath(self, robot, destination):
        """
        Asks Floor component to calculate the path from a Robot's current location to a desired destination.

        After the path is calculated, give the directions to the specified Robot

        Args:
            robot: Robot object we are calculating the path for
            destination: Point object that we want to send the Robot to
        """
        robot_location = robot.getLocation()

        # Get Path by Calling Floor's GetPath
        path = self.floor.getPath(robot_location, destination)
        path_length = len(path)

        robot.setDestination(path)

    def moveRobotToDest(self, robot):
        """
        RobotScheduler tells a specific Robot to move to its destination step-by-step

        For each step in Robot's path, call moveByOne. This is helpful for our event-based simulation

        Args:
            robot: Robot object we are moving around the warehouse
        """
        path_length = len(robot.getDestination())
        for num in range(0, path_length):
            self.moveByOne(robot)

    def moveByOne(self, robot):
        """
        Move a specific Robot and its contents one unit forward following the Robot's path

        Args:
            robot: Robot object we are moving around the warehouse
        """
        # If robot is holding a Shelf
        if robot.getHoldingShelf() is not None and robot.getDestination() != []:
            current_cell = robot.getCell()

            # Next step in Robot's path
            next_cell = self.floor.getCell(robot.getDestination()[0])
            shelf_held = robot.getHoldingShelf()

            # Adding Robot to next Cell
            next_cell.setContents(robot)
            robot.setCell(next_cell)

            # Adding Shelf to next Cell
            next_cell.setContents(shelf_held)

            # Removing Robot from current Cell
            current_cell.removeContent(robot)
            current_cell.removeContent(shelf_held)

            # Remove first Point from destination
            del robot.destination[0]

        # If robot is moving by itself
        else:
            current_cell = robot.getCell()
            next_cell = self.floor.getCell(robot.getDestination()[0])

            # Adding Robot to next Cell
            next_cell.setContents(robot)
            robot.setCell(next_cell)

            # Removing Robot from current Cell
            current_cell.removeContent(robot)

            # Remove first Point from destination
            del robot.destination[0]

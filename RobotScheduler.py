from Point import Point
from Robot import Robot
from Cell import Cell
from Floor import Floor

class RobotScheduler:

    def __init__(self, env, floor):
        self.clock = env
        self.floor = floor
        # for 20 x 20
        # self.robotList = [Robot('A', Point(5, 0)), Robot('B', Point(6, 0)), Robot('C', Point(7, 0)), Robot('D', Point(8, 0)), Robot('E', Point(9, 0))]
        self.robotList = [Robot('A', Point(2, 9)), Robot('B', Point(3, 9)), Robot('C', Point(4, 9)), Robot('D', Point(5, 9)), Robot('E', Point(6, 9))]
        self.availableRobots = []

        self.populate()

    # Returns total number of robots in RobotScheduler
    def numberOfRobots(self):
        return len(self.robotList)

    # Add robot to the scheduler
    def addRobot(self, robot):
        self.robotList.append(robot)

    # Finds a Robot with specified name
    def findRobot(self, name):
        for i in self.robotList:
            if name == i.robotName:
                return i
        return None  # item not found with matching name

    # Find all robots that are currently idle
    def idleRobots(self):
        #idle_bots = []
        for i in self.robotList:
            if i.status == 0:
                #idle_bots.append(i)
                self.availableRobots.append(i)
            else:
                continue  # this robot is busy, check another

        #self.availableRobots = idle_bots
        return self.availableRobots

    # Returns first available robot in list
    def findAvailableRobot(self):
        return self.availableRobots[0]

    # sendRobot?  which finds an available robot and then sends it to that location with pathing coordinates

    # Will take the robots from robotList and distribute them into Cells on Floor
    def populate(self):

        # For each location on floor
        for y in range(0, self.floor.warehousedepth):
            for x in range(0, self.floor.warehousewidth):
                point = Point(x, y)
                for robot in self.robotList:
                    if robot.location.x == point.x and robot.location.y == point.y:
                        cellAtLocation = self.floor.getCell(point)
                        cellAtLocation.setContents(robot)
                        robot.setCell(cellAtLocation)

        # Check if new robots are idle. If so, add then to idleList
        self.idleRobots()

    # CAN BE REMOVED FROM HERE WHEN IT IS TESTED TO WORK WITHIN FLOOR

    # Maps a path from the robots current location to the endPoing
    # Will later make sure it doesn't run into anything
    # returns a list of points (the path the robot will take in order)
    def mapDestination(self, robot, endpoint):
        pathX = []
        pathY = []

        # We will do move Left/Right first (X)
        # Then move Up/Down after (Y)

        # Calculate whether or not we need to Left or Right
        distanceLR = robot.location.x - endpoint.x

        if distanceLR < 0:
            #print("We need to move " + str(abs(distanceLR)) + " units Right")

            for i in range(abs(distanceLR)):
                nextX = robot.location.x + (i + 1)
                currentY = robot.location.y
                # Only moving L/R so Y stays the same
                pathX.append(Point(nextX, currentY))
                #print(pathX)

        if distanceLR > 0:
            #print("We need to move " + str(abs(distanceLR)) + " units Left")

            for i in range(abs(distanceLR)):
                nextX = robot.location.x - (i + 1)
                currentY = robot.location.y
                # Only moving L/R so Y stays the same
                pathX.append(Point(nextX, currentY))
                #print(pathX)

        # Calculate whether or not we need to Up or Down
        distanceUD = robot.location.y - endpoint.y

        if distanceUD < 0:
            #print("We need to move " + str(abs(distanceUD)) + " units Up")

            for i in range(abs(distanceUD)):
                # Use endpoint.x here because we already have pathed out final x location
                currentX = endpoint.x
                nextY = robot.location.y + (i + 1)
                # Only moving U/D so X stays the same
                pathY.append(Point(currentX, nextY))
                #print(pathY)

        if distanceUD > 0:
            #print("We need to move " + str(abs(distanceUD)) + " units Down")

            for i in range(abs(distanceUD)):
                # Use endpoint.x here because we already have pathed out final x location
                currentX = endpoint.x
                nextY = robot.location.y - (i + 1)
                # Only moving U/D so X stays the same
                pathY.append(Point(currentX, nextY))
                #print(pathY)

        # Combine the two Paths, X steps first then Y steps
        fullPath = pathX + pathY

        return fullPath


    # Asks Floor to calculate path from robot -> destination
    def robotPath(self, robot, destination):
        robotlocation = robot.getLocation()

        # Get Path by Calling Floor's GetPath
        path = self.floor.getPath(robotlocation, destination)
        pathlength = len(path)

        robot.setDestination(path)

        # Moving the Robot to location
        # Running moveByOne multiple times  to emulate ticks for time being
        #for num in range(0, pathlength):
        #    self.moveByOne(robot)

    # Make a Robot move to its set destination
    def moveRobotToDest(self, robot):
        path_length = len(robot.getDestination())
        for num in range(0, path_length):
            self.moveByOne(robot)

    # New Version of Robot's
    def moveByOne(self, robot):

        # If robot is holding a Shelf
        if robot.holdingShelf is not None and robot.getDestination() != []:

            currentcell = robot.getCell()
            nextcell = self.floor.getCell(robot.getDestination()[0])
            shelfheld = robot.getHoldingShelf()

            #print(f'Current Cell is: {currentcell}')
            #print(f'Next Cell is: {nextcell}')

            # Adding Robot to next Cell
            nextcell.setContents(robot)
            robot.setCell(nextcell)

            # Adding Shelf to next Cell
            nextcell.setContents(shelfheld)

            # Removing Robot from current Cell
            currentcell.removeContent(robot)
            currentcell.removeContent(shelfheld)

            # Remove first Point from destination
            del robot.destination[0]

        # If robot is moving by itself
        else:

            currentcell = robot.getCell()
            nextcell = self.floor.getCell(robot.getDestination()[0])
            #print(f'Current Cell is: {currentcell}')
            #print(f'Next Cell is: {nextcell}')

            # Adding Robot to next Cell
            nextcell.setContents(robot)
            robot.setCell(nextcell)

            # Removing Robot from current Cell
            currentcell.removeContent(robot)

            # Remove first Point from destination
            del robot.destination[0]


#env = 'meme'
#floor = Floor(env)

#rsched = RobotScheduler(env, floor)

#floor.printMap()

#robot1 = rsched.robotList[0]
#print('\n', robot1)

#shelf1 = floor.getCell(Point(10,10)).getContents()[0]
#print(shelf1)
#robot1.setDestination([Point(5, 1), Point(5, 2), Point(5, 3)])

#rsched.robotToDestination(robot1, Point(10,10))

#floor.printMap()

#robot1.pickUpShelf(shelf1)

#print(robot1)

#rsched.robotToDestination(robot1, Point(2,5))


#floor.printMap()

#print(floor.getCell(Point(2,5)).content)


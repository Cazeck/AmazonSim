from Point import Point
from Robot import Robot

class RobotScheduler:

    def __init__(self):
        self.robotList = []
        self.availableRobots = []

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
    def findAvailableRobots(self):
        for i in self.robotList:
            if i.status == 0:
                self.availableRobots.append(i)
            else:
                continue  # this robot is busy, check another

        return self.availableRobots

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
            print("We need to move " + str(abs(distanceLR)) + " units Right")

            for i in range(abs(distanceLR)):
                nextX = robot.location.x + (i + 1)
                currentY = robot.location.y
                # Only moving L/R so Y stays the same
                pathX.append(Point(nextX, currentY))
                #print(pathX)

        if distanceLR > 0:
            print("We need to move " + str(abs(distanceLR)) + " units Left")

            for i in range(abs(distanceLR)):
                nextX = robot.location.x - (i + 1)
                currentY = robot.location.y
                # Only moving L/R so Y stays the same
                pathX.append(Point(nextX, currentY))
                #print(pathX)

        # Calculate whether or not we need to Up or Down
        distanceUD = robot.location.y - endpoint.y

        if distanceUD < 0:
            print("We need to move " + str(abs(distanceUD)) + " units Up")

            for i in range(abs(distanceUD)):
                # Use endpoint.x here because we already have pathed out final x location
                currentX = endpoint.x
                nextY = robot.location.y + (i + 1)
                # Only moving U/D so X stays the same
                pathY.append(Point(currentX, nextY))
                #print(pathY)

        if distanceUD > 0:
            print("We need to move " + str(abs(distanceUD)) + " units Down")

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




#startPoint1 = Point(1,2)
#startPoint2 = Point(7,8)
#startPoint3 = Point(4,4)
#startPoint4 = Point(6,2)

#roboA= Robot('A', startPoint1)
#roboB = Robot('B', startPoint2)
#roboC= Robot('C', startPoint3)
#roboD = Robot('D', startPoint4)

#newLoc = Point(10, 10)
#newLoc2 = Point(0, 0)

#rSched = RobotScheduler()

#rSched.addRobot(roboA)
#rSched.addRobot(roboB)
#rSched.addRobot(roboC)
#rSched.addRobot(roboD)

#print(rSched.robotList)

#print(rSched.findRobot("B"))

#print(rSched.numberOfRobots())

#roboB.setState(3)
#roboC.setState(5)

#print(rSched.findAvailableRobots())


#rSched.mapDestination(roboB, newLoc)
#rSched.mapDestination(roboB, newLoc)

#roboB.setDestination(rSched.mapDestination(roboB, newLoc))

#newDest = rSched.mapDestination(roboB, newLoc)
#print(newDest)

#roboB.setDestination(newDest)
#roboB.goToDest()

#print(roboB.destination)
#print(newDest)

#roboB.goToDest()
#roboB.goToDest()
#roboB.goToDest()
#roboB.goToDest()
#roboB.goToDest()
#roboB.goToDest()

#print(newDest)
#print(roboB.destination)
#print(roboA.destination)
#roboA.moveByOne()

#print(roboA.destination)
#print(roboA.setDestination(newDest))

#roboA.goTo(newDest)
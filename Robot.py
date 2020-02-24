from Point import Point

class Robot:

    numofrobots = 0
    # Stages for where the robot is while processing an order
    # status will use these values
    idle = 0
    pickershelfbound = 1
    pickerbound = 2
    atpicker = 3
    afterpickershelfbound = 4
    dockshelfbound = 5
    atdock = 7
    afterdockshelfbound = 8
    chargerbound = 9

    def __init__(self, name, startinglocation):
        self.location = startinglocation
        self.status = 0             # start off idle
        self.destination = None       # Will be a point object List of points? Next point needed to go you 1 by 1
        self.holdingShelf = None    # Number of shelf that it is holding
        self.shelflocation = None   # Location of the shelf that it needs to get / return
        self.picker = None
        self.dock = None
        self.robotName = name

        Robot.numofrobots += 1

    # Return where the robot needs to go
    def getDestination(self):
        return self.destination

    # Return where the Robot is at
    def getLocation(self):
        return self.location

    # Return the robots current status
    def getStatus(self):
        return self.status

    # Return the shelf that it is currently holding
    def getholdingShelf(self):
        return self.holdingShelf

    # Change status for Robot
    def setState(self, newstate):
        self.status = newstate

    # Give the Robot a destination to go to
    # Destination will be a list of Points to follow
    def setDestination(self, destination):
        self.destination = destination

    # Method will be used by RobotScheduler every tick
    # to move the robot by one point
    def moveByOne(self):
        if self.destination != []:
            print("| Moving from: " + str(self.location) + " To: " + str(self.destination[0]))
            self.location = self.destination[0]     # Get next point in the list
            del self.destination[0]                 # Remove first point in the list
            #self.destination = self.destination[:]             # remove first point in the list

        else:
            print("Robot is already at destination!")
    # Will tell the robot to start heading to a new destination
    def goToDest(self):
        #self.destination = newDest
        self.moveByOne()


    # Umambiguous reperestation of object, used for debugging / loggin - seen for developers
    # Item('Bong', 67090, 4)
    def __repr__(self):
        return "Robot('{}', '{}', {}, {})".format(self.robotName, self.status, self.location, self.holdingShelf)

    # readable representation of an object, used for display to end users
    # Item: Hydras Lament - Serial No: 11008 - Shelf: None
    def __str__(self):
        return '| Robot: {} -  Status: {} - Location: {}  Shelf Held: {}'.format(self.robotName, self.status, self.location, self.holdingShelf)



#startPoint1 = Point(1,2)

#startPoint2 = Point(7,8)

#roboA= Robot('A', startPoint1)

#roboB = Robot('B', startPoint2)

#print(roboA)

#print(roboB)
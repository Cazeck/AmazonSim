import random
import simpy
from Point import Point

class Robot(object):

    numofrobots = 0

    def __init__(self, env, name, startinglocation):
        self.env = env
        self.location = startinglocation
        self.status = 0
        self.destination = None
        self.holdingshelf = None
        self.robotname = name

        self.action = env.process(self.run())

    def run(self):
        while True:
            print('\nMove forward one unit at: %d' % self.env.now)
            #charge_duration = 5

            # We yield the process that process() returns
            # to wait for it to finish
            yield self.env.process(self.goToDest())

            # The charge process has finished and we can start driving again
            #print('Start moving at %d' % self.env.now)
            #trip_duration = 5
            #yield self.env.timeout(trip_duration)

    def charge(self, duration):
        yield self.env.timeout(duration)

        # Return where the robot needs to go
    def getDestination(self):
        return self.destination

        # Return where the Robot is at
    def getLocation(self):
        return self.location

        # Return the robots current status
    def getStatus(self):
        return self.status

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
            print("Moving from: " + str(self.location) + " To: " + str(self.destination[0]))
            self.location = self.destination[0]
            del self.destination[0]

        else:
            print("Robot is already at destination!")

    # Will tell the robot to start heading to a new destination
    def goToDest(self):
        self.moveByOne()
        yield self.env.timeout(3)


#route = [Point(0,1), Point(0,2), Point(0,3), Point(1,3)]

#env = simpy.Environment()
#robot = Robot(env, 'A', Point(0,0))
#robot.setDestination(route)
#env.run(until=15)


class Warehouse(object):
    def __init__(self, env, numitems, timeathome):
        self.env = env
        self.items = simpy.Resource(env, numitems)
        self.timeathome = timeathome

    def sendOrder(self, order):
        print(f'sending item for {order}')
        yield self.env.timeout(self.timeathome)
        print(f'item from {order} is returned to warehouse')


def order(env, warehouse, name):
    print(f'{name} requesting item')
    with warehouse.items.request() as request:
        yield request
        yield env.process(warehouse.sendOrder(name))


def setup(env, numitems, timeathome, orderinterval):
    warehouse = Warehouse(env, numitems, timeathome)

    for i in range(1, 4):
        env.process(order(env, warehouse, 'Order %d' % i))

    while True:
        yield env.timeout(orderinterval)
        i += 1
        env.process(order(env, warehouse, 'Order %d' % i))


NUM_ITEMS = 1
TIMEATHOME = 2
ORDER_INTERVAL = 3
SIM_TIME = 8

env = simpy.Environment()
env.process(setup(env, NUM_ITEMS, TIMEATHOME, ORDER_INTERVAL))
env.run(until=SIM_TIME)

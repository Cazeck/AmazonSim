import simpy

from Item import Item
from Shelf import Shelf

from Inventory import Inventory
from ShelfArea import ShelfArea

from Point import Point
from Cell import Cell

from RobotScheduler import RobotScheduler
from Robot import Robot

# Test Instances of Areas
inv = Inventory()
sArea = ShelfArea()
rSched = RobotScheduler()

# Test Shelves
shelf1 = Shelf(1, 100)
shelf2 = Shelf(2, 200)

# Test Items
item1 = Item('Bagpipe', 51009)
item2 = Item('Tic-Tac', 57678)
item3 = Item('Hydras Lament', 11008)
item4 = Item('Socks', 13009)
item5 = Item('Puck', 34678)
item6 = Item('Shifters Shield', 81035)
item7 = Item('Tic-Tac', 57678)
item8 = Item('Singular Orange', 34231)

# Creating a few initial points that robots can be placed at
startPoint1 = Point(1,2)
startPoint2 = Point(7,8)
startPoint3 = Point(4,4)
startPoint4 = Point(6,2)

# Test Robots
roboA= Robot('A', startPoint1)
roboB = Robot('B', startPoint2)
roboC= Robot('C', startPoint3)
roboD = Robot('D', startPoint4)

# Test Locations to Path Robots to
newLoc = Point(10, 10)
newLoc2 = Point(0, 0)

# Add Shelves to Shelve Area
sArea.addShelve(shelf1)
sArea.addShelve(shelf2)

# Add Items to Inventory
inv.addItem(item2)
inv.addItem(item1)
inv.addItem(item3)
inv.addItem(item4)
inv.addItem(item5)
inv.addItem(item6)
inv.addItem(item7)
inv.addItem(item8)

# Add Robots to the Scheduler
rSched.addRobot(roboA)
rSched.addRobot(roboB)
rSched.addRobot(roboC)
rSched.addRobot(roboD)













# Placing items on to shelves
def placeItemOnShelf():
    for i in inv.stock:
        nShelf = sArea.findShelfWithSpace()
        i.changeShelf(nShelf.shelfNumber)
        nShelf.push(i)

placeItemOnShelf()

#print('Stock')
#print(inv.stock)

#print('Shelves')
#print(sArea.allShelves)

#print(inv.findItemSerial(81035))


#print(inv.findItemName('Puck'))


















































"""
# Messing around with simpy for a second to do the event based simulation

# Generator function that defines the working of the traffic light
# "timeout()" function makes next yield statement wait for a
# given time passed as the argument
def Traffic_Light(env):
    while True:
        print("Light turns GRN at " + str(env.now))

        # Light is green for 25 seconds
        yield env.timeout(25)

        print("Light turns YEL at " + str(env.now))

        # Light is yellow for 5 seconds
        yield env.timeout(5)

        print("Light turns RED at " + str(env.now))

        # Light is red for 60 seconds
        yield env.timeout(60)

    # env is the environment variable


env = simpy.Environment()

# The process defined by the function Traffic_Light(env)
# is added to the environment
env.process(Traffic_Light(env))

# The process is run for the first 180 seconds (180 is not included)
env.run(until=180)
"""
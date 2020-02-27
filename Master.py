import simpy
import random

from Floor import Floor

from Item import Item
from Shelf import Shelf

from Inventory import Inventory
from ShelfArea import ShelfArea

from Point import Point
from Cell import Cell

from Order import Order
from OrderControl import OrderControl

from RobotScheduler import RobotScheduler
from Robot import Robot

# Test Instances of Areas
sArea = ShelfArea(Point(0,0), 5) # Creates a 5 x 2 Grid for the shelf area
inv = Inventory()

# Need to distribute stock to the shelves we generated (Randomly works fine)

for i in inv.stock:
    #print(random.choice(sArea.areacontents).getContents())
    # Add the item to a random shelf in ShelfArea
    randomShelf = random.choice(sArea.areacontents).getContents()

    randomShelf.addItem(i)
    print("Adding " + str(i) + " to Shelf " + str(randomShelf.getShelfNo()))
    i.changeShelf(randomShelf.getShelfNo())

    #random.choice(sArea.areacontents).getContents().addItem(i)

#print(sArea.areacontents[0].content)
print('\nItems added to Shelves')

rSched = RobotScheduler()

print('Robots Created')

oControl = OrderControl()

print("Order Control Created")
print("\nOrders")
print(oControl.allOrders)

ord1 = oControl.allOrders[0]

ord1.updateStatus("In Progress")


rSched.idleRobots()



for item in ord1.orderitems:
    print("\nItem:")
    print(item)

    if inv.numberInStockName(item) > 0:
        itemlocation = inv.findItemName(item)
        print("Shelf Item is on:")
        print(itemlocation)

        # Now that we have which shelf it is on, we need to ask shelfArea where it is
        shelf = sArea.findShelf(itemlocation)
        print("\nShelf is located at:")
        print(shelf.currentLocation)

        # Then ask Robot Scheduler to send an available robot to that location
        robotToUse = rSched.findAvailableRobot()
        print("\nRobot is ready to use")
        print(robotToUse)

        # Calculating path for robot to take to get to that shelf
        robotPath = rSched.mapDestination(robotToUse, shelf.currentLocation.cellLocation())
        robotToUse.setDestination(robotPath)
        print("\nRobot has path added to shelf added")
        print(robotToUse.destination)

        # Now we need to make that robot move to the shelf
        robotToUse.setState(1) #PickerShelf Bound
        rSched.availableRobots.remove(robotToUse)  # Remove first robot from availability

        # Move the robot to Shelf
        for num in range(0, len(robotToUse.destination)):
            #print("We hav this many steps")
            #print(robotToUse.destination)
            #print(len(robotToUse.destination))
            robotToUse.moveByOne()
        print("Moving to shelf")
        print("\nRobot is at Shelf Location")
        print(robotToUse.getLocation())


        # Now that we are at the shelf, we need to pick it up and bring it to the picker's destination
        print("\npicking up shelf")
        robotToUse.pickUpShelf(shelf)
        print(robotToUse.holdingShelf)

        #picked up, now move to picker's location (updating both of the the items locations as we bgo

        # Find pickers location
        # for now its this point
        pickerLoc = Point(20, 20)

        # Recalculate the path
        robotPath = rSched.mapDestination(robotToUse, pickerLoc)
        robotToUse.setDestination(robotPath)
        print("\nRobot has path to Picker added")

        # Move there
        robotToUse.setState(2)
        for num in range(0, len(robotToUse.destination)):
            # Can maybe throw an if into moveByOne that checks to see if there
            # is a shelf on robot and update location
            robotToUse.moveByOne()
            robotToUse.holdingShelf.currentLocation = robotToUse.location

        print("Moving with Shelf")
        print("\nRobot is at picker Location")
        print(robotToUse.getLocation())
        robotToUse.setState(3)

        print("Shelf Location")
        print(robotToUse.holdingShelf)

        # Now that we are at the picking station, remove the item from the shelf,
        # and add it to the collected for Order (We are ignoring Bin for the moment)
        # Picker Obj?

        # Check if correct item (By Name)
        itemFromShelf = robotToUse.holdingShelf.findItem(item)
        itemFromShelf.changeShelf(None)
        # Item from shelf is put into collected
        ord1.addItem(itemFromShelf)

        # Remove item from shelf
        robotToUse.holdingShelf.removeItem(itemFromShelf)

        print("\nIn Bin:")
        print(ord1.collected)

        print("Shelf status")
        print(robotToUse.holdingShelf)

        # Now that the item is in the bin, we return the shelf back to its location
        # and then also move the robot back

        robotPath = rSched.mapDestination(robotToUse, robotToUse.holdingShelf.homeLocation)
        robotToUse.setDestination(robotPath)
        print("\nRobot has path to Shelf Home Location added")
        robotToUse.setState(4)
        print("Bringing Shelf back")
        for num in range(0, len(robotToUse.destination)):
            # Can maybe throw an if into moveByOne that checks to see if there
            # is a shelf on robot and update location
            robotToUse.moveByOne()
            robotToUse.holdingShelf.currentLocation = robotToUse.location

        print("\nRobot is at Shelf Home")
        print(robotToUse.getLocation())


        print("Shelf Location (Should match Home)")
        print(robotToUse.holdingShelf)

        print("Dropping off shelf")
        robotToUse.putDownShelf(robotToUse.holdingShelf)

        robotToUse.setState(6)
        print(robotToUse)
        print("Robot Heading to charger")

        chargerLoc = Point(0,20)

        # Recalculate the path
        robotPath = rSched.mapDestination(robotToUse, chargerLoc)
        robotToUse.setDestination(robotPath)
        print("\nRobot has path to Charger added")

        # Move there

        for num in range(0, len(robotToUse.destination)):
            # Can maybe throw an if into moveByOne that checks to see if there
            # is a shelf on robot and update location
            robotToUse.moveByOne()

        print("Now charging")
        robotToUse.setState(7)
        print(robotToUse)

    print("\nNext Item\n-----------------------------------------")



# After items are grabbed for the order, check to make sure they are correct
# and ship to the address,  / Move along belt to dock area
ord1.updateStatus("All Items are collected")
for num in range(0, len(ord1.orderitems)):
    if ord1.orderitems[num] != ord1.collected[num].getItemName():
         print("Something wrong with order")
    else:
        print("pog order completed")
        ord1.updateStatus("Completed")








# Do we start an Order here and try to fulfill it?
# Take an order and start going through the steps to fulfill it.
#def CompleteOrder(order):
 #   # Update Status
 #   order.updateStatus("In Progress")

 #   for i in order.orderitems:
 #       currentitem = i
 #       # if in stock
 #       if inv.numberInStockName(currentitem) > 0:
 #           itemlocation = currentitem.getShelf().cellLocation()  # This is messed up ignore
 #           print(itemlocation)


    #inv.numberInStockName()
    # Find the first item in the orders,
    # Ask Inventory, how many are in stock, then ask where I can find it
        # What shelf and location
    # With this info, Ask Robot Scheduler to send a robot to that location
    # Have robot pick up shelf
    # Move to location of Picker,
    # Add item to bin,
        # Check where next item would be
    # Return Shelf,
    # Repeat last 5 steps until completed












# Test Shelves
# These are now autogenerated within sArea
#shelf1 = Shelf(1, 100)
#shelf2 = Shelf(2, 200)

# Test Items
#item1 = Item('Bagpipe', 51009)
#item2 = Item('Tic-Tac', 57678)
#item3 = Item('Hydras Lament', 11008)
#item4 = Item('Socks', 13009)
#item5 = Item('Puck', 34678)
#item6 = Item('Shifters Shield', 81035)
#item7 = Item('Tic-Tac', 57678)
#item8 = Item('Singular Orange', 34231)

# Creating a few initial points that robots can be placed at
#startPoint1 = Point(1,2)
#startPoint2 = Point(7,8)
#startPoint3 = Point(4,4)
#startPoint4 = Point(6,2)

# Test Robots
#roboA= Robot('A', startPoint1)
#roboB = Robot('B', startPoint2)
#roboC= Robot('C', startPoint3)
#roboD = Robot('D', startPoint4)

# Test Locations to Path Robots to
#newLoc = Point(10, 10)
#newLoc2 = Point(0, 0)

# Add Shelves to Shelve Area
#sArea.addShelve(shelf1)
#sArea.addShelve(shelf2)

# Add Items to Inventory
#inv.addItem(item2)
#inv.addItem(item1)
#inv.addItem(item3)
#inv.addItem(item4)
#inv.addItem(item5)
#inv.addItem(item6)
#inv.addItem(item7)
#inv.addItem(item8)

# Add Robots to the Scheduler
#rSched.addRobot(roboA)
#rSched.addRobot(roboB)
#rSched.addRobot(roboC)
#rSched.addRobot(roboD)













# Placing items on to shelves
#def placeItemOnShelf():
    #for i in inv.stock:
        #nShelf = sArea.findShelfWithSpace()
        #i.changeShelf(nShelf.shelfNumber)
        #nShelf.push(i)

#placeItemOnShelf()

#print('Stock')
#print(inv.stock)

#print('Shelves')
#print(sArea.allShelves)

#print(inv.findItemSerial(81035))


#print(inv.findItemName('Puck'))









# TRYING TO THEORYCRAFT HOW WE WILL GO ABOUT GETTING THE WAREHOUSE TO FUNCTION AS ONE BEING
"""
For the time being, build the entire thing around Floor, ShelfArea, Inventory, RobotScheduler, and OrderControl
- Can get away with not implementing Belt -  Visualizer is a problem for another time

ORDER OF OPERATIONS

Phase 1: Setup
- Need to generate our Warehouse
- Create the Floor and fill it          
        - Floor - Populate()  will also create our empty shelves
- Create our Inventory and distribute the items across the warehouse (Put them on shelves)
        - Inventory - Populate 
- Create our RobotScheduler and create an area for the robots,  
        - RobotScheduler - Populate ( add these robots into cells)
                - Maybe make a RobotArea that is just used once to generate

Phase 2: Receiving Orders and Making everything communicate with each other
- Create OrderControl
    - Populate() generate a few sample orders 
    
- Filling out orders
    - Do we do this within orderControl?
    - Or is this just a massive method within Master?
            - I feel like Master is the way to go. 



"""







































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
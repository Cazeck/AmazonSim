import simpy
import random

from Floor import Floor
from SimRandom import SimRandom
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

from Bin import Bin
from Belt import Belt

from Picker import Picker
from Packer import Packer


# As of right now this is all from Masters, Need to actually complete Master as a class


# Need to Randomly distribute all of the items within stock to the
# Shelves within the ShelfAreas
def shelveStock():
    # All items in Inventory
    for item in inventory.stock:
        # Need to choose from one of the Shelf Areas
        randomsArea = random.choice(floor.shelfareas)

        # Choose a random shelf within above Shelf Area
        #randonCellContent= random.choice(randomsArea.areacontents).getContents()
        #randomShelf = randonCellContent[0]
        randomShelf = random.choice(randomsArea.areacontents).getContents()
        randomShelf.addItem(item)  # Put Item on Shelf
        item.changeShelf(randomShelf.getShelfNo())  # Tell Item which Shelf it belongs to

        # print("Adding " + str(item.getItemName()) + " to Shelf " + str(randomShelf.getShelfNo()) + " in Area " + str(randomsArea.areanumber))

# Maps the path from the robots location to the destination
# and tells the robot head there.
def robotRequest(robot, destination):
    robotlocation = robot.location

    # Calculate a path from the Robot's current location to requested
    # At some point make this so it doesn't go through Cells containing objects
    path = floor.getPath(robotlocation, destination)
    robot.setDestination(path)

    # Moving the robot to location
    # Running moveByOne multiple times to emulate ticks for time being)
    for num in range(0, len(robot.getDestination())):
        robot.moveByOne()
    # print("Robot is now at: " + str(robot.getLocation()))


def processOrder(order):
    # The bin that the items will be put on
    order_bin = Bin()
    beltArea = floor.beltAreas[0]

    # Go through each item one-by-one
    # item is just a string of an item name. Not an Item object
    for item in order.orderitems:
        print("\nGrabbing new Item -----------------------\n")
        # Check if item is in stock
        if inventory.numberInStockName(item) > 0:
            # Find our which Shelf this item can be found at
            # itemlocation = number of Shelf that it is on
            shelfnumber = inventory.findItemName(item)
            print("Item: " + item + " is located at Shelf " + str(shelfnumber))

            shelfarea = floor.locateShelf(shelfnumber)  # Ask Floor which ShelfArea it is located
            shelf = shelfarea.findShelf(shelfnumber)  # Ask the ShelfArea to find the Shelf
            shelflocation = shelf.getHomeLocation()  # Cell which the Shelf can be found

            print("Shelf " + str(shelfnumber) + " is located at " + str(shelflocation))

            # Now we need to tell Robot Scheduler to send a Robot to that Cell
            # Ask RobotScheduler for a Robot that is currently idle
            robot = robotScheduler.findAvailableRobot()
            print("\nStarting robotRequest --> Shelf")
            robot.status = 1  # pickershelfbound
            robotRequest(robot, shelflocation)

            # Now at shelf, need to pick it up and bring it to the picker's location
            print("\nPicking up Shelf")
            robot.pickUpShelf(shelf)
            print(robot.holdingShelf)

            print("\nStarting robotRequest --> Picker")
            robot.status = 2  # pickerbound
            robotRequest(robot, floor.getPickerLocation())
            robot.status = 3  # atpicker

            pickeditem = robot.getholdingShelf().findItem(item)

            print("Picker takes items off of shelf")
            picker = floor.getPicker()
            picker.pickItem(shelf, pickeditem, order, order_bin, inventory)

            print(f"\nIn Bin: {order_bin.getContents()}")


            # print("Shelf status")
            # print(robot.getholdingShelf())

            # Bring the Shelf back to its home location

            shelfhome = robot.getholdingShelf().getHomeLocation()
            robot.setState(4)  # shelfhomebound
            print("\nStarting robotRequest --> Shelf Home")
            robotRequest(robot, shelfhome)
            robot.setState(5)  # shelfhomelocation

            # Put Shelf back into place
            print("Dropping off Shelf")
            robot.putDownShelf(robot.holdingShelf)

            robot.setState(6)  # chargerbound
            print("\nStarting robotRequest --> Charger")

            # NEED TO CREATE A GET OPEN CHARGER FUNCTION HERE<
            # FOR NOW JSUT INPUT ORIGINAL LOCATION
            #robotRequest(robot, floor.getCharger())     #Get open charger?
            robotRequest(robot, floor.chargers[0].location)
            robot.setState(7)  # charging

    print("\n-------------- OUTSIDE ITEM LOOP -------------------")
    # After grabbing each Item, check if order is fulfilled
    #if order.isFilled():
    #print(order_bin.getContents())
    #print(order.collected)
    if order_bin.getContents() == order.collected:

        # Find the location of the Belt next to Picker
        firstBelt = beltArea.getBeltAt(picker.beltlocation)
        print(f'Picker Belt is: {firstBelt}')

        # Need to put the Bin onto the Belt
        picker.putOnBelt(order_bin, firstBelt)

        # Contents on Bin that is on Belt
        #print(pBelt.getContent().getContents())

        # Now we need to calculate how far picker is from packer
        packer = floor.getPacker()

        dist = packer.location.y - picker.location.y
        print(f'\nPacker is {dist} Units away from Picker')

        # Moving the belt with Bin on it to the Packer
        print("Moving Belt")
        for i in range(0, dist):
            beltArea.moveBelt()
            #print('Moved one space on belt')
            #print(f'firstBelt now at: {firstBelt.getBeltCoord()}')

        # Now we need to take the Bin off of the Belt
        # same as firstBelt. Just making sure
        packbelt = beltArea.getBeltAt(packer.getPackerBeltLocation())
        print(f'\n{packbelt} is in front of Packer')

        # Take Bin off of Belt
        binfrombelt = packbelt.getContent()
        packer.takeOffBelt(binfrombelt, packbelt)
        print(f'{binfrombelt} taken off of {packbelt}')

        # Create the package
        print('\nCreating package')
        orderpackage = packer.createPackage(binfrombelt, order.getShipAddr())
        print(f'Package is {orderpackage.contents}, ship to: {orderpackage.destination}')

        packer.putOnBelt(orderpackage, packbelt)

        # Now we need to calculate how far packer is from shipping dock
        dist2 = beltArea.endpoint.y - packer.beltlocation.y -1
        print(f'\nPacker is {dist2} Units away from Dock')

        # Moving the belt with Bin on it to the Packer
        print("Moving Belt")
        for i in range(0, dist2):
            beltArea.moveBelt()
            #print('Moved one space on belt')
            #print(f'firstBelt now at: {firstBelt.getBeltCoord()}')


        # Pretend shippingDock removes the package from Belt, and ships it
        print("\nPackage has made it to Shipping Dock")
        firstBelt.removeObject(orderpackage)
        #print(firstBelt.getContent())
        print("Item has been Shipped!")




env = simpy.Environment()
# Test Instances of Areas
floor = Floor(env)
inventory = Inventory(env)
robotScheduler = RobotScheduler(env)
orderControl = OrderControl(env)
#picker = Picker(Point(1,5), inventory)
#packer = Packer(Point(1,10))

# Place items into shelves within ShelfAreas
shelveStock()

orders_to_complete = orderControl.allOrders
order_one = orders_to_complete[0]

processOrder(order_one)

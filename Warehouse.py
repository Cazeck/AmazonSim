import simpy
import random
from Floor import Floor
from Inventory import Inventory
from OrderControl import OrderControl
from RobotScheduler import RobotScheduler

"""
Warehouse is main meme
"""

class Warehouse(object):

    def __init__(self, env):
        random.seed(2)
        self.clock = env           # SimPy environment for Event-Based Simulation
        # Create Instances of main components
        self.floor = Floor(env)
        self.inventory = Inventory(env, self.floor)
        self.robot_scheduler = RobotScheduler(env, self.floor)
        self.order_control = OrderControl(env, self.inventory)

    # Warehouse will possess all of the Simulation methods that replicate methods
    # within the warehouse components. These are for the Event-Based Simulation
    def orderCreated(self, order):
        print(f'\nTick: {self.clock.now}'
              f'\nNew order has arrived!'
              f'\n{order}')
        yield self.clock.timeout(1)

    def orderStarted(self, order):
        print(f'\nTick: {self.clock.now}'
              f'\nStarting to process order {order.orderid}'
              f'\n{order.orderitems}')
        yield self.clock.timeout(1)

    def startItem(self, item):
        print(f'\nTick: {self.clock.now}'
              f'\nStarting to grab {item}')
        yield self.clock.timeout(1)

    def itemLocationRequest(self, item):
        print(f'\nTick: {self.clock.now}'
              f'\nFinding shelf location for {item}')
        yield self.clock.timeout(1)

    def shelfLocationRequest(self, shelf):
        print(f'\nTick: {self.clock.now}'
              f'\nFinding Shelf {shelf.shelfNumber} location on Floor')
        yield self.clock.timeout(1)

    def robotPathRequest(self, robot):
        path_length = len(robot.destination)
        print(f'\nTick: {self.clock.now}'
              f'\nGenerating path for Robot {robot.robotName}'
              f'\nWill need to move {path_length} units')
        yield self.clock.timeout(1)

    def robotMovement(self, robot):
        # print(f'\nTick: {self.clock.now}\nRobot {robot.robotName} moved one unit')
        yield self.clock.timeout(1)

    def robotAtLocation(self, robot):
        print(f'\nTick: {self.clock.now}'
              f'\nRobot {robot.robotName} has arrived at destination')
        yield self.clock.timeout(1)

    def robotPickUpShelf(self, robot, shelf):
        print(f'\nTick: {self.clock.now}'
              f'\nRobot {robot.robotName} has picked up Shelf {shelf.shelfNumber}')
        yield self.clock.timeout(1)

    def robotPutDownShelf(self, robot, shelf):
        print(f'\nTick: {self.clock.now}'
              f'\nRobot {robot.robotName} has put down Shelf {shelf.shelfNumber}')
        yield self.clock.timeout(1)

    def robotAtCharger(self, robot):
        print(f'\nTick: {self.clock.now}'
              f'\nRobot {robot.robotName} has returned to charger')
        yield self.clock.timeout(1)

    def pickerGrabsItem(self, item, shelf):
        print(f'\nTick: {self.clock.now}'
              f'\nPicker takes {item} off of Shelf {shelf.shelfNumber} and places it in bin')
        yield self.clock.timeout(1)

    def pickerPutOnBelt(self, belt):
        print(f'\nTick: {self.clock.now}'
              f'\nPicker puts Bin on Belt {belt.id}')
        yield self.clock.timeout(1)

    def beltMovement(self):
        # print(f'\nTick: {self.clock.now}'
        #      f'\nBelt rotates one position')
        yield self.clock.timeout(1)

    def beltAtLocation(self, belt, item, destination):
        print(f'\nTick: {self.clock.now}'
              f'\nBelt {belt.id} with {item} is now at {destination}')
        yield self.clock.timeout(1)

    def packerTakeOffBelt(self, belt):
        print(f'\nTick: {self.clock.now}'
              f'\nPacker takes Bin off of belt {belt.id}')
        yield self.clock.timeout(1)

    def createPackage(self, package):
        print(f'\nTick: {self.clock.now}'
              f'\nPacker creates Package from Bin contents'
              f'\nPackage is to be shipped to: {package.destination}'
              f'\nContents: {package.contents}')
        yield self.clock.timeout(1)

    def shipPackage(self, package):
        print(f'\nTick: {self.clock.now}'
              f'\nPackage has been shipped to: {package.destination}')
        yield self.clock.timeout(1)


def simulation(env):
    warehouse = Warehouse(env)
    floor = warehouse.floor
    inventory = warehouse.inventory
    robot_scheduler = warehouse.robot_scheduler
    order_control = warehouse.order_control
    order_queue = order_control.allOrders

    picker = floor.getPicker()
    packer = floor.getPacker()
    belt_area = floor.beltAreas[0]
    dock_area = floor.shippingdock

    print('Warehouse is created')

    while True:
        yield env.timeout(2)
        #print(f'\nTick {env.now}')

        num_of_orders = len(order_queue)

        # If no Orders exist, make one
        if num_of_orders == 0:
            print('There are no Orders. Creating one now')
            # Generate a random Order
            order_control.genRandomOrder()
            #new_order
            #yield

        # If there are Orders in queue, start fulfilling them
        if num_of_orders > 0:
            order = order_queue[0]
            order_bin = picker.grabBin()
            order.updateStatus('Being processed')
            yield env.process(warehouse.orderStarted(order))

            # Beginning of Order fulfillment
            for item in order.orderitems:

                yield env.process(warehouse.startItem(item))

                # Check if the Item is in stock. If so, begin the Item grabbing process
                if inventory.numberInStockName(item) > 0:

                    # Finding Shelf that Item is located on
                    shelf_number = inventory.findItemName(item)
                    yield env.process(warehouse.itemLocationRequest(item))

                    # Asking Floor where this Shelf can be found at
                    shelf_area = floor.locateShelf(shelf_number)
                    shelf = shelf_area.findShelf(shelf_number)
                    shelf_location = shelf.getHomeLocation()
                    yield env.process(warehouse.shelfLocationRequest(shelf))

                    # Ask Robot Scheduler to send an inactive Robot to Shelf location
                    robot = robot_scheduler.findAvailableRobot()
                    robot.status = 1

                    # Calculate the path to Shelf
                    robot_scheduler.robotPath(robot, shelf_location)
                    path_length = len(robot.destination)
                    yield env.process(warehouse.robotPathRequest(robot))

                    # Move Robot to Shelf location
                    for num in range(0, path_length):
                        robot_scheduler.moveByOne(robot)
                        yield env.process(warehouse.robotMovement(robot))
                    yield env.process(warehouse.robotAtLocation(robot))

                    # Pick up Shelf with Robot
                    robot.pickUpShelf(shelf)
                    yield env.process(warehouse.robotPickUpShelf(robot, shelf))

                    # Calculate the path to Picker
                    picker = floor.getPicker()
                    picker_location = picker.getPickerRobotLocation()
                    robot_scheduler.robotPath(robot, picker_location)
                    path_length = len(robot.destination)
                    robot.status = 2
                    yield env.process(warehouse.robotPathRequest(robot))

                    # Move Robot to Picker location
                    robot.status = 3
                    for num in range(0, path_length):
                        robot_scheduler.moveByOne(robot)
                        yield env.process(warehouse.robotMovement(robot))
                    yield env.process(warehouse.robotAtLocation(robot))

                    # Have Picker take the Item off of the Shelf and add it to Bin
                    holding_shelf = robot.getHoldingShelf()
                    requested_item = holding_shelf.findItem(item)

                    picker.pickItem(holding_shelf, requested_item, order, order_bin, inventory)
                    yield env.process(warehouse.pickerGrabsItem(item, holding_shelf))

                    # Calculate the path to Shelf home location
                    home_location = holding_shelf.getHomeLocation()
                    robot_scheduler.robotPath(robot, home_location)
                    path_length = len(robot.destination)
                    robot.status = 4
                    yield env.process(warehouse.robotPathRequest(robot))

                    # Move Robot to Shelf home location
                    robot.status = 5
                    for num in range(0, path_length):
                        robot_scheduler.moveByOne(robot)
                        yield env.process(warehouse.robotMovement(robot))
                    yield env.process(warehouse.robotAtLocation(robot))

                    # Put down Shelf with Robot
                    robot.putDownShelf(shelf)
                    yield env.process(warehouse.robotPutDownShelf(robot, shelf))

                    # Calculate path back to charger
                    # Might need a chargerArea so that we can check which are open
                    charger_location = floor.getChargerLocation()
                    robot_scheduler.robotPath(robot, charger_location)
                    path_length = len(robot.destination)
                    robot_status = 6
                    yield env.process(warehouse.robotPathRequest(robot))

                    # Move Robot to charger location
                    for num in range(0, path_length):
                        robot_scheduler.moveByOne(robot)
                        yield env.process(warehouse.robotMovement(robot))
                    yield env.process(warehouse.robotAtLocation(robot))

                    # Robot is now charging
                    robot_status = 7
                    yield env.process(warehouse.robotAtCharger(robot))

                # Item is not in stock
                else:
                    # This shouldn't hit because we resupply when an Item gets removed
                    print("Item is not in Stock!")

            print('\n----------------------- OUTSIDE ITEM LOOP -----------------------')

            # After grabbing each Item, the order now needs to be packaged and shipped
            # If the Items in bin match the Items from the Order
            if order_bin.getContents() == order.collected:

                # Find the location of the Belt next to Picker
                first_belt = belt_area.getBeltAt(picker.getPickerBeltLocation())

                # Tell Picker to put Bin on Belt
                picker.putOnBelt(order_bin, first_belt)
                yield env.process(warehouse.pickerPutOnBelt(first_belt))

                # Distance from Picker to Packer
                picker_to_packer = packer.location.y - picker.location.y

                # Moving Belt with Bin on it to the Packer
                for num in range(0, picker_to_packer):
                    belt_area.moveBelt()
                    yield env.process(warehouse.beltMovement())
                yield env.process(warehouse.beltAtLocation(first_belt, "Bin", "Packer"))

                # Tell Packer to take Bin off of Belt
                packer.takeOffBelt(order_bin, first_belt)
                yield env.process(warehouse.packerTakeOffBelt(first_belt))

                # Tell Packer to create a Package from the contents of Bin
                order_package = packer.createPackage(order_bin, order.getShipAddr())
                yield env.process(warehouse.createPackage(order_package))

                packer_to_dock = belt_area.endpoint.y - packer.beltlocation.y - 1

                # Moving Belt with Package on it to the Shipping Dock
                for num in range(0, packer_to_dock):
                    belt_area.moveBelt()
                    yield env.process(warehouse.beltMovement())
                yield env.process(warehouse.beltAtLocation(first_belt, "Package",  "Dock Area"))

                # Take Package off of Belt and Ship it to Address
                dock_area.shipPackage(first_belt, order_package)
                yield env.process(warehouse.shipPackage(order_package))

                # Now delete Order from OrderControl
                order_control.removeOrder(order)
                print('\n----------------------- END OF ORDER -----------------------')


def run():
    env = simpy.Environment()
    env.process(simulation(env))
    env.run(until=1100)


run()
import random
import simpy

# Warehouse Components
from Floor import Floor
from Inventory import Inventory
from OrderControl import OrderControl
from RobotScheduler import RobotScheduler

import Display

# Whether or not we are going to show the Display during the Simulation
show_animation = True

class Warehouse(object):
    """
    Warehouse class is the master class for this project. Warehouse creates an instance of each of the primary
    components and allows them to communicate in order to fulfill Orders of Items that customers purchase

    Attributes:
        clock: Reference to SimPy simulation environment
        floor: Reference to the Floor component
        inventory: Reference to Inventory component
        robot_scheduler: Reference to RobotScheduler component
        order_control: Reference to OrderControl component
    """

    def __init__(self, env):
        # Seed in which the randomness of the simulation pans out
        # Change the number to see different Order schedules
        random.seed(5)
        # env is the SimPy simulation environment. It works as our world clock for this simulation
        # env is created and can be adjusted at the bottom of Warehouse.py
        self.clock = env
        # Create Instances of main components
        self.floor = Floor(env)
        self.inventory = Inventory(env, self.floor)
        self.robot_scheduler = RobotScheduler(env, self.floor)
        self.order_control = OrderControl(env, self.inventory)

    # Simulation methods for Event-Based Simulation
    # Different methods yield the clock for different amounts of time
    # to simulate the amount of time that action would take
    def orderCreated(self, order):
        """
        Simulation method used for Event-Based Simulation
        Yields the clock for 1 tick

        Args:
            self: Our instance of Warehouse
            order: Order object created within the Warehouse
        """
        print(f'\nTick: {self.clock.now}'
              f'\nNew order has arrived!'
              f'\n{order}')

        yield self.clock.timeout(1)

    def orderStarted(self, order):
        """
        Simulation method used for Event-Based Simulation
        Yields the clock for 3 ticks

        Also sends information about the Order progress to Display and
        updates status information

        Args:
            self: Our instance of Warehouse
            order: Order object which is starting to be fulfilled
        """
        print(f'\nTick: {self.clock.now}'
              f'\nStarting to process order {order.order_id}'
              f'\n{order.order_items}')

        Display.App.new_order(order)
        Display.App.update_status(f'Beginning Fulfillment')
        Display.App.ticker_update(f'\n\n\n\nTick: {self.clock.now}'
              f'\nStarting to process Order {order.order_id}\n')

        yield self.clock.timeout(3)

    def startItem(self, item):
        """
        Simulation method used for Event-Based Simulation
        Yields the clock for 4 ticks

        Also sends information about the Order progress to Display and
        updates status information

        Args:
            self: Our instance of Warehouse
            item: Item object needed in order to fulfill an Order

        """
        print(f'\nTick: {self.clock.now}'
              f'\nStarting to grab {item}')

        Display.App.update_status(f'Collecting Items')

        Display.App.ticker_update(f'\n\n\n\nTick: {self.clock.now}'
              f'\nStarting to grab {item}\n')

        yield self.clock.timeout(4)

    def itemLocationRequest(self, item):
        """
        Simulation method used for Event-Based Simulation
        Yields the clock for 4 ticks

        Also sends information about the Order progress to Display and
        updates status information

        Args:
            self: Our instance of Warehouse
            item: Item object where location is needed
        """
        print(f'\nTick: {self.clock.now}'
              f'\nFinding shelf location for {item}')

        Display.App.ticker_update(f'\n\n\n\nTick: {self.clock.now}'
              f'\nFinding shelf location for'
              f'\n{item}\n')

        yield self.clock.timeout(4)

    def shelfLocationRequest(self, shelf):
        """
        Simulation method used for Event-Based Simulation
        Yields the clock for 4 ticks

        Also sends information about the Order progress to Display and
        updates status information

        Args:
            self: Our instance of Warehouse
            shelf: Shelf object that is holding the needed Item
        """
        print(f'\nTick: {self.clock.now}'
              f'\nFinding Shelf {shelf.getShelfNo()} location on Floor')

        Display.App.ticker_update(f'\n\n\n\nTick: {self.clock.now}'
              f'\nFinding Shelf {shelf.getShelfNo()} location on Floor\n')

        yield self.clock.timeout(4)

    def robotPathRequest(self, robot):
        """
        Simulation method used for Event-Based Simulation
        Yields the clock for 4 ticks

        Also sends information about the Order progress to Display and
        updates status information

        Args:
            self: Our instance of Warehouse
            robot: Robot object needed to grab Shelf contained needed Item
        """
        path_length = len(robot.destination)
        print(f'\nTick: {self.clock.now}'
              f'\nGenerating path for Robot {robot.getName()}'
              f'\nWill need to move {path_length} units')

        Display.App.ticker_update(f'\n\n\n\nTick: {self.clock.now}'
              f'\nGenerating path for Robot {robot.getName()}\n')

        yield self.clock.timeout(4)

    def robotMovement(self, robot):
        """
        Simulation method used for Event-Based Simulation
        Yields the clock for 1 tick

        This is called for each time the Robot moves 1 unit so the Robot moves
        once per tick

        Args:
            self: Our instance of Warehouse
            robot: Robot that is moving
        """
        yield self.clock.timeout(1)

    def robotMovementUpdate(self, step, length, robot, shelf):
        """
        Simulation method used to update information for the Display ticker based on the Robot's movement

        Args:
            step: integer that is 1 - 4 depending on which step of an Order's fulfillment we are on
            length: integer representing how many more steps the Robot needs to move to destination
            robot: Robot object which is moving
            shelf: Shelf object that the Robot is carrying
        """
        # Moving to a Shelf
        if step == 1:
            Display.App.ticker_update(
                f'\n\n\nTick: {self.clock.now} - {self.clock.now + length}'
                f'\nMoving Robot {robot.getName()}'
                f'\nto Shelf {shelf.getShelfNo()}\n')

        # Moving with Shelf to Picker location
        if step == 2:
            Display.App.ticker_update(
                f'\n\n\nTick: {self.clock.now} - {self.clock.now + length}'
                f'\nMoving Robot {robot.getName()}'
                f'\nto Picker location\n')

        # Returning Shelf to Shelf home location
        if step == 3:
            Display.App.ticker_update(
                f'\n\n\nTick: {self.clock.now} - {self.clock.now + length}'
                f'\nReturning Shelf {shelf.getShelfNo()}'
                f'\nTo its home location\n')

        # Returning to charging location
        if step == 4:
            Display.App.ticker_update(
                f'\n\n\nTick: {self.clock.now} - {self.clock.now + length}'
                f'\nRobot {robot.getName()}'
                f'\nReturning to charger\n')

    def BeltMovementUpdate(self, step, length):
        """
        Simulation method used to update information for the Display ticker based on the Belt's movement

        Args:
            step: integer that is 1 - 2 depending on whether an Bin or Package is on the Belt
            length: integer representing how many more steps the Belt needs to move to destination
        """
        # Belt is moving with a Bin on it
        if step == 1:
            Display.App.ticker_update(
                f'\n\n\nTick: {self.clock.now} - {self.clock.now + length}'
                f'\nMoving Belt with Bin'
                f'\nTo Packer Location\n')

        # Belt is moving with a Package on it
        if step == 2:
            Display.App.ticker_update(
                f'\n\n\nTick: {self.clock.now} - {self.clock.now + length}'
                f'\nMoving Belt with Package'
                f'\nTo Shipping Dock\n')


    def robotAtLocation(self, robot, destination):
        """
        Simulation method used for Event-Based Simulation
        Yields the clock for 1 tick

        Args:
            self: Our instance of Warehouse
            robot: Robot object that has arrived at location
            destination: Point object which is the location arrived
        """
        print(f'\nTick: {self.clock.now}'
              f'\nRobot {robot.getName()} has arrived at {destination}')

        #Display2.App.ticker_update(f'\n\n\n\nTick: {self.clock.now}'
        #      f'\nRobot {robot.getName()} has arrived at {destination}\n')

        yield self.clock.timeout(1)

    def robotPickUpShelf(self, robot, shelf):
        """
        Simulation method used for Event-Based Simulation
        Yields the clock for 4 ticks

        Also sends information about the Order progress to Display and
        updates status information

        Args:
            self: Our instance of Warehouse
            robot: Robot object that is picking up Shelf
            shelf: Shelf object that is being picked up
        """
        print(f'\nTick: {self.clock.now}'
              f'\nRobot {robot.getName()} has picked up Shelf {shelf.getShelfNo()}')

        Display.App.ticker_update(f'\n\n\n\nTick: {self.clock.now}'
              f'\nRobot {robot.getName()} has picked up Shelf {shelf.getShelfNo()}\n')

        yield self.clock.timeout(4)

    def robotPutDownShelf(self, robot, shelf):
        """
        Simulation method used for Event-Based Simulation
        Yields the clock for 4 ticks

        Also sends information about the Order progress to Display and
        updates status information

        Args:
            self: Our instance of Warehouse
            robot: Robot object that is dropping off Shelf
            shelf: Shelf object that is being put down
        """
        print(f'\nTick: {self.clock.now}'
              f'\nRobot {robot.getName()} has put down Shelf {shelf.getShelfNo()}')

        Display.App.ticker_update(f'\n\n\n\nTick: {self.clock.now}'
              f'\nRobot {robot.getName()} has put down Shelf {shelf.getShelfNo()}\n')

        yield self.clock.timeout(4)

    def pickerGrabsItem(self, item, shelf):
        """
        Simulation method used for Event-Based Simulation
        Yields the clock for 4 ticks

        Also sends information about the Order progress to Display and
        updates status information

        Args:
            item: Item object Picker is removing from Shelf
            shelf: Shelf object containing needed Item
        """
        print(f'\nTick: {self.clock.now}'
              f'\nPicker takes {item} off of\n'
              f'Shelf {shelf.getShelfNo()} and places it in Bin')

        Display.App.update_collected(item)

        Display.App.ticker_update(f'\n\n\n\nTick: {self.clock.now}'
              f'\nPicker takes {item} off of\n'
              f'Shelf {shelf.getShelfNo()} and places it in Bin\n')

        yield self.clock.timeout(4)

    def pickerPutOnBelt(self, belt):
        """
        Simulation method used for Event-Based Simulation
        Yields the clock for 4 ticks

        Also sends information about the Order progress to Display and
        updates status information

        Args:
            belt: Belt object which Bin is being placed onto
        """
        print(f'\nTick: {self.clock.now}'
              f'\nPicker puts Bin on Belt {belt.getBeltNo()}')

        Display.App.update_status(f'All Items Collected')

        Display.App.ticker_update(f'\n\n\n\nTick: {self.clock.now}'
              f'\nPicker puts Bin on Belt {belt.getBeltNo()}\n')

        yield self.clock.timeout(4)

    def beltMovement(self):
        """
        Simulation method used for Event-Based Simulation
        Yields the clock for 2 tick

        This is called for each time the Belt moves 1 unit so the Belt moves
        once per 2 ticks
        """
        # print(f'\nTick: {self.clock.now}'
        #      f'\nBelt rotates one position')
        yield self.clock.timeout(2)

    def beltAtLocation(self, belt, item, destination):
        """
        Simulation method used for Event-Based Simulation
        Yields the clock for 3 ticks

        Also sends information about the Order progress to Display and
        updates status information

        Args:
            belt: Belt object which has arrived at destination
            item: Item object moving on the Belt
            destination: Point object of the Belt's destination location
        """
        print(f'\nTick: {self.clock.now}'
              f'\nBelt {belt.getBeltNo()} with {item} is now at {destination}')

        Display.App.ticker_update(f'\n\n\n\nTick: {self.clock.now}'
              f'\nBelt {belt.getBeltNo()} with {item} is now at {destination}\n')

        yield self.clock.timeout(3)

    def packerTakeOffBelt(self, belt):
        """
        Simulation method used for Event-Based Simulation
        Yields the clock for 4 ticks

        Also sends information about the Order progress to Display and
        updates status information

        Args:
            belt: Belt object which Bin is being taken off of
        """
        print(f'\nTick: {self.clock.now}'
              f'\nPacker takes Bin off of Belt {belt.getBeltNo()}')

        Display.App.update_status(f'Creating Package')

        Display.App.ticker_update(f'\n\n\n\nTick: {self.clock.now}'
              f'\nPacker takes Bin off of Belt {belt.getBeltNo()}\n')

        yield self.clock.timeout(4)

    def packerPutOnBelt(self, belt):
        """
        Simulation method used for Event-Based Simulation
        Yields the clock for 4 ticks

        Also sends information about the Order progress to Display and
        updates status information

        Args:
            belt: Belt object which Package is being placed onto
      """
        print(f'\nTick: {self.clock.now}'
              f'\nPacker puts Package onto Belt {belt.getBeltNo()}')

        Display.App.ticker_update(f'\n\n\n\nTick: {self.clock.now}'
              f'\nPacker puts Package onto Belt {belt.getBeltNo()}\n')

        yield self.clock.timeout(4)

    def createPackage(self, package):
        """
        Simulation method used for Event-Based Simulation
        Yields the clock for 4 ticks

        Also sends information about the Order progress to Display and
        updates status information

        Args:
            package: Package object which has been created
        """
        print(f'\nTick: {self.clock.now}'
              f'\nPacker creates package from bin contents'
              f'\nPackage is to be shipped to: {package.destination}'
              f'\nContents: {package.contents}')

        Display.App.update_status(f'Shipping Package')

        Display.App.ticker_update(f'\n\n\n\nTick: {self.clock.now}'
              f'\nPacker creates Package from Bin contents\n')

        yield self.clock.timeout(4)

    def shipPackage(self, package):
        """
        Simulation method used for Event-Based Simulation
        Yields the clock for 4 ticks

        Also sends information about the Order progress to Display and
        updates status information

        Args:
            package: Package object which has been shipped from Warehouse
        """
        print(f'\nTick: {self.clock.now}'
              f'\nPackage has been shipped to: {package.destination}')

        Display.App.ticker_update(f'\n\n\n\nTick: {self.clock.now}'
              f'\nPackage has been shipped to: {package.destination}\n')

        yield self.clock.timeout(4)


def simulation(env):
    """
    This method runs the entire Warehouse Simulation. It will continually run until the specified amount
    time (ticks) within the SimPy environment. The amount of time that is runs can be adjusted at the bottom of
    Warehouse.py

    The while loop steps through every process the Warehouse needs to do in order to fulfill orders. The progress of
    Order fulfillment are printed as text updates or outputted to the Display
    If no Order exists or all have been completed, new Orders will be randomly generated

    Args:
        env: The SimPy simulation environment
    """
    # Create an instance of our Warehouse and assign every component of Warehouse a simpler name
    warehouse = Warehouse(env)
    floor = warehouse.floor
    inventory = warehouse.inventory
    robot_scheduler = warehouse.robot_scheduler
    order_control = warehouse.order_control
    order_queue = order_control.all_orders

    picker = floor.getPicker()
    packer = floor.getPacker()
    belt_area = floor.belt_areas[0]
    dock_area = floor.shipping_dock

    # If we want the Display to run at the same time as the simulation,
    # the display is created here
    if show_animation:
        display_grid = Display.App.floor_grid
        Display.App.ticker_update(f'\nTick 0:\n'
                                   f'Warehouse is created\n')
        Display.App.update()

    print('Warehouse is created')

    while True:
        # Loop
        yield env.timeout(1)
        num_of_orders = len(order_queue)
        # If no Orders exist, make one
        if num_of_orders == 0:
            print('There are no Orders. Creating one now')
            # Generate a random Order
            order_control.genRandomOrder()

        # If there are Orders in queue, start fulfilling them
        if num_of_orders > 0:
            order = order_queue[0]
            order_bin = picker.grabBin()
            yield env.process(warehouse.orderStarted(order))

            # Beginning of Order fulfillment
            for item in order.order_items:

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

                    # If we are using Display
                    if show_animation:
                        # Choose display Shelf
                        DISPLAY_SHELF = display_grid.getDisplayShelf(shelf)

                    yield env.process(warehouse.shelfLocationRequest(shelf))

                    # Ask Robot Scheduler to send an inactive Robot to Shelf location
                    robot = robot_scheduler.findAvailableRobot()

                    # If we are using Display
                    if show_animation:
                        # Choose display Robot
                        DISPLAY_ROBOT = display_grid.getDisplayRobot(robot)

                    # Calculate the path to Shelf
                    robot_scheduler.robotPath(robot, shelf_location)
                    path = robot.destination
                    path_length = len(robot.destination)
                    yield env.process(warehouse.robotPathRequest(robot))

                    # Move Robot to Shelf location
                    if show_animation:
                        warehouse.robotMovementUpdate(1, path_length, robot, shelf)

                    for num in range(0, path_length):
                        # If we are using Display
                        if show_animation:
                            DISPLAY_ROBOT.move_robot(path[0])

                        robot_scheduler.moveByOne(robot)
                        yield env.process(warehouse.robotMovement(robot))
                    yield env.process(warehouse.robotAtLocation(robot, "Shelf location"))

                    # Pick up Shelf with Robot
                    robot.pickUpShelf(shelf)
                    yield env.process(warehouse.robotPickUpShelf(robot, shelf))

                    # Calculate the path to Picker
                    picker = floor.getPicker()
                    picker_location = picker.getPickerRobotLocation()
                    robot_scheduler.robotPath(robot, picker_location)
                    path = robot.destination
                    path_length = len(robot.destination)
                    yield env.process(warehouse.robotPathRequest(robot))

                    # Move Robot to Picker location
                    if show_animation:
                        warehouse.robotMovementUpdate(2, path_length, robot, shelf)

                    for num in range(0, path_length):
                        # If we are using Display
                        if show_animation:
                            DISPLAY_ROBOT.move_robot(path[0])
                            DISPLAY_SHELF.move_shelf(path[0])

                        robot_scheduler.moveByOne(robot)
                        yield env.process(warehouse.robotMovement(robot))
                    yield env.process(warehouse.robotAtLocation(robot, "Picker"))

                    # Have Picker take the Item off of the Shelf and add it to Bin
                    holding_shelf = robot.getHoldingShelf()
                    requested_item = holding_shelf.findItem(item)

                    picker.pickItem(holding_shelf, requested_item, order, order_bin, inventory)
                    yield env.process(warehouse.pickerGrabsItem(item, holding_shelf))

                    # Calculate the path to Shelf home location
                    home_location = holding_shelf.getHomeLocation()
                    robot_scheduler.robotPath(robot, home_location)
                    path = robot.destination
                    path_length = len(robot.destination)
                    yield env.process(warehouse.robotPathRequest(robot))

                    # Move Robot to Shelf home location
                    if show_animation:
                        warehouse.robotMovementUpdate(3, path_length, robot, shelf)

                    for num in range(0, path_length):
                        # If we are using Display
                        if show_animation:
                            DISPLAY_ROBOT.move_robot(path[0])
                            DISPLAY_SHELF.move_shelf(path[0])

                        robot_scheduler.moveByOne(robot)
                        yield env.process(warehouse.robotMovement(robot))
                    yield env.process(warehouse.robotAtLocation(robot, "Shelf home location"))

                    # Put down Shelf with Robot
                    robot.putDownShelf(shelf)
                    yield env.process(warehouse.robotPutDownShelf(robot, shelf))

                    # Calculate path back to charger
                    charger_location = floor.getChargerLocation(robot)
                    robot_scheduler.robotPath(robot, charger_location)
                    path = robot.destination
                    path_length = len(robot.destination)
                    yield env.process(warehouse.robotPathRequest(robot))

                    # Move Robot to charger location
                    if show_animation:
                        warehouse.robotMovementUpdate(4, path_length, robot, shelf)

                    for num in range(0, path_length):
                        # If we are using Display
                        if show_animation:
                            DISPLAY_ROBOT.move_robot(path[0])

                        robot_scheduler.moveByOne(robot)
                        yield env.process(warehouse.robotMovement(robot))
                    yield env.process(warehouse.robotAtLocation(robot, "Charger"))

                    # Robot is now charging
                    # robot.setCharging()

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

                # If we are using Display
                if show_animation:
                    # Create Animation Bin
                    ORDER_BIN = display_grid.grabBin(picker.getPickerBeltLocation())

                yield env.process(warehouse.pickerPutOnBelt(first_belt))

                # Distance from Picker to Packer
                picker_to_packer = -(packer.location.y - picker.location.y)

                # Moving Belt with Bin on it to the Packer
                if show_animation:
                    warehouse.BeltMovementUpdate(1, picker_to_packer)

                for num in range(0, picker_to_packer):
                    belt_area.moveBelt()
                    # If we are using Display
                    if show_animation:
                        # Bin Animation
                        ORDER_BIN.move_bin(first_belt.getBeltCoord())

                        # Belt Animation
                        display_grid.rotateBelt()

                    yield env.process(warehouse.beltMovement())
                yield env.process(warehouse.beltAtLocation(first_belt, "Bin", "Packer"))

                # Tell Packer to take Bin off of Belt
                packer.takeOffBelt(order_bin, first_belt)

                # If we are using Display
                if show_animation:
                    # Delete Bin
                    display_grid.deleteObject(ORDER_BIN)

                yield env.process(warehouse.packerTakeOffBelt(first_belt))

                # Tell Packer to create a Package from the contents of Bin
                order_package = packer.createPackage(order_bin, order.getShipAddr())

                # If we are using Display
                if show_animation:
                    # Create Animation Package
                    PACKAGE = display_grid.createPackage(packer.getPackerBeltLocation())

                yield env.process(warehouse.createPackage(order_package))

                # Put new Package onto Belt
                packer.putOnBelt(order_package, first_belt)
                yield env.process(warehouse.packerPutOnBelt(first_belt))

                packer_to_dock = packer.getPackerBeltLocation().y - belt_area.end_point.y - 1

                # Moving Belt with Package on it to the Shipping Dock
                if show_animation:
                    warehouse.BeltMovementUpdate(1, packer_to_dock)

                for num in range(0, packer_to_dock):
                    belt_area.moveBelt()

                    # If we are using Display
                    if show_animation:
                        # Package Animation
                        PACKAGE.move_package(first_belt.getBeltCoord())

                        # Belt Animation
                        display_grid.rotateBelt()

                    yield env.process(warehouse.beltMovement())
                yield env.process(warehouse.beltAtLocation(first_belt, "Package",  "Dock Area"))

                # Take Package off of Belt and Ship it to Address
                dock_area.shipPackage(first_belt, order_package)

                # If we are using Display
                if show_animation:
                    # Delete Package
                    display_grid.deleteObject(PACKAGE)

                yield env.process(warehouse.shipPackage(order_package))

                # Now delete Order from OrderControl
                order_control.removeOrder(order)

                print('\n----------------------- END OF ORDER -----------------------')

# runs the Warehouse Simulation with the SimPy environment
def run():
    #env = simpy.Environment()
    env = simpy.RealtimeEnvironment(factor=.4)      # factor= how fast the simulation runs (.4 = 40% speed)
    env.process(simulation(env))
    env.run(until=200)                              # until= amount of time that the simulation will run (200 ticks)


# If we are not showing the Display during the simulation,
# simply run the warehouse within itself
if not show_animation:
    run()

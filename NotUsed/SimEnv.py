import simpy
import random
from Floor import Floor
from Inventory import Inventory
from Point import Point
from OrderControl import OrderControl
from Order import Order
from RobotScheduler import RobotScheduler

# Environment = Clock
# Processes = (Implemented as generators)
# Events (Futures or promises)  *Things that the Components do aka OrderControl / Inv
# Resources (Shared and used by processes)  *Used by above Items, Robots


class Warehouse(object):
    # The simpy environment is our clock
    def __init__(self, env):
        self.clock = env
        self.floor = Floor(env)
        self.inventory = Inventory(env)
        self.robot_scheduler = RobotScheduler(env)
        self.order_control = OrderControl(env)


    def populateStock(self):
        for item in self.inventory.stock:
            random_sarea = random.choice(self.floor.shelfareas)

            random_shelf = random.choice(random_sarea.areacontents).getContents()
            random_shelf.addItem(item)
            item.changeShelf(random_shelf.getShelfNo())

    def robotRequest(self, robot, destination):
        robotlocation = robot.location

        # Calculate a path from the Robot's current location to requested
        # At some point make this so it doesn't go through Cells containing objects
        path = self.floor.getPath(robotlocation, destination)
        robot.setDestination(path)

        # Moving the robot to location
        # Running moveByOne multiple times to emulate ticks for time being)
        #print(f'Robot needs to move {len(path)} steps')
        for num in range(0, len(robot.getDestination())):
            robot.moveByOne()
        # print("Robot is now at: " + str(robot.getLocation()))

    # Sim Function
    def getItem(self, item):
        print("\nGrabbing Item: ", item, " at tick ", self.clock.now)
        yield self.clock.timeout(2)

    def findItemNameSim(self, item):
        print("Finding", item, "location at tick", self.clock.now)
        yield self.clock.timeout(1)

    def findShelfLocationSim(self, shelf):
        print(f'Finding {shelf} location at tick {self.clock.now}')
        yield self.clock.timeout(1)

    def robotRequestSim(self, robot, destination):
        path = self.floor.getPath(robot.location, destination)
        num_of_steps = len(path)
        print(f'Robot starts moving to location at tick {self.clock.now}')
        print(f'Robot needs to move {len(path)} steps')
        for num in range(0, len(path)):
            yield env.process(self.robotMoveSim(robot, path[num]))
        print(f'Robot is now at {destination}')
        yield self.clock.timeout(1)

    def robotMoveSim(self, robot, nextStep):
        #print(f'Robot moving to {nextStep} at tick {self.clock.now}')
        yield self.clock.timeout(1)

    def robotPickUpSim(self, robot, shelf):
        print(f'Robot picking up {shelf} at tick {self.clock.now}')
        yield self.clock.timeout(1)

    def robotPutDownSim(self, robot, shelf):
        print(f'Robot putting down {shelf} at tick {self.clock.now}')
        yield self.clock.timeout(1)

    def pickerTakeItemSim(self, item, shelf):
        print(f'Picker takes {item} off of shelf {shelf.shelfNumber} at tick {self.clock.now}')
        yield self.clock.timeout(2)


# order interval is how often orders come in
def setup(env):
    warehouse = Warehouse(env)
    # Put items on Shelves (instant)
    warehouse.populateStock()

    order_to_complete = warehouse.order_control.allOrders
    order_one = order_to_complete[0]
    print("Order One is:\n", order_one)

    while True:
        yield env.timeout(1)
        print("\n------ Tick ", env.now, " ----------")
        for item in order_one.orderitems:

            # Check if the Item is in stock (One Tick?)
            if warehouse.inventory.numberInStockName(item) > 0:

                print("\n Trying to grab new item ", item)
                shelfnumber = warehouse.inventory.findItemName(item)
                yield env.process(warehouse.findItemNameSim(item))
                print(f"Item: {item} is located at Shelf {shelfnumber}")


                print(f"\nAsking Floor where Shelf {shelfnumber} is located" )
                shelfarea = warehouse.floor.locateShelf(shelfnumber)
                shelf = shelfarea.findShelf(shelfnumber)
                shelflocation = shelf.getHomeLocation()
                yield env.process(warehouse.findItemNameSim(item))
                print(f'Shelf {shelfnumber} is located at {shelflocation}')



                print('\nRequesting Robot to go to Shelf Location')
                robot = warehouse.robot_scheduler.findAvailableRobot()
                robot.status = 1
                yield env.process(warehouse.robotRequestSim(robot, shelflocation))  # At some point these should
                warehouse.robotRequest(robot, shelflocation)                        # be going simultaneously
                print('\nRobot is at Shelf location')




                print('Picking up Shelf')
                robot.pickUpShelf(shelf)
                yield env.process(warehouse.robotPickUpSim(robot, shelf))

                print('\nRequesting Robot to go to Picker Location')
                robot.status = 2
                pickerlocation = warehouse.floor.getPicker()
                yield env.process(warehouse.robotRequestSim(robot, pickerlocation))  # At some point these should
                warehouse.robotRequest(robot, pickerlocation)  # be going simultaneously
                robot.status = 3
                print('\nRobot is at Picker location')

                # Take item off of Shelf and add to Collected
                pickeditem = robot.getholdingShelf().findItem(item)
                # Remove from Inventory
                warehouse.inventory.removeItem(pickeditem)
                # Take off of Shelf
                pickeditem.changeShelf(None)
                # Put Item in Bin
                order_one.addItem(pickeditem)
                yield env.process(warehouse.pickerTakeItemSim(pickeditem, shelf))
                print(f'In Bin: {order_one.collected}')

                shelfhome = robot.getholdingShelf().getHomeLocation()
                robot.setState(4)
                print(f'\nTaking Shelf {shelf.shelfNumber} back to home location {shelfhome}')

                yield env.process(warehouse.robotRequestSim(robot, shelfhome))  # At some point these should
                warehouse.robotRequest(robot, shelfhome)  # be going simultaneously
                robot.setState(5)
                print('\nRobot is at Shelf Home location')

                # Put Shelf back into place
                print("Dropping off Shelf")
                robot.putDownShelf(robot.holdingShelf)
                yield env.process(warehouse.robotPutDownSim(robot, shelf))

                robot.setState(6)

                print('\nSending Robot to Charger now')
                yield env.process(warehouse.robotRequestSim(robot, warehouse.floor.getCharger()))
                warehouse.robotRequest(robot, warehouse.floor.getCharger())

                print('\nRobot now charging')


                robot.setState(7)


















                # run the process as normal, but make an event for each happening

                #yield env.process(warehouse.getItem(item))


        #print("Warehouse Time before getItem", env.now)
        #yield env.process(warehouse.getItem(env, order_one.orderitems[0]))
        #print("Warehouse Time after getItem", env.now)




env = simpy.Environment()
env.process(setup(env))
env.run(until=700)
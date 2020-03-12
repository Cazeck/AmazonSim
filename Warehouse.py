import random
import simpy
import numpy as np # a maths and plotting module
import matplotlib.pyplot as plt
import math
import time
import tkinter as tk

# Warehouse Components
from Point import Point
from Floor import Floor
from Inventory import Inventory
from OrderControl import OrderControl
from RobotScheduler import RobotScheduler

# Setup animation #
show_animation = True

"""
Warehouse is main meme
"""

class Warehouse(object):

    def __init__(self, env):
        random.seed(3)
        self.clock = env
        # Create Instances of main components
        self.floor = Floor(env)
        self.inventory = Inventory(env, self.floor)
        self.robot_scheduler = RobotScheduler(env, self.floor)
        self.order_control = OrderControl(env, self.inventory)

    # Simulation methods for Event-Based Simulation
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

    def robotAtLocation(self, robot, destination):
        print(f'\nTick: {self.clock.now}'
              f'\nRobot {robot.robotName} has arrived at {destination}')
        yield self.clock.timeout(1)

    def robotPickUpShelf(self, robot, shelf):
        print(f'\nTick: {self.clock.now}'
              f'\nRobot {robot.robotName} has picked up Shelf {shelf.shelfNumber}')
        yield self.clock.timeout(1)

    def robotPutDownShelf(self, robot, shelf):
        print(f'\nTick: {self.clock.now}'
              f'\nRobot {robot.robotName} has put down Shelf {shelf.shelfNumber}')
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
        yield self.clock.timeout(2)

    def beltAtLocation(self, belt, item, destination):
        print(f'\nTick: {self.clock.now}'
              f'\nBelt {belt.id} with {item} is now at {destination}')
        yield self.clock.timeout(1)

    def packerTakeOffBelt(self, belt):
        print(f'\nTick: {self.clock.now}'
              f'\nPacker takes Bin off of belt {belt.id}')
        yield self.clock.timeout(1)

    def packerPutOnBelt(self, belt):
        print(f'\nTick: {self.clock.now}'
              f'\nPacker puts Package onto belt {belt.id}')
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


# ANIMATION CLASSES
class Display_Picker:
    def __init__(self, canvas, point, unit_size, name):
        self.point = point
        self.unit_size = unit_size
        self.name = name
        self.x1 = point.x * unit_size
        self.y1 = point.y * unit_size
        self.x2 = self.x1 + unit_size
        self.y2 = self.y1 + unit_size
        self.canvas = canvas
        self.picker = canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="light blue", tags=name)
        self.picker_id = canvas.create_text(((self.x2 - self.x1) / 2 + self.x1),
                                           ((self.y2 - self.y1) / 2 + self.y1), text=name)
        self.canvas.update()

class Display_Bin:
    def __init__(self, canvas, point, unit_size, name):
        self.point = point
        self.unit_size = unit_size
        self.name = name
        self.x1 = point.x * unit_size
        self.y1 = point.y * unit_size
        self.x2 = self.x1 + unit_size
        self.y2 = self.y1 + unit_size
        self.canvas = canvas
        self.bin = canvas.create_rectangle(self.x1 + (self.unit_size * .20), self.y1 + (self.unit_size * .25),
                                           self.x2 - (self.unit_size * .20), self.y2 - (self.unit_size * .25),
                                           fill="gold", tags=name)
        self.id = canvas.create_text(((self.x2 - self.x1) / 2 + self.x1),
                                           ((self.y2 - self.y1) / 2 + self.y1), text=name)
        self.canvas.update()

    def move_bin(self, point):
        # Move Up
        if self.point.x == point.x and self.point.y > point.y:
            self.canvas.move(self.bin, 0, (point.y - self.point.y) * self.unit_size)
            self.canvas.move(self.id, 0, (point.y - self.point.y) * self.unit_size)
            next_point = Point(self.point.x, self.point.y - 1)
            self.point = next_point

        self.canvas.update

class Display_Packer:
    def __init__(self, canvas, point, unit_size, name):
        self.point = point
        self.unit_size = unit_size
        self.name = name
        self.x1 = point.x * unit_size
        self.y1 = point.y * unit_size
        self.x2 = self.x1 + unit_size
        self.y2 = self.y1 + unit_size
        self.canvas = canvas
        self.packer = canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="light green", tags=name)
        self.packer_id = canvas.create_text(((self.x2 - self.x1) / 2 + self.x1),
                                           ((self.y2 - self.y1) / 2 + self.y1), text=name)
        self.canvas.update()



class Display_Package:
    def __init__(self, canvas, point, unit_size, name):
        self.point = point
        self.unit_size = unit_size
        self.name = name
        self.x1 = point.x * unit_size
        self.y1 = point.y * unit_size
        self.x2 = self.x1 + unit_size
        self.y2 = self.y1 + unit_size
        self.canvas = canvas
        self.package = canvas.create_rectangle(self.x1 + (self.unit_size * .25), self.y1 + (self.unit_size * .20),
                                               self.x2 - (self.unit_size * .25), self.y2 - (self.unit_size * .20),
                                               fill="tan", tags=name)
        self.id = canvas.create_text(((self.x2 - self.x1) / 2 + self.x1),
                                           ((self.y2 - self.y1) / 2 + self.y1), text=name)
        self.canvas.update()

    def move_package(self, point):
        # Move Up
        if self.point.x == point.x and self.point.y > point.y:
            self.canvas.move(self.package, 0, (point.y - self.point.y) * self.unit_size)
            self.canvas.move(self.id, 0, (point.y - self.point.y) * self.unit_size)
            next_point = Point(self.point.x, self.point.y - 1)
            self.point = next_point

        self.canvas.update()

class Display_Dock:
    def __init__(self, canvas, point, unit_size, name):
        self.point = point
        self.x1 = point.x * unit_size
        self.y1 = point.y * unit_size
        self.x2 = self.x1 + unit_size
        self.y2 = self.y1 + unit_size
        self.canvas = canvas
        self.robot = canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="slategray3", tags=name)
        self.robot_id = canvas.create_text(((self.x2 - self.x1) / 2 + self.x1),
                                           ((self.y2 - self.y1) / 2 + self.y1), text=name)
        self.canvas.update()

class Display_Charger:
    def __init__(self, canvas, point, unit_size, name):
        self.point = point
        self.unit_size = unit_size
        self.name = name
        self.x1 = point.x * unit_size
        self.y1 = point.y * unit_size
        self.x2 = self.x1 + unit_size
        self.y2 = self.y1 + unit_size
        self.canvas = canvas
        self.charger = canvas.create_oval(self.x1 + (self.unit_size * .15), self.y1 + (self.unit_size * .15),
                                        self.x2 - (self.unit_size * .15), self.y2 - (self.unit_size * .15),
                                        fill="pink", tags=name)
        self.charger_id = canvas.create_text(((self.x2 - self.x1) / 2 + self.x1),
                                           ((self.y2 - self.y1) / 2 + self.y1), text=name)
        self.canvas.update()

class Display_Robot:
    def __init__(self, canvas, point, unit_size,  name):
        self.point = point
        self.unit_size = unit_size
        self.name = name
        self.x1 = point.x * unit_size
        self.y1 = point.y * unit_size
        self.x2 = self.x1 + unit_size
        self.y2 = self.y1 + unit_size
        self.canvas = canvas
        self.robot = canvas.create_rectangle(self.x1 + (self.unit_size * .05), self.y1 + (self.unit_size * .05),
                                             self.x2 - (self.unit_size * .05), self.y2 - (self.unit_size * .05),
                                             fill="orange", tags=name)
        self.robot_id = canvas.create_text(((self.x2 - self.x1) / 2 + self.x1),
                                          ((self.y2 - self.y1) / 2 + self.y1), text=name)
        self.canvas.update()

    def move_robot(self, point):
        #print(f'Moving from {self.point.x, self.point.y} to: {point.x, point.y}')

        # Move Left
        if self.point.x > point.x and self.point.y == point.y:
            self.canvas.move(self.robot, (point.x - self.point.x) * self.unit_size, 0)
            self.canvas.move(self.robot_id, (point.x - self.point.x) * self.unit_size, 0)
            # print(f'Move Left {(point.x - self.point.x) * unit_size} Units')
            next_point = Point(self.point.x - 1, self.point.y)
            self.point = next_point

        # Move Right
        if self.point.x < point.x and self.point.y == point.y:
            self.canvas.move(self.robot, (point.x - self.point.x) * self.unit_size, 0)
            self.canvas.move(self.robot_id, (point.x - self.point.x) * self.unit_size, 0)
            #print(f'Move Right {(point.x - self.point.x) * unit_size} Units')
            next_point = Point(self.point.x + 1, self.point.y)
            self.point = next_point

        # Move Up
        if self.point.x == point.x and self.point.y > point.y:
            self.canvas.move(self.robot, 0, (point.y - self.point.y) * self.unit_size)
            self.canvas.move(self.robot_id, 0, (point.y - self.point.y) * self.unit_size)
            # print(f'Move Up {(point.y - self.point.y) * unit_size} Units')
            next_point = Point(self.point.x, self.point.y - 1)
            self.point = next_point

        # Move Down
        if self.point.x == point.x and self.point.y < point.y:
            self.canvas.move(self.robot, 0, (point.y - self.point.y) * self.unit_size)
            self.canvas.move(self.robot_id, 0, (point.y - self.point.y) * self.unit_size)
            # print(f'Move Down {(point.y - self.point.y) * unit_size} Units')
            next_point = Point(self.point.x, self.point.y + 1)
            self.point = next_point

        self.canvas.update()


class Display_Belt:
    def __init__(self, canvas, point, unit_size,  name):
        self.point = point
        self.unit_size = unit_size
        self.name = name
        self.x1 = point.x * unit_size
        self.y1 = point.y * unit_size
        self.x2 = self.x1 + unit_size
        self.y2 = self.y1 + unit_size
        self.canvas = canvas
        self.belt = canvas.create_rectangle(self.x1 + (self.unit_size * .15), self.y1,
                                             self.x2 - (self.unit_size * .15), self.y2, fill="light gray", tags=name)
        self.belt_id = canvas.create_text(((self.x2 - self.x1) / 2 + self.x1),
                                          ((self.y2 - self.y1) / 2 + self.y1), text=name)
        self.canvas.update()

    def move_belt(self, point):
        #print(f'Moving from {self.point.x, self.point.y} to: {point.x, point.y}')

        # Move Up
        if self.point.x == point.x and self.point.y > point.y:
            #print("Gotta move up kurwa")
            self.canvas.move(self.belt, 0, (point.y - self.point.y) * self.unit_size)
            self.canvas.move(self.belt_id, 0, (point.y - self.point.y) * self.unit_size)
            # print(f'Move Up {(point.y - self.point.y) * unit_size} Units')
            next_point = Point(self.point.x, self.point.y - 1)
            self.point = next_point

        # Move Down to bottom location
        if self.point.x == point.x and self.point.y < point.y:
            #print("Gotta move to the bottoem luls")
            self.canvas.move(self.belt, 0, (point.y - self.point.y) * self.unit_size)
            self.canvas.move(self.belt_id, 0, (point.y - self.point.y) * self.unit_size)

            # First Belt is 5 away so lets just jump next to picker
            next_point = Point(self.point.x, self.point.y + 5)
            self.point = next_point

        self.canvas.update()


class Display_Shelf:
    def __init__(self, canvas, point, unit_size, name, number):
        self.point = point
        self.unit_size = unit_size
        self.name = name
        self.number = number
        self.x1 = point.x * unit_size
        self.y1 = point.y * unit_size
        self.x2 = self.x1 + unit_size
        self.y2 = self.y1 + unit_size
        self.canvas = canvas
        self.shelf = canvas.create_rectangle(self.x1 + (self.unit_size * .12), self.y1 + (self.unit_size * .12),
                                             self.x2 - (self.unit_size * .12), self.y2 - (self.unit_size * .12),
                                             fill="yellow", tags=name)
        self.shelf_id = canvas.create_text(((self.x2 - self.x1) / 2 + self.x1),
                                          ((self.y2 - self.y1) / 2 + self.y1), text=name)
        self.canvas.update()

    def move_shelf(self, point):
        #print(f'Moving from {self.point.x, self.point.y} to: {point.x, point.y}')

        # Move Left
        if self.point.x > point.x and self.point.y == point.y:
            self.canvas.move(self.shelf, (point.x - self.point.x) * self.unit_size, 0)
            self.canvas.move(self.shelf_id, (point.x - self.point.x) * self.unit_size, 0)
            # print(f'Move Left {(point.x - self.point.x) * unit_size} Units')
            next_point = Point(self.point.x - 1, self.point.y)
            self.point = next_point

        # Move Right
        if self.point.x < point.x and self.point.y == point.y:
            self.canvas.move(self.shelf, (point.x - self.point.x) * self.unit_size, 0)
            self.canvas.move(self.shelf_id, (point.x - self.point.x) * self.unit_size, 0)
            #print(f'Move Right {(point.x - self.point.x) * unit_size} Units')
            next_point = Point(self.point.x + 1, self.point.y)
            self.point = next_point

        # Move Up
        if self.point.x == point.x and self.point.y > point.y:
            self.canvas.move(self.shelf, 0, (point.y - self.point.y) * self.unit_size)
            self.canvas.move(self.shelf_id, 0, (point.y - self.point.y) * self.unit_size)
            # print(f'Move Up {(point.y - self.point.y) * unit_size} Units')
            next_point = Point(self.point.x, self.point.y - 1)
            self.point = next_point

        # Move Down
        if self.point.x == point.x and self.point.y < point.y:
            self.canvas.move(self.shelf, 0, (point.y - self.point.y) * self.unit_size)
            self.canvas.move(self.shelf_id, 0, (point.y - self.point.y) * self.unit_size)
            # print(f'Move Down {(point.y - self.point.y) * unit_size} Units')
            next_point = Point(self.point.x, self.point.y + 1)
            self.point = next_point

        self.canvas.update()


# Setup Canvas
if show_animation:
    master = tk.Tk()

    HEIGHT = 700
    WIDTH = 600

    # For Grid Canvas
    GRID_WIDTH = 400
    GRID_HEIGHT = 400
    UNIT_SIZE = 40

    main_canvas = tk.Canvas(master, width=WIDTH, height=HEIGHT)

    lower_frame = tk.Frame(master, bg="#80c1ff", bd=5)
    lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

    grid = tk.Canvas(lower_frame, width=GRID_WIDTH, height=GRID_HEIGHT)

    master.title("Amazon Warehouse")
    grid.pack()
    main_canvas.pack()

# Animation Methods

# Create the Grid layout for our display
def checkered(canvas, line_distance):
    # Vertical lines at an interval of "line_distance" pixel
    for x in range(line_distance, GRID_WIDTH, line_distance):
        canvas.create_line(x, 0, x, GRID_HEIGHT, fill="#476042")

    # Horizontal lines at an interval of "line_distance" pixel
    for y in range(line_distance, GRID_HEIGHT, line_distance):
        canvas.create_line(0, y, GRID_WIDTH, y, fill="#476042")


def getDisplayRobot(robot_object):
    #display_bot = None
    for bot in ROBOT_LIST:
        if bot.name == robot_object.robotName:
            display_bot = bot

    return display_bot


def getDisplayShelf(shelf_object):
    #display_shelf = None
    for shelf in SHELF_LIST:
        if shelf.number == shelf_object.shelfNumber:
            display_shelf = shelf

    return display_shelf


def rotateBelt():
    belt_length = len(BELT_LIST)
    #print(f'Len {belt_length}')
    count = 0
    for belt in BELT_LIST:
        if count == belt_length - 1:
            belt.move_belt(Point(belt.point.x, belt.point.y + belt_length - 1))

        else:
            # should move up one
            belt.move_belt(Point(belt.point.x, belt.point.y - 1))

        count += 1

    # Need to Sort belts by y (Highest first)
    BELT_LIST.sort(key=lambda belt: -belt.point.y)


def grabBin(point):
    NEW_BIN = Display_Bin(grid, point, UNIT_SIZE, 'Bin')
    return NEW_BIN


def createPackage(point):
    NEW_PACKAGE = Display_Package(grid, point, UNIT_SIZE, 'Pkg')
    return NEW_PACKAGE


def deleteObject(display_object):
    grid.delete(display_object.name)
    grid.delete(display_object.id)
    grid.update()


# Setup Warehouse
if show_animation:
    # Warehouse Grid
    checkered(grid, UNIT_SIZE)

    # Picker
    PICKER = Display_Picker(grid, Point(1, 7), UNIT_SIZE, 'Picker')

    # Packer
    PACKER = Display_Packer(grid, Point(1, 4), UNIT_SIZE, 'Packer')

    # Dock Area
    DOCK = Display_Dock(grid, Point(0, 0), UNIT_SIZE * 2, 'Dock')

    # Chargers
    CHARGER_1 = Display_Charger(grid, Point(2, 9), UNIT_SIZE, 'C1')
    CHARGER_2 = Display_Charger(grid, Point(3, 9), UNIT_SIZE, 'C2')
    CHARGER_3 = Display_Charger(grid, Point(4, 9), UNIT_SIZE, 'C3')
    CHARGER_4 = Display_Charger(grid, Point(5, 9), UNIT_SIZE, 'C4')
    CHARGER_5 = Display_Charger(grid, Point(6, 9), UNIT_SIZE, 'C5')

    # Robots

    ROBOT_1 = Display_Robot(grid, Point(2, 9), UNIT_SIZE, 'A')
    ROBOT_2 = Display_Robot(grid, Point(3, 9), UNIT_SIZE, 'B')
    ROBOT_3 = Display_Robot(grid, Point(4, 9), UNIT_SIZE, 'C')
    ROBOT_4 = Display_Robot(grid, Point(5, 9), UNIT_SIZE, 'D')
    ROBOT_5 = Display_Robot(grid, Point(6, 9), UNIT_SIZE, 'E')
    ROBOT_LIST = [ROBOT_1, ROBOT_2, ROBOT_3, ROBOT_4, ROBOT_5]

    # Belt
    BELT_1 = Display_Belt(grid, Point(0, 7), UNIT_SIZE, 'B1')
    BELT_2 = Display_Belt(grid, Point(0, 6), UNIT_SIZE, 'B2')
    BELT_3 = Display_Belt(grid, Point(0, 5), UNIT_SIZE, 'B3')
    BELT_4 = Display_Belt(grid, Point(0, 4), UNIT_SIZE, 'B4')
    BELT_5 = Display_Belt(grid, Point(0, 3), UNIT_SIZE, 'B5')
    BELT_6 = Display_Belt(grid, Point(0, 2), UNIT_SIZE, 'B6')
    BELT_LIST = [BELT_1, BELT_2, BELT_3, BELT_4, BELT_5, BELT_6]

    # Shelves
    SHELF_1 = Display_Shelf(grid, Point(5, 1), UNIT_SIZE, 'S1', 1)
    SHELF_2 = Display_Shelf(grid, Point(6, 1), UNIT_SIZE, 'S2', 2)
    SHELF_3 = Display_Shelf(grid, Point(7, 1), UNIT_SIZE, 'S3', 3)
    SHELF_4 = Display_Shelf(grid, Point(8, 1), UNIT_SIZE, 'S4', 4)
    SHELF_5 = Display_Shelf(grid, Point(9, 1), UNIT_SIZE, 'S5', 5)

    SHELF_6 = Display_Shelf(grid, Point(5, 2), UNIT_SIZE, 'S6', 6)
    SHELF_7 = Display_Shelf(grid, Point(6, 2), UNIT_SIZE, 'S7', 7)
    SHELF_8 = Display_Shelf(grid, Point(7, 2), UNIT_SIZE, 'S8', 8)
    SHELF_9 = Display_Shelf(grid, Point(8, 2), UNIT_SIZE, 'S9', 9)
    SHELF_10 = Display_Shelf(grid, Point(9, 2), UNIT_SIZE, 'S10', 10)

    SHELF_11 = Display_Shelf(grid, Point(5, 5), UNIT_SIZE, 'S11', 11)
    SHELF_12 = Display_Shelf(grid, Point(6, 5), UNIT_SIZE, 'S12', 12)
    SHELF_13 = Display_Shelf(grid, Point(7, 5), UNIT_SIZE, 'S13', 13)
    SHELF_14 = Display_Shelf(grid, Point(8, 5), UNIT_SIZE, 'S14', 14)
    SHELF_15 = Display_Shelf(grid, Point(9, 5), UNIT_SIZE, 'S15', 15)

    SHELF_16 = Display_Shelf(grid, Point(5, 6), UNIT_SIZE, 'S16', 16)
    SHELF_17 = Display_Shelf(grid, Point(6, 6), UNIT_SIZE, 'S17', 17)
    SHELF_18 = Display_Shelf(grid, Point(7, 6), UNIT_SIZE, 'S18', 18)
    SHELF_19 = Display_Shelf(grid, Point(8, 6), UNIT_SIZE, 'S19', 19)
    SHELF_20 = Display_Shelf(grid, Point(9, 6), UNIT_SIZE, 'S20', 20)
    SHELF_LIST = [SHELF_1, SHELF_2, SHELF_3, SHELF_4, SHELF_5,
                  SHELF_6, SHELF_7, SHELF_8, SHELF_9, SHELF_10,
                  SHELF_11, SHELF_12, SHELF_13, SHELF_14, SHELF_15,
                  SHELF_16, SHELF_17, SHELF_18, SHELF_19, SHELF_20]



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
                    DISPLAY_SHELF = getDisplayShelf(shelf)
                    yield env.process(warehouse.shelfLocationRequest(shelf))

                    # Ask Robot Scheduler to send an inactive Robot to Shelf location
                    robot = robot_scheduler.findAvailableRobot()

                    # Choose display Robot
                    DISPLAY_ROBOT = getDisplayRobot(robot)

                    robot.status = 1

                    # Calculate the path to Shelf
                    robot_scheduler.robotPath(robot, shelf_location)
                    path = robot.destination
                    path_length = len(robot.destination)
                    yield env.process(warehouse.robotPathRequest(robot))

                    # Move Robot to Shelf location
                    for num in range(0, path_length):
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
                    robot.status = 2
                    yield env.process(warehouse.robotPathRequest(robot))

                    # Move Robot to Picker location
                    robot.status = 3
                    for num in range(0, path_length):
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
                    robot.status = 4
                    yield env.process(warehouse.robotPathRequest(robot))

                    # Move Robot to Shelf home location
                    robot.status = 5
                    for num in range(0, path_length):
                        DISPLAY_ROBOT.move_robot(path[0])
                        DISPLAY_SHELF.move_shelf(path[0])
                        robot_scheduler.moveByOne(robot)
                        yield env.process(warehouse.robotMovement(robot))
                    yield env.process(warehouse.robotAtLocation(robot, "Shelf home location"))

                    # Put down Shelf with Robot
                    robot.putDownShelf(shelf)
                    yield env.process(warehouse.robotPutDownShelf(robot, shelf))

                    # Calculate path back to charger
                    # Might need a chargerArea so that we can check which are open
                    charger_location = floor.getChargerLocation()
                    robot_scheduler.robotPath(robot, charger_location)
                    path = robot.destination
                    path_length = len(robot.destination)
                    robot_status = 6
                    yield env.process(warehouse.robotPathRequest(robot))

                    # Move Robot to charger location
                    for num in range(0, path_length):
                        DISPLAY_ROBOT.move_robot(path[0])
                        robot_scheduler.moveByOne(robot)
                        yield env.process(warehouse.robotMovement(robot))
                    yield env.process(warehouse.robotAtLocation(robot, "Charger"))

                    # Robot is now charging
                    robot_status = 7

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
                # Create Animation Bin
                ORDER_BIN = grabBin(picker.beltlocation)
                yield env.process(warehouse.pickerPutOnBelt(first_belt))

                # Distance from Picker to Packer
                picker_to_packer = -(packer.location.y - picker.location.y)

                # Moving Belt with Bin on it to the Packer
                for num in range(0, picker_to_packer):
                    belt_area.moveBelt()
                    # Bin Animation
                    ORDER_BIN.move_bin(first_belt.getBeltCoord())
                    # Belt Animation
                    rotateBelt()
                    yield env.process(warehouse.beltMovement())
                yield env.process(warehouse.beltAtLocation(first_belt, "Bin", "Packer"))

                # Tell Packer to take Bin off of Belt
                packer.takeOffBelt(order_bin, first_belt)
                # Delete Bin
                deleteObject(ORDER_BIN)
                yield env.process(warehouse.packerTakeOffBelt(first_belt))

                # Tell Packer to create a Package from the contents of Bin
                order_package = packer.createPackage(order_bin, order.getShipAddr())
                # Create Animation Package
                PACKAGE = createPackage(packer.beltlocation)
                yield env.process(warehouse.createPackage(order_package))

                # Put new Package onto Belt
                packer.putOnBelt(order_package, first_belt)
                yield env.process(warehouse.packerPutOnBelt(first_belt))

                packer_to_dock = packer.beltlocation.y - belt_area.endpoint.y - 1

                # Moving Belt with Package on it to the Shipping Dock
                for num in range(0, packer_to_dock):
                    belt_area.moveBelt()
                    # Package Animation
                    PACKAGE.move_package(first_belt.getBeltCoord())
                    # Belt Animation
                    rotateBelt()
                    yield env.process(warehouse.beltMovement())
                yield env.process(warehouse.beltAtLocation(first_belt, "Package",  "Dock Area"))

                # Take Package off of Belt and Ship it to Address
                dock_area.shipPackage(first_belt, order_package)
                # Delete Package
                deleteObject(PACKAGE)
                yield env.process(warehouse.shipPackage(order_package))

                # Now delete Order from OrderControl
                order_control.removeOrder(order)

                print('\n----------------------- END OF ORDER -----------------------')


def run():
    env = simpy.RealtimeEnvironment(factor=.25)
    env.process(simulation(env))
    env.run(until=119)


run()

master.mainloop()

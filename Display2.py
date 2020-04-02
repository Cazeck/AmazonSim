import tkinter as tk
import Warehouse2
from Point import Point

class Application(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title('Amazon Warehouse Simulation')
        # Width & Height of Entire Display
        master.geometry("1000x530")
        master.config(background='LightSkyBlue4')
        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Create Grid
        # FLOOR GRID
        self.floor_grid = FloorGrid(master=root, width=500, height=500)
        self.floor_grid.grid(row=0, column=0, rowspan=30, padx=10, pady=10)

        # Tick Counter
        self.tick_text = tk.StringVar()
        self.tick_label = tk.Label(self.master, text='Current Tick:', font=('Courier', 10),
                                   bg='LightSkyBlue4', fg='white')
        self.tick_label.grid(row=0, column=1, sticky=tk.W)
        self.tick_value = tk.Label(self.master, textvariable=self.tick_text, font=('Courier', 10),
                                   bg='LightSkyBlue4', fg='white')
        self.tick_value.grid(row=0, column=2, sticky=tk.W)
        self.tick_text.set('100')

        # Customer
        self.customer_text = tk.StringVar()
        self.customer_label = tk.Label(self.master, text='Customer', font=('Courier', 10),
                                       bg='LightSkyBlue4', fg='white')
        self.customer_label.grid(row=1, column=1, sticky=tk.W)
        self.customer_entry = tk.Entry(self.master, textvariable=self.customer_text, width=40,
                                       bg='LightSkyBlue4', fg='white')
        self.customer_entry.grid(row=1, column=2, columnspan=3)

        # Retailer
        self.retailer_text = tk.StringVar()
        self.retailer_label = tk.Label(self.master, text='Retailer', font=('Courier', 10),
                                       bg='LightSkyBlue4', fg='white')
        self.retailer_label.grid(row=2, column=1, sticky=tk.W)
        self.retailer_entry = tk.Entry(self.master, textvariable=self.retailer_text, width=40,
                                       bg='LightSkyBlue4', fg='white')
        self.retailer_entry.grid(row=2, column=2, columnspan=3)

        # Price
        self.price_text = tk.StringVar()
        self.price_label = tk.Label(self.master, text='Price', font=('Courier', 10),
                                    bg='LightSkyBlue4', fg='white')
        self.price_label.grid(row=3, column=1, sticky=tk.W)
        self.price_entry = tk.Entry(self.master, textvariable=self.price_text, width=40,
                                    bg='LightSkyBlue4', fg='white')
        self.price_entry.grid(row=3, column=2, columnspan=3)

        # Current Order
        self.order_label = tk.Label(self.master, text='Current Order', font=('Courier', 10), bg='LightSkyBlue4',
                                       fg='white')
        self.order_label.grid(row=4, column=1, sticky=tk.W)
        self.order_list = tk.Listbox(self.master, height=4, width=28, border=0)
        self.order_list.grid(row=5, column=1, columnspan=2,
                                rowspan=6, sticky=tk.W)
        # RIGHT
        self.parts_label_m2 = tk.Label(self.master, text='Items Collected', font=('Courier', 10), bg='LightSkyBlue4',
                                       fg='white')
        self.parts_label_m2.grid(row=4, column=3, sticky=tk.W)
        self.parts_list_m2 = tk.Listbox(self.master, height=4, width=30, border=0)
        self.parts_list_m2.grid(row=5, column=3, columnspan=2,
                                rowspan=6, sticky=tk.W)

        # Parts list 2 (listbox)
        self.parts_label_2 = tk.Label(self.master, text='Two Sonk', font=('Courier', 10), bg='LightSkyBlue4',
                                      fg='white')
        self.parts_label_2.grid(row=12, column=1, sticky=tk.W)
        self.parts_list_2 = tk.Listbox(self.master, height=4, width=60, border=0)
        self.parts_list_2.grid(row=13, column=1, columnspan=4,
                               rowspan=4, sticky=tk.W)

        # Parts list (listbox)
        self.parts_label = tk.Label(self.master, text='One Sonk', font=('Courier', 10), bg='LightSkyBlue4', fg='white')
        self.parts_label.grid(row=18, column=1, sticky=tk.W)
        self.parts_list = tk.Text(self.master, height=8, width=55, border=0)
        self.parts_list.grid(row=19, column=1, columnspan=4,
                             rowspan=8, sticky=tk.W)

        # Create scrollbar
        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.grid(row=19, column=4, rowspan=8, columnspan=2, sticky=tk.N + tk.S + tk.W)
        # Set scrollbar to parts
        self.parts_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.parts_list.yview)

        # BOTTM
        self.meme_label = tk.Label(self.master, text='Babba Bouey', font=('Courier', 10),
                                   bg='LightSkyBlue4', fg='white')
        self.meme_label.grid(row=28, column=1, sticky=tk.W)
        self.meme_entry = tk.Entry(self.master, textvariable=self.meme_label, width=60, bg='LightSkyBlue4', fg='white')
        self.meme_entry.grid(row=29, column=1, columnspan=4, sticky=tk.W)


    def add_item(self, item_list):
        for i in item_list:
            self.parts_list_m1.insert(tk.END, i)

    def new_order(self, order):
        # Clear order_list first
        self.order_list.delete(0, tk.END)
        #self.order_list
        for i in order.getItems():
            self.order_list.insert(tk.END, i)



    def update_status(self, string):
        # These strings will be properly formatted within the Warehouse Simulation methods
        self.parts_list.insert(tk.END, string)


class FloorGrid(tk.Canvas):

    def __init__(self, master, width, height):
        # Create Tk Canvas with Specified Height / Width
        super().__init__(master, width=width, height=height)
        self.master = master
        # Width & Height of Floor
        self.grid_width = width
        self.grid_height = height
        # Size of each Floor Cell 10 x 10
        self.unit_size = int(width / 10)
        # Make a checkered pattern on the Floor
        self.checkered(self, self.unit_size)
        self.populate()

        #self.grid(row=0, column=0)
    # Create the Grid layout for our display
    def checkered(self, canvas, line_distance):
        # Vertical lines at an interval of "line_distance" pixel
        for x in range(line_distance, self.grid_width, line_distance):
            canvas.create_line(x, 0, x, self.grid_height, fill="#476042")

        # Horizontal lines at an interval of "line_distance" pixel
        for y in range(line_distance, self.grid_height, line_distance):
            canvas.create_line(0, y, self.grid_width, y, fill="#476042")

    # Animation Methods
    def getDisplayRobot(self, robot_object):
        display_bot = None
        for bot in self.ROBOT_LIST:
            if bot.name == robot_object.getName():
                display_bot = bot

        return display_bot

    def getDisplayShelf(self, shelf_object):
        display_shelf = None
        for shelf in self.SHELF_LIST:
            if shelf.number == shelf_object.getShelfNo():
                display_shelf = shelf

        return display_shelf

    def rotateBelt(self):
        belt_length = len(self.BELT_LIST)
        count = 0
        for belt in self.BELT_LIST:
            if count == belt_length - 1:
                belt.move_belt(Point(belt.point.x, belt.point.y + belt_length - 1))

            else:
                # should move up one
                belt.move_belt(Point(belt.point.x, belt.point.y - 1))

            count += 1

        # Need to Sort belts by y (Highest first)
        self.BELT_LIST.sort(key=lambda belt: -belt.point.y)

    def grabBin(self, point):
        NEW_BIN = Display_Bin(self, point, self.unit_size, 'Bin')
        return NEW_BIN

    def createPackage(self, point):
        NEW_PACKAGE = Display_Package(self, point, self.unit_size, 'Pkg')
        return NEW_PACKAGE

    def deleteObject(self, display_object):
        self.delete(display_object.name)
        self.delete(display_object.id)
        self.update()

    # Setup Warehouse Display
    def populate(self):
        # Picker
        self.PICKER = Display_Picker(self, Point(1, 7), self.unit_size, 'Picker')

        # Packer
        self.PACKER = Display_Packer(self, Point(1, 4), self.unit_size, 'Packer')

        # Dock Area
        self.DOCK = Display_Dock(self, Point(0, 0), self.unit_size * 2, 'Dock')

        # Chargers
        self.CHARGER_1 = Display_Charger(self, Point(2, 9), self.unit_size, 'C1')
        self.CHARGER_2 = Display_Charger(self, Point(3, 9), self.unit_size, 'C2')
        self.CHARGER_3 = Display_Charger(self, Point(4, 9), self.unit_size, 'C3')
        self.CHARGER_4 = Display_Charger(self, Point(5, 9), self.unit_size, 'C4')
        self.CHARGER_5 = Display_Charger(self, Point(6, 9), self.unit_size, 'C5')

        # Robots
        self.ROBOT_1 = Display_Robot(self, Point(2, 9), self.unit_size, 'A')
        self.ROBOT_2 = Display_Robot(self, Point(3, 9), self.unit_size, 'B')
        self.ROBOT_3 = Display_Robot(self, Point(4, 9), self.unit_size, 'C')
        self.ROBOT_4 = Display_Robot(self, Point(5, 9), self.unit_size, 'D')
        self.ROBOT_5 = Display_Robot(self, Point(6, 9), self.unit_size, 'E')
        self.ROBOT_LIST = [self.ROBOT_1, self.ROBOT_2, self.ROBOT_3, self.ROBOT_4, self.ROBOT_5]

        # Belt
        self.BELT_1 = Display_Belt(self, Point(0, 7), self.unit_size, 'B1')
        self.BELT_2 = Display_Belt(self, Point(0, 6), self.unit_size, 'B2')
        self.BELT_3 = Display_Belt(self, Point(0, 5), self.unit_size, 'B3')
        self.BELT_4 = Display_Belt(self, Point(0, 4), self.unit_size, 'B4')
        self.BELT_5 = Display_Belt(self, Point(0, 3), self.unit_size, 'B5')
        self.BELT_6 = Display_Belt(self, Point(0, 2), self.unit_size, 'B6')
        self.BELT_LIST = [self.BELT_1, self.BELT_2, self.BELT_3, self.BELT_4, self.BELT_5, self.BELT_6]

        # Shelves
        self.SHELF_1 = Display_Shelf(self, Point(5, 1), self.unit_size, 'S1', 1)
        self.SHELF_2 = Display_Shelf(self, Point(6, 1), self.unit_size, 'S2', 2)
        self.SHELF_3 = Display_Shelf(self, Point(7, 1), self.unit_size, 'S3', 3)
        self.SHELF_4 = Display_Shelf(self, Point(8, 1), self.unit_size, 'S4', 4)
        self.SHELF_5 = Display_Shelf(self, Point(9, 1), self.unit_size, 'S5', 5)

        self.SHELF_6 = Display_Shelf(self, Point(5, 2), self.unit_size, 'S6', 6)
        self.SHELF_7 = Display_Shelf(self, Point(6, 2), self.unit_size, 'S7', 7)
        self.SHELF_8 = Display_Shelf(self, Point(7, 2), self.unit_size, 'S8', 8)
        self.SHELF_9 = Display_Shelf(self, Point(8, 2), self.unit_size, 'S9', 9)
        self.SHELF_10 = Display_Shelf(self, Point(9, 2), self.unit_size, 'S10', 10)

        self.SHELF_11 = Display_Shelf(self, Point(5, 5), self.unit_size, 'S11', 11)
        self.SHELF_12 = Display_Shelf(self, Point(6, 5), self.unit_size, 'S12', 12)
        self.SHELF_13 = Display_Shelf(self, Point(7, 5), self.unit_size, 'S13', 13)
        self.SHELF_14 = Display_Shelf(self, Point(8, 5), self.unit_size, 'S14', 14)
        self.SHELF_15 = Display_Shelf(self, Point(9, 5), self.unit_size, 'S15', 15)

        self.SHELF_16 = Display_Shelf(self, Point(5, 6), self.unit_size, 'S16', 16)
        self.SHELF_17 = Display_Shelf(self, Point(6, 6), self.unit_size, 'S17', 17)
        self.SHELF_18 = Display_Shelf(self, Point(7, 6), self.unit_size, 'S18', 18)
        self.SHELF_19 = Display_Shelf(self, Point(8, 6), self.unit_size, 'S19', 19)
        self.SHELF_20 = Display_Shelf(self, Point(9, 6), self.unit_size, 'S20', 20)
        self.SHELF_LIST = [self.SHELF_1, self.SHELF_2, self.SHELF_3, self.SHELF_4, self.SHELF_5,
                      self.SHELF_6, self.SHELF_7, self.SHELF_8, self.SHELF_9, self.SHELF_10,
                      self.SHELF_11, self.SHELF_12, self.SHELF_13, self.SHELF_14, self.SHELF_15,
                      self.SHELF_16, self.SHELF_17, self.SHELF_18, self.SHELF_19, self.SHELF_20]


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

        self.canvas.update()


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
        # Move Left
        if self.point.x > point.x and self.point.y == point.y:
            self.canvas.move(self.robot, (point.x - self.point.x) * self.unit_size, 0)
            self.canvas.move(self.robot_id, (point.x - self.point.x) * self.unit_size, 0)
            next_point = Point(self.point.x - 1, self.point.y)
            self.point = next_point

        # Move Right
        if self.point.x < point.x and self.point.y == point.y:
            self.canvas.move(self.robot, (point.x - self.point.x) * self.unit_size, 0)
            self.canvas.move(self.robot_id, (point.x - self.point.x) * self.unit_size, 0)
            next_point = Point(self.point.x + 1, self.point.y)
            self.point = next_point

        # Move Up
        if self.point.x == point.x and self.point.y > point.y:
            self.canvas.move(self.robot, 0, (point.y - self.point.y) * self.unit_size)
            self.canvas.move(self.robot_id, 0, (point.y - self.point.y) * self.unit_size)
            next_point = Point(self.point.x, self.point.y - 1)
            self.point = next_point

        # Move Down
        if self.point.x == point.x and self.point.y < point.y:
            self.canvas.move(self.robot, 0, (point.y - self.point.y) * self.unit_size)
            self.canvas.move(self.robot_id, 0, (point.y - self.point.y) * self.unit_size)
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
        # Move Up
        if self.point.x == point.x and self.point.y > point.y:
            self.canvas.move(self.belt, 0, (point.y - self.point.y) * self.unit_size)
            self.canvas.move(self.belt_id, 0, (point.y - self.point.y) * self.unit_size)
            next_point = Point(self.point.x, self.point.y - 1)
            self.point = next_point

        # Move Down to bottom location
        if self.point.x == point.x and self.point.y < point.y:
            self.canvas.move(self.belt, 0, (point.y - self.point.y) * self.unit_size)
            self.canvas.move(self.belt_id, 0, (point.y - self.point.y) * self.unit_size)
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
        # Move Left
        if self.point.x > point.x and self.point.y == point.y:
            self.canvas.move(self.shelf, (point.x - self.point.x) * self.unit_size, 0)
            self.canvas.move(self.shelf_id, (point.x - self.point.x) * self.unit_size, 0)
            next_point = Point(self.point.x - 1, self.point.y)
            self.point = next_point

        # Move Right
        if self.point.x < point.x and self.point.y == point.y:
            self.canvas.move(self.shelf, (point.x - self.point.x) * self.unit_size, 0)
            self.canvas.move(self.shelf_id, (point.x - self.point.x) * self.unit_size, 0)
            next_point = Point(self.point.x + 1, self.point.y)
            self.point = next_point

        # Move Up
        if self.point.x == point.x and self.point.y > point.y:
            self.canvas.move(self.shelf, 0, (point.y - self.point.y) * self.unit_size)
            self.canvas.move(self.shelf_id, 0, (point.y - self.point.y) * self.unit_size)
            next_point = Point(self.point.x, self.point.y - 1)
            self.point = next_point

        # Move Down
        if self.point.x == point.x and self.point.y < point.y:
            self.canvas.move(self.shelf, 0, (point.y - self.point.y) * self.unit_size)
            self.canvas.move(self.shelf_id, 0, (point.y - self.point.y) * self.unit_size)
            next_point = Point(self.point.x, self.point.y + 1)
            self.point = next_point

        self.canvas.update()

if Warehouse2.show_animation:


    root = tk.Tk()
    App = Application(master=root)
    Warehouse2.run()
    App.mainloop()

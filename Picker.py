
from Point import Point
from Bin import Bin


class Picker:
    """
    Picker class represents the person that takes each Item off the shelves carried by robots

    Picker will remain stationary at one location and wait for robots to bring
    shelves to its location. It will take order items off of the shelves and put
    them into a Bin for each order. When all of the items for an order have been
    gathered, the picker will move that Bin onto the Belt to go to the Packer

    Attributes:
        location: A Point object representing the location in warehouse
        belt_location: A Point object where the belt next to the Picker is located
        robot_location: A Point object where the robots will bring the shelves
    """

    def __init__(self, location):
        """
        Inits Packer with its own location

        Also calculates where the belt should be located next to Picker (one to left),
        and calculates the location the robots should be bringing shelves to

        Args:
            location: The x y position for the Picker
        """
        self.location = location
        self.belt_location = Point(location.x-1, location.y)
        self.robot_location = Point(location.x+1, location.y)

    def getPickLocation(self):
        """
        Returns the Picker's Point location

        Returns:
            The location of Picker
        """
        return self.location

    def getPickerBeltLocation(self):
        """
        Returns the Belt location next to Picker

        Returns:
            Point object which is the location of a Belt
        """
        return self.belt_location

    def getPickerRobotLocation(self):
        """
        Returns the location next to Picker where robots will arrive

        Returns:
            Point object which is where the shelves / robot will be
        """
        return self.robot_location

    def grabBin(self):
        """
        Creates a new Bin object that will store Items taken from Shelves

        Returns:
             new_bin: A Bin object containing nothing
        """
        new_bin = Bin()
        return new_bin

    def pickItem(self, shelf, item, order, order_bin, inventory):
        """
        Takes an Item off of the Shelf next to the Picker and adds it to the Bin

        Also updates Inventory and the Order about the Item collected

        Args:
            shelf: A Shelf object that contains the Item Picker needs to grab
            item: A Item object with will be taken off of Shelf and placed in Bin
            order: The Order object that is currently being fulfilled
            order_bin: A Bin object where the Item will be placed
            inventory: The Inventory object that keeps track of all Items in warehouse
        """
        item.changeShelf(None)
        shelf.removeItem(item)
        order_bin.addToBin(item)
        # Order now knows this item has been collected
        order.addItem(item)
        # Remove the item from inventory
        inventory.removeItem(item)

    def putOnBelt(self, order_bin, belt):
        """
        Places a Bin object on the Belt next to Picker's location

        Args:
            order_bin: A Bin object containing all needed Items for an Order
            belt: A Belt object representing the belt that is currently next to Picker
        """
        belt_cell = belt.getBeltLocation()
        belt.addObject(order_bin)
        belt_cell.setContents(order_bin)
        order_bin.changeLocation(belt.getBeltLocation())
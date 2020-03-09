"""
Picker will remain stationary at one location and wait for robots to bring
shelves to its location. It will take order items off of the shelves and put
them into a Bin for each order. When all of the items for an order have been
gathered, the picker will move that Bin onto the Belt to go to the Packer
"""
from Point import Point
from Bin import Bin

class Picker:

    def __init__(self, location):
        self.location = location
        self.beltlocation = Point(location.x-1, location.y)
        self.robotlocation = Point(location.x+1, location.y)
        #self.inventory = inventory

    def getPickLocation(self):
        return self.location

    def getPickerBeltLocation(self):
        # Picker knows belt will be one unit to their left
        return self.beltlocation

    def getPickerRobotLocation(self):
        # Picker know the Robot should arrive one unit to their left
        return self.robotlocation

    # Creates a new bin object
    def grabBin(self):
        new_bin = Bin()
        return new_bin

    # Takes an Item off of the Shelf and adds it to the Bin
    # Will also update Inventory and Order about the Item
    def pickItem(self, shelf, item, order, orderbin, inventory):

        item.changeShelf(None)              # Item is no longer on a shelf
        shelf.removeItem(item)              # Remove Item from shelf contents
        orderbin.addToBin(item)             # Item is in the Bin
        order.addItem(item)                 # Order now knows this item has been collected
        inventory.removeItem(item)          # Remove the item from inventory

    def putOnBelt(self, orderbin, belt):
        beltcell = belt.getBeltLocation()
        belt.addObject(orderbin)
        beltcell.setContents(orderbin)
        orderbin.changeLocation(belt.getBeltLocation())
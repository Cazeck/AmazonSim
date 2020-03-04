"""
Picker will remain stationary at one location and wait for robots to bring
shelves to its location. It will take order items off of the shelves and put
them into a Bin for each order. When all of the items for an order have been
gathered, the picker will move that Bin onto the Belt to go to the Packer
"""

class Picker:

    def __init__(self, location, inventory):
        self.location = location
        self.inventory = inventory

    def getPickLocation(self):
        return self.location

    # Takes an Item off of the Shelf and adds it to the Bin
    # Will also update Inventory and Order about the Item
    def pickItem(self, shelf, item, order, orderbin):

        item.changeShelf(None)              # Item is no longer on a shelf
        shelf.removeItem(item)              # Remove Item from shelf contents
        orderbin.addToBin(item)                  # Item is in the Bin
        order.addItem(item)                 # Order now knows this item has been collected
        self.inventory.removeItem(item)     # Remove the item from inventory

    def putOnBelt(self, orderbin, belt):
        print("I put bin on Belt")
        orderbin.changeLocation("Belt start Location")
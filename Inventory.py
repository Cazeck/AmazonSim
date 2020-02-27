from ShelfArea import ShelfArea
from Shelf import Shelf
from Item import Item

class Inventory:
    # Create a list with all stocked items in it
    def __init__(self):
        self.stock = []

        self.populate()
    # Adds an item to the stock
    # item = the item to add
    ## Do I assign a shelf here?
    def addItem(self, item):
        self.stock.append(item)

    # Finds out how many of an item is in stock
    # itemName is the item you want
    def numberInStockName(self, itemName):
        count = 0
        for i in self.stock:
            if itemName == i.getItemName():
                count += 1

        return count

    # Similar to above, but instead searches for serial number
    def numberInStockSerial(self, serialNo):
        count = 0
        for i in self.stock:
            if serialNo == i.getSerialNumber():
                count += 1

        return count

    # Test Method
    # Returns the item in stock at specified index number
    def getItemAtIndex(self, index):
        item = self.stock[index]
        return item

    # Finds a shelf that has a given item on it
    # To be called by Orders subset
    # In: serial no of item --> Out: the number of the shelf that it is on
    def findItemSerial(self, serialNo):
        for i in self.stock:
            if serialNo == i.getSerialNumber():
                return i.getShelf()
        return None      # item not found with matching serial

    # Finds a shelf that has a given item on it
    # To be called by Orders subset
    # In: name of item --> Out: the number of the shelf that it is on
    def findItemName(self, iName):
        for i in self.stock:
            if iName == i.getItemName():
                return i.getShelf()
        return None      # item not found with matching name


    def populate(self):
        # Creates a variety of items and then adds them to random shelves
        testitems = [Item('Bagpipe', 51009), Item('Tic-Tac', 57678), Item('Hydras Lament', 11008), Item('Socks', 13009),
                     Item('Puck', 34678), Item('Shifters Shield', 81035), Item('Tic-Tac', 57678), Item('Singular Orange', 34231)]

        # Add the Items into Stock
        for i in testitems:
            self.stock.append(i)

        # Do we now distribute this across shelves in Master
        # in Master
    # Method for tick? not exactly sure how this will work out at the moment


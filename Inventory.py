
import random
from Catalog import Catalog
from Item import Item
from ShelfArea import ShelfArea
from Shelf import Shelf

class Inventory:
    # Create a list with all stocked items in it
    def __init__(self, env, floor):
        self.clock = env
        self.floor = floor
        self.stock = []
        self.catalog = Catalog()

        self.populateStock()
        self.stockShelves()

    # Adds an item to the stock
    # item = the item to add
    def addItem(self, item):
        self.stock.append(item)

    def removeItem(self, item):
        self.stock.remove(item)

        # If there are no more of this Item in Stock
        if self.numberInStockName(item.itemName) == 0:
            # Resupply that Item
            self.restockItem(item.itemName)


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

    # From Master / Warehouse / Sim
    # Can delete old after test
    def stockShelves(self):
        # All Items in Inventory
        for item in self.stock:
            random_sarea = random.choice(self.floor.shelfareas)                     # Choose one of the ShelfAreas

            # Choose a random Shelf within above Shelf Area
            rcell_content = random.choice(random_sarea.areacontents).getContents()  # Content of Cell (List)
            random_shelf = rcell_content[0]                                         # Shelf within Cell
            random_shelf.addItem(item)                                              # Put Item on Shelf
            item.changeShelf(random_shelf.getShelfNo())                             # Tell Item which Shelf it's on

    # Takes an Item name, checks to see if it is in the catalog, and creates a new Item object if so
    # Then places this item onto a random shelf
    def restockItem(self, item):
        new_item = self.catalog.createItem(item)

        #print(f'new Item is: {new_item}')

        random_sarea = random.choice(self.floor.shelfareas)  # Choose one of the ShelfAreas

        # Choose a random Shelf within above Shelf Area
        rcell_content = random.choice(random_sarea.areacontents).getContents()  # Content of Cell (List)
        random_shelf = rcell_content[0]                                         # Shelf within Cell
        random_shelf.addItem(new_item)                                              # Put Item on Shelf
        new_item.changeShelf(random_shelf.getShelfNo())                          # Tell Item which Shelf it's on
        #print(f'{item} has been added to Shelf {random_shelf.getShelfNo()}')

        self.addItem(new_item)


    # Adds (One!) of each Item from the Catalog into stock
    # Will work out duplicates
    def populateStock(self):
        catalog = self.catalog.itemList

        for item in catalog:
            self.stock.append(item)

        # ---- Original Below -------
        # Creates a variety of items and then adds them to random shelves
        #testitems = [Item('Bagpipe', 51009), Item('Tic-Tac', 57678), Item('Hydras Lament', 11008), Item('Socks', 13009),
        #             Item('Puck', 34678), Item('Shifters Shield', 81035), Item('Tic-Tac', 57678), Item('Singular Orange', 34231)]

        # Add the Items into Stock
        #for i in testitems:
        #    self.stock.append(i)

        # Do we now distribute this across shelves in Master
        # in Master
    # Method for tick? not exactly sure how this will work out at the moment



import random
from Catalog import Catalog


class Inventory:
    """
    Inventory class tracks the total stock of all Items in the warehouse

    Can place Items on Shelves and make orders for new Items if stock runs out

    Attributes:
        clock: Reference to SimPy simulation environment
        floor: Reference to the Floor component
        stock: A list of all Item objects within the warehouse
        catalog: Catalog object that contains all possible Items used in the simulation
    """

    def __init__(self, env, floor):
        """
        Inits Inventory with the simulation environment and a reference to warehouse Floor layout

        During initialization, Inventory creates an instance of each Item in Catalog and distributes
        them across random Shelf objects within the warehouse

        Args:
            env: SimPy simulation environment
            floor: Floor object so we can communicate with this subset
        """
        self.clock = env
        self.floor = floor
        self.stock = []
        self.catalog = Catalog()

        self.populateStock()
        self.stockShelves()

    def addItem(self, item):
        """
        Adds an Item to the total stock of Inventory

        Args:
            item: Item object being added to stock
        """
        self.stock.append(item)

    def removeItem(self, item):
        """
        Remove a specified Item from Inventory stock. If it was the last instance of that Item,
        make an order to resupply that Item back into stock

        Args:
            item: Item object being removed
        """
        self.stock.remove(item)

        # If there are no more of this Item in Stock
        if self.numberInStockName(item.getItemName()) == 0:
            # Resupply that Item
            self.restockItem(item.getItemName())

    def numberInStockName(self, item_name):
        """
        Check Inventory stock to see how many of a specific Item is in stock based off of name

        Args:
            item_name: Item object being counted

        Returns:
            count: Integer of how many Items matching item_name are in stock
        """
        count = 0
        for i in self.stock:
            if item_name == i.getItemName():
                count += 1

        return count

    def numberInStockSerial(self, serial_no):
        """
        Check Inventory stock to see how many of a specific Item is in stock based off of serial number

        Args:
            serial_no: Item object being counted

        Returns:
            count: Integer of how many Items matching serial_no are in stock
        """
        count = 0
        for i in self.stock:
            if serial_no == i.getSerialNumber():
                count += 1

        return count

    def findItemSerial(self, serial_no):
        """
        Find an Shelf within the Warehouse that has a given Item on it. Searching by serial number

        Args:
            serial_no: Item object being searched for

        Returns:
            shelf_found: Integer that is the number of the Shelf holding an Item with matching serial_no

        Raises:
            Exception: Item cannot be found on a Shelf in warehouse
        """
        for i in self.stock:
            if serial_no == i.getSerialNumber():
                shelf_found = i.getShelf()
                return shelf_found

        raise Exception(f'Item {serial_no} cannot be found on a Shelf in the warehouse')

    def findItemName(self, item_name):
        """
        Find an Shelf within the Warehouse that has a given Item on it. Searching by Item name

        Args:
            item_name: Item object being searched for

        Returns:
            shelf_found: Integer that is the number of the Shelf holding an Item with matching item_name

        Raises:
            Exception: Item cannot be found on a Shelf in warehouse
        """
        for i in self.stock:
            if item_name == i.getItemName():
                shelf_found = i.getShelf()
                return shelf_found
        raise Exception(f'Item {item_name} cannot be found on a Shelf in the warehouse')

    def stockShelves(self):
        """
        Takes every Item object within stock and places each Item on an random Shelf object within the warehouse
        """
        for item in self.stock:
            # Choose one of the Shelf Areas randomly
            random_sarea = random.choice(self.floor.shelf_areas)

            # Choose a random Shelf within above Shelf Area
            rcell_content = random.choice(random_sarea.area_contents).getContents()  # Content of Cell (List)
            random_shelf = rcell_content[0]                                          # Shelf within Cell
            random_shelf.addItem(item)                                               # Put Item on Shelf
            item.changeShelf(random_shelf.getShelfNo())                              # Tell Item which Shelf it's on

    def restockItem(self, item_name):
        """
        Takes an Item name, checks to see if it is within the Catalog, and creates a new Item
        object with the same name and places it ont a random Shelf within the warehouse

        Args:
            item_name: A string representing the name of the Item we are restocking
        """
        new_item = self.catalog.createItem(item_name)

        # Choose one of the Shelf Areas
        random_sarea = random.choice(self.floor.shelf_areas)

        # Choose a random Shelf within above Shelf Area
        rcell_content = random.choice(random_sarea.area_contents).getContents()  # Content of Cell (List)
        random_shelf = rcell_content[0]                                          # Shelf within Cell
        random_shelf.addItem(new_item)                                           # Put Item on Shelf
        new_item.changeShelf(random_shelf.getShelfNo())                          # Tell Item which Shelf it's on

        self.addItem(new_item)

    def populateStock(self):
        """
        Adds one instance of each Item object within the Catalog into Inventory stock
        """
        catalog = self.catalog.getItemList()
        for item in catalog:
            self.stock.append(item)

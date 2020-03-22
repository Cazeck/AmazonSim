
class Shelf:
    """
    Shelf class represents the shelves in the warehouse that contain the items used to fulfill orders.

    These shelves can be picked up by Robot objects and moved around the warehouse

    Class Variables:
        max_items: A integer representing the maximum amount of Items that shelf_stock can possess
        num_of_shelves: A integer used to count the total number of shelves created

    Attributes:
        shelf_number: A integer representing the number of a shelf
        home_location: Point object that is the original location the shelf was located at
        shelf_stock: A list that will consist of Item objects as they are placed on the shelf
        resting: A boolean indicating if a shelf is being carried by a Robot or not
    """
    max_items = 15
    num_of_shelves = 0

    def __init__(self, number, home):
        """
        Inits Shelf with a number and a home location

        Args:
            number: A integer to be used as the name of the shelf (Ex: Shelf 1)
            home: A Point object marking where to return the shelf to if moved
        """
        self.shelf_number = number
        self.home_location = home
        self.shelf_stock = []
        self.resting = True
        Shelf.num_of_shelves += 1

    def addItem(self, item):
        """
        Adds an Item object onto the Shelf, as long as it is not full

        Args:
            item: A Item object that will be placed onto the shelf

        Raises:
            Exception: Shelf is full
        """
        if len(self.shelf_stock) == self.max_items:
            raise Exception(f'Shelf {self.getShelfNo()} is full: Cannot put this item here')

        else:
            self.shelf_stock.append(item)

    def removeItem(self, item):
        """
        Remove an Item object from the Shelf

        Args:
            item: A Item object that will be removed from the shelf
        """
        self.shelf_stock.remove(item)

    def findItem(self, name):
        """
        Returns an Item on the Shelf with a matching name

        Args:
            name: A string with an item's name

        Returns:
            item: A Item object that's name matches the item argument
        """
        for item in self.shelf_stock:
            if name == item.getItemName():
                return item

    def getHomeLocation(self):
        """
        Returns the home location of the Shelf object

        Returns:
            The Point object, home_location of the shelf object
        """
        return self.home_location

    def getShelfNo(self):
        """
        Returns the shelf number of the Shelf object

        Returns:
            The shelf_number of the shelf object
        """
        return self.shelf_number

    def onShelf(self):
        """
        Returns the stock of the Shelf object

        Returns:
            The list of Items that Shelf currently possesses
        """
        return self.shelf_stock

    def __repr__(self):
        """
        Unambiguous representation of Shelf object

        Used for debugging and logging

        Returns:
            In the format: Shelf(shelf_number, home_location, resting, shelf_stock)
            Ex: Shelf(11, Point(1, 2), True, [Items])
        """
        return "Shelf('{}', '{}', {}, {})".format(self.shelf_number, self.home_location, self.resting, self.shelf_stock)

    def __str__(self):
        """
        Readable representation of Shelf object

        Used for display

        Returns:
            In the format:
            Shelf: 11 - HomeLoc: Point(1, 2), True
            Stock: [Item, Item, Item]
        """
        return 'Shelf: {} -  HomeLoc: {} - Resting: {} \nStock: {}'.format(self.shelf_number, self.home_location,
                                                                           self.resting, self.shelf_stock)





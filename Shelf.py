import Item

class Shelf:
    # Class Variable, applies to all instances
    maxItems = 5
    numofshelves = 0

    def __init__(self, number, home):
        # Both of these will be Point Objects
        # Location of where the shelf could be at any time
        # Where to return to
        self.shelfNumber = number
        self.shelfStock = []
        self.homeLocation = home
        self.resting = True   # Whether or not the shelf is moving

        Shelf.numofshelves += 1

    # Adds an item onto the shelf, check number of times on shelf to not overflow
    def addItem(self, item):
        if len(self.shelfStock) == self.maxItems:
            # Not sure what to do here yet, but need to not add the item and try to find a new shelf
            print('This shelf is full: Cannot put this item here')

        else:
            #print('Adding item to shelf ' + str(item))
            self.shelfStock.append(item)
            # Give an item it's shelf number here

    def removeItem(self, item):
        self.shelfStock.remove(item)

    # If a item with matching name is on shelf, return it
    def findItem(self, name):
        for item in self.shelfStock:
            if name == item.itemName:
                return item

    def getHomeLocation(self):
        return self.homeLocation

    def getShelfNo(self):
        return self.shelfNumber

    def onShelf(self):
        return self.shelfStock


    # Umambiguous reperestation of object, used for debugging / loggin - seen for developers
    # Item('Bong', 67090, 4)
    def __repr__(self):
        return "Shelf('{}', '{}', {}, {})".format(self.shelfNumber, self.homeLocation, self.resting, self.shelfStock)

    # readable representation of an object, used for display to end users
    # Item: Hydras Lament - Serial No: 11008 - Shelf: None
    def __str__(self):
        return '| Shelf: {} -  HomeLoc: {} - Resting: {} \n| Stock: {}'.format(self.shelfNumber, self.homeLocation, self.resting, self.shelfStock)





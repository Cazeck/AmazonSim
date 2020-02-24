
class Item:

    # Every item has a name, serial number, and shelf it belongs on (no shelf at the moment)
    def __init__(self, itemName, serialNumber):
        self.itemName = itemName
        self.serialNumber = serialNumber
        self.shelf = None

    # Return the item's name
    def getItemName(self):
        return self.itemName

    # Return the item's serial number
    def getSerialNumber(self):
        return self.serialNumber

    # Return the shelf that the item is on
    def getShelf(self):
        return self.shelf

    # Change the shelf than an Item is on
    def changeShelf(self, newShelf):
        self.shelf = newShelf

    # Umambiguous reperestation of object, used for debugging / loggin - seen for developers
    # Item('Bong', 67090, 4)
    def __repr__(self):
        return "Item('{}', '{}', {})".format(self.itemName, self.serialNumber, self.shelf)

    # readable representation of an object, used for display to end users
    # Item: Hydras Lament - Serial No: 11008 - Shelf: None
    def __str__(self):
        return 'Item: {} - Serial No: {} - Shelf: {}'.format(self.itemName, self.serialNumber, self.shelf)




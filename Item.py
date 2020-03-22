
class Item:
    """
    Item class represents the items that people will order from Amazon.

    Attributes:
        item_name: A string representing the name of an item
        serial_number: A integer representing the serial code of an item
        shelf: A reference to a Shelf object when an item is on a shelf
    """

    def __init__(self, serial_number, item_name):
        """
        Inits Item with a serial number and an item name

        shelf is set to None at the moment because the Item is not on a shelf yet

        Args:
            serial_number: The serial number for this item
            item_name: The name of the item
        """
        self.serial_number = serial_number
        self.item_name = item_name
        self.shelf = None

    def getItemName(self):
        """
        Returns the name of the Item object

        Returns:
            The item_name of the item object
        """
        return self.item_name

    def getSerialNumber(self):
        """
        Returns the serial number of the Item object

        Returns:
            The serial_number of the Item object
        """
        return self.serial_number

    def getShelf(self):
        """
        Returns the Shelf that the Item is on

        Returns:
            The Shelf object that this Item is located at
        """
        return self.shelf

    def changeShelf(self, new_shelf):
        """
        Changes the Shelf that Item is located at to new_shelf

        Args:
            new_shelf: A Shelf object that now contains this Item
        """
        self.shelf = new_shelf

    def __repr__(self):
        """
        Unambiguous representation of Item object

        Used for debugging and logging

        Returns:
            In the format: Item(item_name, serial_number, shelf)
            Ex: Item("TV Stand", 364422, Shelf 13)
        """
        return "Item('{}', '{}', Shelf {})".format(self.item_name, self.serial_number, self.shelf)

    def __str__(self):
        """
        Readable representation of Item object

        Used for display

        Returns:
            In the format: Item: "TV Stand" - Serial No: 364422 - Shelf: 13
        """
        return 'Item: {} - Serial No: {} - Shelf: {}'.format(self.item_name, self.serial_number, self.shelf.getShelfNo())




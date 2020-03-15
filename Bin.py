
class Bin:
    """
    Bin class represents the bins that are filled with items needed to fulfill an order

    These bins will be created by the Picker and then be moved around using the Belt

    Class Variables:
        bin_size: A integer representing the maximum amount of Items that a bin can possess
        num_of_bin: A integer used to count the total number of bins

    Attributes:
        contents: A list of Item objects needed for an Order
        location: Point object that is the current location of the Bin
        bin_id: A integer used to identify different Bins
    """

    bin_size = 5
    num_of_bins = 1

    def __init__(self):
        """
        Inits Bin with a bin id
        """
        self.contents = []
        self.location = None
        self.bin_id = self.num_of_bins
        self.num_of_bins += 1

    def getContents(self):
        """
         Returns all of the Items that are currently in the Bin

         Returns:
             contents: list of Item Object
         """
        return self.contents

    def changeLocation(self, new_location):
        """
        Changes the Cell that Bin is located at to new location

        Args:
            new_location: A Cell object that the Bin location will be changed to
        """
        self.location = new_location

    def addToBin(self, item):
        """
        Adds an object into the Bin, as long as the Bin isn't

        Args:
            item: An Item that will be placed onto the Belt

        Raises:
            Exception: Bin is full
        """
        if len(self.contents) < self.bin_size:
            self.contents.append(item)

        else:
            raise Exception(f'Bin is full')

    def removeFromBin(self, item_to_remove):
        """
        Remove an object from the Belt

        Args:
            item_to_remove: A Item that will be removed from Bin's content

        Raises:
            Exception: Bin is empty
        """
        if len(self.getContents()) > 0:
            self.contents.remove(item_to_remove)
        else:
            raise Exception(f'Bin is empty')




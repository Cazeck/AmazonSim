
class Package:
    """
    Package class represents the boxes containing Items that are shipped to customers

    Attributes:
        contents: A list of Items that the package contains
        destination: A string that is an address to be shipped to
    """

    def __init__(self):
        """
        Inits Package with an empty list

        The attributes of each Package will be given to it by the Packer class
        """
        self.contents = []
        self.destination = None

    def addToPackage(self, item):
        """
        Adds an Item object to Package's contents

        Args:
            item: A Item object that is now within the Package
        """
        self.contents.append(item)

    def setDestination(self, location):
        """
        Changes the address that the Package is to be shipped to

        Args:
            location: A string that is simply an address
        """
        self.destination = location

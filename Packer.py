
from Point import Point
from Package import Package


class Packer:
    """
    Packer class represents the person that packages all of the items within an order

    Packer will remain stationary at one location and wait for the belt to bring
    bins to its location. It will then take items out of the bins and package
    them in order to be shipped. When done creating the package, the picker
    will move the Package onto the Belt to go to the Shipping Dock

    Attributes:
        location: A Point object representing the location in warehouse
        belt_location: A Point object where the belt next to the Packer is located
    """

    def __init__(self, location):
        """
        Inits Packer with its own location

        Also calculates where the belt should be located next to Packer (one to left)

        Args:
            location: The x y position for the Packer
        """
        self.location = location
        self.belt_location = Point(location.x - 1, location.y)

    def getLocation(self):
        """
        Returns the Packer's Point location

        Returns:
            Point object which is location of Packer
        """
        return self.location

    def getPackerBeltLocation(self):
        """
        Returns the Belt location next to Packer

        Returns:
            Point object which is location of a Belt
        """
        return self.belt_location

    def createPackage(self, order_bin, address):
        """
        Creates a new Package object containing the contents of order_bin to be shipped to an address

        Args:
            order_bin: A Bin object containing all of needed Item objects to complete an Order
            address: A string representing the address this new package will be sent to

        Returns:
             package: A Package object containing all of the Item objects
        """
        package = Package()
        package.setDestination(address)

        for item in order_bin.getContents():
            package.addToPackage(item)

        return package

    def takeOffBelt(self, order_bin, belt):
        """
        Removes a Bin object from the Belt at Packer's location

        Args:
            order_bin: A Bin object containing Item objects
            belt: A Belt object representing the belt that is currently in front of Packer
        """
        belt_cell = belt.getBeltLocation()
        belt.removeObject(order_bin)
        belt_cell.removeContent(order_bin)
        order_bin.changeLocation("Off of Belt")

    def putOnBelt(self, package, belt):
        """
        Places a Package object on the Belt next to Packer's location

        Args:
            package: A Package object ready to be shipped
            belt: A Belt object representing the belt that is currently next to Packer
        """
        belt_cell = belt.getBeltLocation()
        belt.addObject(package)
        belt_cell.setContents(package)

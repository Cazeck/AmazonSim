"""
Packer will remain stationary at one location and wait for the belt to bring
bins to its location. It will then take items out of the bins and package
them in order to be shipped. When done creating the package, the picker
will move the Package onto the Belt to go to the Shipping Dock

Also creates Package objects
"""
from Point import Point
from Order import Order

class Packer:

    def __init__(self, location):
        self.location = location
        self.beltlocation = Point(location.x - 1, location.y)

    def getLocation(self):
        return self.location

    def getPackerBeltLocation(self):
        return self.beltlocation

    # Take all Items within the Bin and puts them into a package to be shipped
    def createPackage(self, orderbin, address):
        # Create new Package Object
        package = Package()
        package.setDestination(address)
        # Add the contents of the bin to it
        for item in orderbin.getContents():
            package.addToPackage(item)

        return package

    def takeOffBelt(self, orderbin, belt):
        beltcell = belt.getBeltLocation()
        belt.removeObject(orderbin)
        beltcell.removeContent(orderbin)
        orderbin.changeLocation("Off of Belt")
        #print(f'Bin has been taken off of Belt {belt.id}')

    def putOnBelt(self, package, belt):
        beltcell = belt.getBeltLocation()
        belt.addObject(package)
        beltcell.setContents(package)
        #print(f'Package has been placed on Belt {belt.id}')

"""
Package is just a box that will be filled with Order Items 
and shipped
"""
class Package:
    def __init__(self):
        self.contents = []
        self.destination = None

    def addToPackage(self, item):
        self.contents.append(item)

    def setDestination(self, location):
        self.destination = location

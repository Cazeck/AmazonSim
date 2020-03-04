"""
Packer will remain stationary at one location and wait for the belt to bring
bins to its location. It will then take items out of the bins and package
them in order to be shipped. When done creating the package, the picker
will move the Package onto the Belt to go to the Shipping Dock

Also creates Package objects
"""

class Packer:

    def __init__(self, location):
        self.location = location

    def getLocation(self):
        return self.location

    # Take all Items within the Bin and puts them into a package to be shipped
    def createPackage(self, orderbin):
        # Create new Package Object
        package = Package()
        # Add the contents of the bin to it
        for item in orderbin.getContents():
            package.addToPackage(item)

        return package

    def takeOffBelt(self, orderbin, belt):
        print("I take Bin ooff Belt")
        orderbin.setLocation("At Packer")

    def putOnBelt(self, package, belt):
        print("I put package on Belt")
        package.setLocation("Belt Location Packer")

"""
Package is just a box that will be filled with Order Items 
and shipped
"""
class Package:
    def __init__(self):
        self.contents = []
        self.location = None

    def addToPackage(self, item):
        self.contents.append(item)

    def setLocation(self, location):
        self.location = location

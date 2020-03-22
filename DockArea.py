
class DockArea:
    """
    DockArea class represents the Shipping Dock segment of the Warehouse that takes completed Orders
    in the shape of Packages and ships them to the desired address

    As of right now, we simply just delete the Package when shipping

    Attributes:
        points: A list of Point objects that fill the Shipping Dock
    """

    def __init__(self, point_list):
        """
        Inits Shelf with list of Points, these points represent the Cells that fill the Shipping Dock

        Args:
            pointlist: A list of Point objects
        """
        self.points = point_list

    def shipPackage(self, belt, package):
        """
        Takes a Package off of the Belt at DockArea location and "Ships" it from the Warehouse

        We just delete the package because we have nothing else to do with it once the Order
        has been completed

        Args:
            belt: Belt object representing the Belt section that is in front of Dock Area
            package: Package object that is being shipped from the Warehouse
        """
        # Location of Belt at DockArea
        belt_cell = belt.getBeltLocation()
        belt.removeObject(package)
        belt_cell.removeContent(package)
        del package

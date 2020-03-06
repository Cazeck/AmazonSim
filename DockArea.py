"""
m,eem
"""

class DockArea:

    def __init__(self, pointlist):
        self.points = pointlist

    def shipPackage(self, belt, package):
        beltcell = belt.getBeltLocation()       # Location of Belt at DockArea
        belt.removeObject(package)              # Remove Package from Belt
        beltcell.removeContent(package)         # Remove Package from Cell
        print(f'Package has been shipped to {package.destination}')
        del package                             # Delete Package from Memory
        print('Package Deleted')

"""
m,eem
"""

class DockArea:

    def __init__(self, pointlist):
        self.points = pointlist

    def shipPackage(self, belt, package):
        beltcell = belt.getBeltLocation()       # Location of Belt at DockArea
        belt.removeObject(package)              # Remove Package from Belt
        # Needed? when package display is worked out
        #beltcell.removeContent(package)         # Remove Package from Cell
        del package                             # Delete Package from Memory

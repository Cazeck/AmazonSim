
class Bin:

    binsize = 5
    numofbins = 0

    def __init__(self):

        self.contents = []
        self.order = None       # Order that it is a part of
        self.finished = False   # Whether or not the bin has all of the items needed
        self.binId = self.numofbins  # Give an id when it is made
        self.numofbins += 1     # Move the id up for the next bin

    def isFinished(self):
        return self.finished

    def setFinished(self):
        self.finished = True

    def setOrder(self, ord):
        self.order = ord

    # Return which order this bin is a part of
    def getOrder(self):
        return self.order

    def getContents(self):
        return self.contents

    def addToBin(self, item):
        if len(self.contents) < self.binsize:
            self.contents.append(item)

        else:
            print("There is not enough room in this bin")

    def removeFromBin(self, item):
        self.contents.remove(item)


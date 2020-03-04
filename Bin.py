
class Bin:

    binsize = 5
    numofbins = 0

    def __init__(self):

        self.contents = []
        self.location = None
        self.binId = self.numofbins     # Give an id when it is made
        self.numofbins += 1             # Move the id up for the next bin

    def getContents(self):
        return self.contents

    def changeLocation(self, location):
        self.location = location

    def addToBin(self, item):
        if len(self.contents) < self.binsize:
            self.contents.append(item)

        else:
            print("There is not enough room in this bin")

    def removeFromBin(self, item):
        if len(self.getContents()) > 0:
            self.contents.remove(item)
        else:
            print("The bin is empty")





class Belt:

    def __init__(self, id, capacity, width):
        self.id = id
        self.capacity = capacity
        self.width = width
        self.currentBins = []
        self.moving = False         # Whether or not the belt is moving down the line


    def pauseBelt(self):
        self.moving = False

    def resumeBelt(self):
        self.moving = True

    def getCurrentBins(self):
        return self.currentBins

    def addBin(self, bin):
        self.currentBins.append(bin)

    def removeBin(self, bin):
        self.currentBins.remove(bin)

    # Will need some way to implement tick so that we will be able to move
    # objects up the belt every tick
    def tick(self):
        return 'meme'

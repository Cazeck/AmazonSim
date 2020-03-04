
class Belt:

    def __init__(self, id, location):
        self.id = id
        self.location = location
        self.content = None
        self.moving = False

    def pauseBelt(self):
        self.moving = False

    def resumeBelt(self):
        self.moving = True

    # Returns a Cell
    def getBeltLocation(self):
        return self.location

    def getBeltCoord(self):
        return self.location.cellLocation()

    def addObject(self, object):
        if self.content is None:
            self.content = object
        else:
            print(f'Already an object on Belt {self.id}')

    def removeObject(self, object):
        self.content = None

    def getContent(self):
        return self.content

    def __str__(self):
        return'Belt No: {} - Contents: {}'.format(self.id, self.content)
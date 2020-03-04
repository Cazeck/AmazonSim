
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

    def addObject(self, object):
        if self.content is None:
            self.content = object
        else:
            print(f'Already an object on Belt {self.id}')

    def removeObject(self, object):
        self.content = None


    def __str__(self):
        return'Belt No: {} - Contents: {} Location: {}'.format(self.id, self.content, self.location)
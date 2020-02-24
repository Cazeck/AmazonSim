
from Shelf import Shelf

# Shelf area has information where every shelf is at all times
# is also used to create and shelves

class ShelfArea:

    def __init__(self):
        self.allShelves = []

    def numberOfShelves(self):
        return len(self.allShelves)

    # Finds a shelf with its number
    def findShelf(self, shelfNo):
        for i in self.allShelves:
            if shelfNo == i.shelfNumber:
                return i
        return None  # item not found with matching serial

    def findShelfWithSpace(self):
        for i in self.allShelves:
            if len(i.shelfStock) < i.maxItems:
                #print('This shelf is not full, returning')
                return i

            else:
                #print('This shelf is full, checking another')
                continue

    def addShelve(self, shelf):
        self.allShelves.append(shelf)





class Belt:
    """
    Belt class represents the belt in the warehouse that move bins and packages from location to location

    Each belt object represents one section of the belt, a belt might be 10 belt objects in a row

    Attributes:
        number: A integer representing the number for a section of the Belt
        location: Cell object that is the location the shelf is currently at
        content: Can be any object that is on this specific Belt unit at this time (usually Bin or Package)
    """

    def __init__(self, number, location):
        """
        Inits Belt with an id number and a Cell location

        Args:
            number: A integer to be used as the name of the shelf (Ex: Shelf 1)
            location: A Cell object representing the Belt unit's location on the Floor
        """
        self.belt_number = number
        self.location = location
        self.content = None

    def getBeltNo(self):
        """
        Returns the belt number of the Belt Section

        Returns:
            The belt_number of the Belt
        """
        return self.belt_number

    def setLocation(self, new_location):
        """
        Changes the Cell that Belt is located at to new location

        Args:
            new_location: A Cell object that the Belt location will be changed to
        """
        self.location = new_location

    def getBeltLocation(self):
        """
         Returns the current cell location of the Belt

         Returns:
             The Cell object, location of the Belt object
         """
        return self.location

    def getBeltCoord(self):
        """
         Returns the current cell location of the Belt as a Point

         Returns:
             Point object, location of the Belt object
         """
        return self.location.cellLocation()

    def addObject(self, new_object):
        """
        Adds an object onto the Belt, as long as one isn't already on it

        Args:
            new_object: An object that will be placed onto the Belt

        Raises:
            Exception: Belt already has an object on it
        """
        if self.content is None:
            self.content = new_object
        else:
            raise Exception(f'Already an object on Belt {self.belt_number}')

    def removeObject(self, object_to_remove):
        """
        Remove an object from the Belt

        Args:
            object_to_remove: A object that will be removed from Belt section's content

        """
        self.content = None

    def getContent(self):
        """
         Returns the current object that is on the Belt section

         Returns:
             Bin object, Package object, or None
         """
        return self.content

    def __str__(self):
        """
        Readable representation of Belt object

        Used for display

        Returns:
            In the format:
            Belt No: 4 - Contents: Bin object
        """
        return'Belt No: {} - Contents: {}'.format(self.belt_number, self.content)

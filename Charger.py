
class Charger:
    """
    Package class represents a location that a Robot would return to when it is not doing a task

    Attributes:
        location: A Point object which is the Charger's location in the Warehouse

    """
    def __init__(self, location):
        """
        Inits Charger with a Point location
        """
        self.location = location

    def getChargerLocation(self):
        """
        Returns the location of the Charger

        Returns:
            Point object
        """
        return self.location

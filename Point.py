
# Point is used to establish coordinates in the shelf area


# x = Right/Left , y = Up/Down
class Point:

    # Class Variables, applies to all instances
    areasizeX = 10      # Width of Area (East)
    areasizeY = 10      # Height of Area (North)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Return the point just "right" of this point (= East)
    # or return none if there is no "right"
    def right(self):
        newx = self.x + 1
        if newx > self.areasizeX:
            print("out of bounds")
            return None
        return Point(newx, self.y)

    # Return the point just "left" of this point (= West)
     # or return none if there is no "left"
    def below(self):
        newx = self.y - 1
        if newx < 0:
            print("out of bounds")
            return None
        return Point(newx, self.y)

    # Return the point just "above" this point (= North)
    # or return none if there is no "above"
    def above(self):
        newy = self.y + 1
        if newy > self.areasizeY:
            print("out of bounds")
            return None
        return Point(self.x, newy)

    # Return the point just "below" this point (= South)
    # or return none if there is no "below"
    def below(self):
        newy = self.y - 1
        if newy < 0:
            print("out of bounds")
            return None
        return Point(self.x, newy)


    # Compares two points against each other to see if they are equal
    def equals(self, otherPoint):
        issame = self.x == otherPoint.x and self.y == otherPoint.y
        return issame

    def __repr__(self):
        return "Point('{}', '{}')".format(self.x, self.y)

    def __str__(self):
        return "Point x:{} y:{}".format(self.x, self.y)



#point1 = Point(5,3)

#point2 = Point(5,2)
#print(point1)
#print(point2)

#print(point1.equals(point2))

#print(point1.above())

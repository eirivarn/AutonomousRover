from Utils import lineAngle


class Line:
    def __init__(self, p1, p2):
        # Point: [x, y] or (x, y)
        self.p1 = tuple(p1)
        self.p2 = tuple(p2)


        # Angle is 130 if the line points approximately from the bottom right to top left
        # Angle is 60 if the line points approximately from the bottom left to the top right
        self.angle = 180 - lineAngle(self.p1, self.p2)

    def __str__(self):
        return "Angle: " + str(self.angle) + "  P1: " + str(self.p1) + "  P2: " + str(self.p2)

    def __iter__(self):
        for point in [self.p1, self.p2]:
            yield point
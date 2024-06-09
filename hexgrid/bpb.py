import math

class Point:
    def __init__(self, x, y) -> None:
        self.x, self.y = x, y

    def __str__(self) -> str:
        return f"{self.x}, {self.y}"

class Orientation:
    def __init__(self, f0, f1, f2, f3, b0, b1, b2, b3, sa) -> None:
        self.f0, self.f1, self.f2, self.f3 = f0, f1, f2, f3
        self.b0, self.b1, self.b2, self.b3 = b0, b1, b2, b3
        self.start_angle = sa        

colors = {
    "BLACK": (0,0,0),
    "RED": (217, 28, 44),
    "GREEN": (36, 133, 57),
    "BGREEN": (170, 255, 0),
    "WHITE": (255, 255, 255),
    "GREY": (128, 128, 128),
    "BROWN": (64, 43, 39),
    "SANDISH": (194, 178, 128),
}

LAYOUT_POINTY = Orientation(math.sqrt(3.0), math.sqrt(3.0)/2.0, 0.0, 3.0/2.0, 
                            math.sqrt(3.0)/3.0, -1.0/3.0, 0.0, 2.0/3.0, 
                            0.5)

LAYOUT_FLAT = Orientation(3.0/2.0, 0.0, math.sqrt(3.0)/2.0, math.sqrt(3.0), 
                           2.0/3.0, 0.0, -1.0/3.0, math.sqrt(3.0)/3.0, 
                           0.0)

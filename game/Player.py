import random

class Player:
    def __init__(self, city) -> None:
        self.city = city
        self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
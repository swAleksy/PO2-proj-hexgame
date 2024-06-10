import random

class Player:
    def __init__(self, name, city, is_player) -> None:
        self.name = name
        self.city = city
        self.units = []
        self.is_player = is_player
        
    def add_unit(self, unit):
        self.units.append(unit)

    def remove_unit(self, unit):
        self.units.remove(unit)
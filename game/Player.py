
class Player:
    def __init__(self, name, city, color) -> None:
        self.name = name
        self.city = city
        self.color = color
        self.units = []

    def add_unit(self, unit):
        self.units.append(unit)

    def remove_unit(self, unit):
        self.units.remove(unit)

    def refill_movement(self):
        for unit in self.units:
            print(unit)
            unit.refill_movement()

    def __str__(self) -> str:
        return f"Player: {self.name}, city:{self.city}"
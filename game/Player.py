class Player:
    def __init__(self, name, color) -> None:
        self.name = name
        self.color = color
        self.units = []
        self.wonders = []
        self.city = None

    def add_unit(self, unit):
        self.units.append(unit)

    def remove_unit(self, unit):
        self.units.remove(unit)

    def add_wonder(self, wonder):
        self.wonders.append(wonder)

    def rm_wonder(self, wonder):
        self.wonders.remove(wonder)

    def add_city(self, city):
        self.city = city

    def refill_movement(self):
        for unit in self.units:
            print(unit)
            unit.refill_movement()

    def __str__(self) -> str:
        return f"Player: {self.name}"
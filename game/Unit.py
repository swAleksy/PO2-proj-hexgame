import pygame
from hexgrid.SpriteUnit import SpriteUnit
from hexgrid.Hex import City

class Unit(pygame.sprite.Sprite):
    def __init__(self, owner, hex, image_path):
        super().__init__()
        self.owner = owner
        self.current_hex = hex
        self.img_path = image_path
        self.sprite = SpriteUnit(hex.center, image_path)

    def draw_unit(self, screen):
        self.sprite.draw_unit_sprite(screen, self.owner.color)
        self.sprite.draw_unit_hp_bar(screen)

    def attack(self, hex):
        hex.unit.health -= self.attack_power
        print(hex.unit.health)
        if hex.unit.health <= 0:
            hex.remove_unit()
            print(hex.unit)

    def attack_city(self, hex):
        hex.hp -= self.attack_power
        hex.update_city_sprite()
        if hex.hp <= 0:
            print("GAME OVER")

    def rm_unit(self):
       self.kill()


class Infantry(Unit):
    def __init__(self, owner, position, image_path, health=12):
        super().__init__(owner, position, image_path)
        self.max_health = 12
        self.health = health
        self.attack_power = 4

    def move_to(self, new_hex):
        if isinstance(new_hex.unit, Unit) and self.owner != new_hex.owner:
            self.attack(new_hex)

        elif isinstance(new_hex, City) and new_hex.hp > 0 and self.owner != new_hex.owner:
            self.attack_city(new_hex)

        else:
            new_hex.add_unit(Infantry(self.owner, new_hex, self.img_path, self.health))
            # new_hex.set_owner(self.owner)
            self.current_hex.remove_unit()

    def draw_unit(self, screen):
        self.sprite.draw_unit_sprite(screen, self.owner.color)
        self.sprite.draw_unit_hp_bar(screen, self.max_health, self.health)

    def __str__(self) -> str:
        return f"{type(self)}, {self.health}"
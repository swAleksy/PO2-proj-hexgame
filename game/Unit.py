import pygame
from hexgrid.SpriteUnit import SpriteUnit

class Unit(pygame.sprite.Sprite):
    def __init__(self, owner, position, image_path):
        super().__init__()
        self.owner = owner
        self.position = position
        self.sprite = SpriteUnit(self.position, image_path)

    def move_to(self, new_position):
        self.position = new_position
        self.rect.center = (new_position.center.x, new_position.center.y)

    def draw_unit(self, screen):
        self.sprite.draw_unit_sprite(screen, self.owner.color)

    # def attack(self, target_unit):
    #     target_unit.health -= self.attack_power
    #     if target_unit.health <= 0:
    #         target_unit.die()

    def die(self):
        # ----------------
        pass

class Infantry(Unit):
    def __init__(self, owner, position, image_path):
        super().__init__(owner, position, image_path)
        self.health = 10  
        self.attack_power = 10  
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

        self.deny_sfx = pygame.mixer.Sound("./assets/audio/deny.mp3")
        self.march_sfx = pygame.mixer.Sound("./assets/audio/march.mp3")
        self.fight_sfx = pygame.mixer.Sound("./assets/audio/fight.mp3")
        self.take_over_sfx = pygame.mixer.Sound("./assets/audio/takeOver.mp3")

    def draw_unit(self, screen):
        self.sprite.draw_unit_sprite(screen, self.owner.color)
        self.sprite.draw_unit_hp_bar(screen)

    def attack(self, hex):
        self.fight_sfx.play()
        hex.unit.health -= self.attack_power
        print(hex.unit.health)
        if hex.unit.health <= 0:
            hex.remove_unit()
            print(hex.unit)

    def attack_city(self, hex):
        self.fight_sfx.play()
        hex.hp -= self.attack_power
        hex.update_city_sprite()
        if hex.hp <= 0:
            print("GAME OVER")

    def take_over_hex(self):
        self.take_over_sfx.play()
        if self.current_hex.owner != self.owner:
            self.current_hex.set_owner(self.owner)

    def rm_unit(self):
       self.kill()

DEFAULT_HEALTH = 12
DEFAULT_MOVES = 1
DEFAULT_ATTACK_POWER = 4

class Infantry(Unit):
    def __init__(self, owner, position, image_path, infobox, health = DEFAULT_HEALTH, moves = DEFAULT_MOVES):
        super().__init__(owner, position, image_path)
        self.name = "Infantry"
        self.max_health = DEFAULT_HEALTH
        self.health = health
        self.attack_power = DEFAULT_ATTACK_POWER
        self.moves = moves
        self.infobox = infobox

    def move_to(self, new_hex):
        pos = new_hex.hex_ret_coords()
        if pos in self.current_hex.neighbor_list:
            if isinstance(new_hex.unit, Unit) and self.owner != new_hex.owner:
                self.moves -= 1
                self.attack(new_hex)

            elif isinstance(new_hex, City) and new_hex.hp > 0 and self.owner != new_hex.owner:
                self.moves -= 1
                self.attack_city(new_hex)

            else:
                self.moves -= 1
                cp_unit = Infantry(self.owner, new_hex, self.img_path, self.infobox, self.health, self.moves)
                for i in self.owner.units:
                    if i == self:
                        self.owner.remove_unit(i)
                self.owner.add_unit(cp_unit)
                
                new_hex.add_unit(cp_unit)
                # new_hex.set_owner(self.owner)
                self.march_sfx.play()
                self.rm_unit()
                self.current_hex.remove_unit()

        else:
            self.deny_sfx.play()

    def refill_movement(self):
        self.moves = 1

    def draw_unit(self, screen):
        self.sprite.draw_unit_sprite(screen, self.owner.color)
        self.sprite.draw_unit_hp_bar(screen, self.max_health, self.health)

    def draw_unit_infobox(self):
        self.infobox.draw_unit_infobox(self)

    def __str__(self) -> str:
        return f"Inf: {self.name}{type(self)}, {self.moves}, -- {self.current_hex}"
import pygame, math
from .bpb import colors

class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class SpriteCity(Sprite):
    icon_size = 64
    def __init__(self, pos, level = 1):
        super().__init__()
        self.x = pos.x
        self.y = pos.y
        self.default_city_icon = pygame.image.load("./assets/city.png").convert_alpha()
        self.image = pygame.transform.scale(self.default_city_icon, (self.icon_size, self.icon_size))
        self.rect = pygame.Rect(self.x-self.icon_size/2, self.y-self.icon_size/1.8, self.icon_size, self.icon_size)

    def draw_health_bar(self, screen, max_hp, acc_hp):
        start_pos = (self.x - self.icon_size/2, self.y - self.icon_size/2)
        end_pos = (self.x + self.icon_size/2, self.y - self.icon_size/2)
        perc = (acc_hp*100) / max_hp
        end_pos_acc = (start_pos[0]+self.icon_size*(perc/100), start_pos[1])
        pygame.draw.line(screen, colors["GREY"],start_pos, end_pos, 3)
        pygame.draw.line(screen, colors["BGREEN"],start_pos, end_pos_acc, 3)
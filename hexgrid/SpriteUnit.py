import pygame
from .bpb import colors

class SpriteUnit(pygame.sprite.Sprite):
    unit_size=32
    def __init__(self, pos, path):
        super().__init__()
        self.x = pos.x
        self.y = pos.y
        self.default_city_icon = pygame.image.load(path).convert_alpha()


        self.image = pygame.transform.scale(self.default_city_icon, (self.unit_size, self.unit_size))
        self.rect_for_sprite = pygame.Rect(self.x-self.unit_size/2, self.y-self.unit_size/2, self.unit_size, self.unit_size)

    def draw_unit_sprite(self, screen, color):
        filled_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        
        filled_surface.fill(color) 
        filled_surface.blit(self.image, (0, 0))
        
        screen.blit(filled_surface, self.rect_for_sprite.topleft)

    def draw_unit_hp_bar(self, screen, max_hp, acc_hp):
        start_pos = (self.x - self.unit_size/2, self.y + self.unit_size/2)
        end_pos = (self.x + self.unit_size/2, self.y + self.unit_size/2)
        perc = (acc_hp*100) / max_hp
        end_pos_acc = (start_pos[0]+self.unit_size*(perc/100), start_pos[1])
        pygame.draw.line(screen, colors["GREY"],start_pos, end_pos, 3)
        pygame.draw.line(screen, colors["BGREEN"],start_pos, end_pos_acc, 3)
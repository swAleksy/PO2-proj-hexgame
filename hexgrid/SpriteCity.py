import pygame
from .bpb import colors

class SpriteCity(pygame.sprite.Sprite):
    icon_size = 64
    def __init__(self, pos, path):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.x = pos.x
        self.y = pos.y
        self.default_city_icon = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.default_city_icon, (self.icon_size, self.icon_size))
        self.rect_for_sprite = pygame.Rect(self.x-self.icon_size/2, self.y-self.icon_size/1.8, self.icon_size, self.icon_size)
        self.font = pygame.font.SysFont("Arial",15)

    def draw_city(self, screen):
        screen.blit(self.image, self.rect_for_sprite)

    def draw_city_hpbar_and_name(self, screen, max_hp, acc_hp, city_name, color):
        start_pos = (self.x - self.icon_size/2, self.y - self.icon_size/2)
        end_pos = (self.x + self.icon_size/2, self.y - self.icon_size/2)
        perc = (acc_hp*100) / max_hp
        end_pos_acc = (start_pos[0]+self.icon_size*(perc/100), start_pos[1])
        pygame.draw.line(screen, colors["GREY"],start_pos, end_pos, 3)
        pygame.draw.line(screen, colors["BGREEN"],start_pos, end_pos_acc, 3)


        rect_for_name = pygame.Rect(self.x -15*2, self.y + self.icon_size/2.5, 15*4, 20)

        pygame.draw.rect(screen, color, rect_for_name, 0)
        
        pygame.draw.rect(screen, (72, 59, 45), rect_for_name, 2) 
        if sum(color)/len(color) > 150:
            img = self.font.render(city_name, True, (0, 0, 0))
        else:
            img = self.font.render(city_name, True, (200,200,200))


        text_rect = img.get_rect()
        text_rect.center = rect_for_name.center

        screen.blit(img, text_rect.topleft)
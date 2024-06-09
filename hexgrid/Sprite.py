import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class SpriteCity(Sprite):
    icon_size = 64
    def __init__(self, pos, level = 1):
        super().__init__()
        self.default_city_icon = pygame.image.load("./assets/city.png").convert_alpha()
        self.image = pygame.transform.scale(self.default_city_icon, (self.icon_size, self.icon_size))
        self.rect = pygame.Rect(pos.x-self.icon_size/2, pos.y-self.icon_size/1.8, self.icon_size, self.icon_size)

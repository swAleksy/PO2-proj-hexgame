import pygame

class SpriteWonder(pygame.sprite.Sprite):
    icon_size = 64
    def __init__(self, pos, path):
        super().__init__()
        self.x = pos.x
        self.y = pos.y
        self.default_city_icon = pygame.image.load(path).convert_alpha()

        self.image = pygame.transform.scale(self.default_city_icon, (self.icon_size, self.icon_size))
        self.rect_for_sprite = pygame.Rect(self.x-self.icon_size/2, self.y-self.icon_size/2, self.icon_size, self.icon_size)

    def draw_wonder_sprite(self, screen):
        screen.blit(self.image, self.rect_for_sprite)
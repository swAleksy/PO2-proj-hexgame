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
        self.font = pygame.font.SysFont("Arial",15)

    def draw_wonder_sprite(self, screen):
        screen.blit(self.image, self.rect_for_sprite)

    def draw_wonder_namebar(self, screen, name):
        rect_for_name = pygame.Rect(self.x -15*2, self.y + self.icon_size/2.5, 15*4, 20)

        pygame.draw.rect(screen, (200, 165, 125), rect_for_name, 0) 
        pygame.draw.rect(screen, (72, 59, 45), rect_for_name, 2) 

        img = self.font.render(name, True, (0, 0, 0))

        text_rect = img.get_rect()
        text_rect.center = rect_for_name.center

        screen.blit(img, text_rect.topleft)
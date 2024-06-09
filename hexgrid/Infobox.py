import pygame

class Infobox:
    def __init__(self, screen, width, height) -> None:
        self.x = width
        self.y = height
        self.screen = screen
        self.font = pygame.font.SysFont("Arial",15)

    def draw_city_infobox(self):
        rect = pygame.Rect(0, self.y-200, 300, 200)
        pygame.draw.rect(self.screen, (128, 128, 128), rect, 0) 
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 4) 
        img = self.font.render("TEST", True, (0, 0, 0))
        self.screen.blit(img, (15, self.y-180))
        
class CityInfoBox(Infobox):
    def __init__(self, screen, width, height) -> None:
        super().__init__(screen, width, height)
        
import pygame

class Infobox:
    def __init__(self, screen, width, height) -> None:
        self.x = width
        self.y = height
        self.screen = screen
        self.font = pygame.font.SysFont("Arial",15)
        self.rect = pygame.Rect(0, self.y-200, 300, 150)
        
    def draw_rect(self, color):
        pygame.draw.rect(self.screen, color, self.rect, 0) 
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 4)

    def get_rect(self):
        return self.rect

 
class CityInfoBox(Infobox):
    def __init__(self, screen, width, height) -> None:
        super().__init__(screen, width, height)

    def draw_city_infobox(self, city):
        self.draw_rect(city.owner.color)


        city_info = [
            f"Name: {city.city_name}",
            f"Owner: {city.owner}",
            f"HP: {city.hp}/{city.max_hp}",
            f"Money: {city.money}",
            f"Resources: {city.resources}"
        ]

        y_offset = self.y - 180
        for info in city_info:
            if sum(city.owner.color)/len(city.owner.color) > 128: 
                img = self.font.render(info, True, (0, 0, 0))
            else:
                img = self.font.render(info, True, (255,255,255))
            self.screen.blit(img, (15, y_offset))
            y_offset += 20 

class UnitInfoBox(Infobox):
    def __init__(self, screen, width, height) -> None:
        super().__init__(screen, width, height)

    def draw_unit_infobox(self, unit):
        self.draw_rect(unit.owner.color)

        city_info = [
            f"Name: {unit.name}",
            f"Owner: {unit.owner}",
            f"HP: {unit.health}/{unit.max_health}",
            f"Attack: {unit.attack_power}",
            f"moves: {unit.moves}"
        ]

        y_offset = self.y - 180
        for info in city_info:
            if sum(unit.owner.color)/len(unit.owner.color) > 128: 
                img = self.font.render(info, True, (0, 0, 0) )
            else:
                img = self.font.render(info, True, (255,255,255))
            self.screen.blit(img, (15, y_offset))
            y_offset += 20 
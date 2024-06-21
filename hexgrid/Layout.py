import pygame, math, random
from .bpb import Point, COUNTRIES, INF_UNIT_PATH, CITI_LEVEL, WONDERS
from .Hex import *
from .SpriteCity import SpriteCity
from .SpriteWonder import SpriteWonder
from game.Unit import Unit, Infantry
from game.Player import Player
from .Infobox import CityInfoBox, UnitInfoBox

class Layout:
    def __init__(self, orientation, size, origin, screen, w, h) -> None:
        self.width = w
        self.heigh = h
        self.orientation = orientation
        self.size = size
        self.origin = origin
        self.screen = screen
        self.map_array = None
        self.map_data = {}
        
    def set_hexagonal_map(self, N):
        hex_map = []
        for q in range(-N, N + 1):
            r1 = max(-N, -q - N)
            r2 = min(N, -q + N)
            for r in range(r1, r2 + 1):          
                h = Hex(q, r, -q - r)
                h.set_hex_center(hex_to_pixel(self, h))
                hex_map.append(h)

        self.map_array = hex_map

    def add_city_to_hexagonal_map(self):
        while True:
            random_index = random.randint(0, len(self.map_array) - 1)
            city_hex = self.map_array[random_index]
            if not isinstance(city_hex, City):
                random_nation = random.choice(COUNTRIES)

                player = Player(random_nation[0], random_nation[2])
                
                coords = city_hex.hex_ret_coords()
                city = City(coords[0], coords[1], coords[2], SpriteCity(city_hex.center, CITI_LEVEL[1]), random_nation[1], random_nation[2], player, CityInfoBox(self.screen, self.width, self.heigh))
                city.set_hex_center(hex_to_pixel(self, city))

                base_unit = Infantry(player, city, INF_UNIT_PATH, UnitInfoBox(self.screen, self.width, self.heigh))
                city.add_unit(base_unit)
                player.add_city(city)
                player.add_unit(base_unit)

                self.map_array[random_index] = city
                COUNTRIES.remove(random_nation) 

                break
        
        self.map_data = set(self.map_array)
        return player
    
    def add_wonders_to_hexagonal_map(self):
        while True:
            random_index = random.randint(0, len(self.map_array) - 1)
            wonder_hex = self.map_array[random_index]
            if not isinstance(wonder_hex, City) and not isinstance(wonder_hex, Wonder):
                random_wonder = random.choice(WONDERS)

                coords = wonder_hex.hex_ret_coords()
                wonder = Wonder(coords[0], coords[1], coords[2], SpriteWonder(wonder_hex.center, random_wonder[1]), random_wonder[0])
                wonder.set_hex_center(hex_to_pixel(self, wonder))

                self.map_array[random_index] = wonder
                WONDERS.remove(random_wonder) 

                if len(WONDERS) == 0:
                    break
        
        self.map_data = set(self.map_array)

    def draw_hexagonal_map(self, N: int) -> None:
        for hex in self.map_data:
            self.draw_hex(self.screen, hex)

    def redraw_hexagonal_map(self, N: int) -> None:
        buff = []
        for hex in self.map_data:   
            if isinstance(hex, City) or isinstance(hex, Wonder):
                buff.append(hex)
            else:
                self.draw_hex(hex)
                if isinstance(hex.unit, Unit):
                    hex.unit.draw_unit(self.screen)
        
        for hex in buff:
            self.draw_hex( hex)
            hex.draw(self.screen)
            if isinstance(hex.unit, Unit):
                hex.unit.draw_unit(self.screen)
                
        for hex in buff:
            hex.draw_info(self.screen)


    def draw_hex(self, h):
        corners = polygon_corners(self, h)
        point_list = [(p.x, p.y) for p in corners]
        pygame.draw.polygon(self.screen, h.color, point_list, 0)
        if (isinstance(h, City)):
            pygame.draw.polygon(self.screen, h.border_color, point_list, 4)
        elif h.border_color != (0,0,0): 
            pygame.draw.polygon(self.screen, h.border_color, point_list, 4)
        else: 
            pygame.draw.polygon(self.screen, h.border_color, point_list, 1)


def hex_to_pixel(layout, h):
    M = layout.orientation
    size = layout.size
    origin = layout.origin
    x = (M.f0 * h._q + M.f1 * h._r) * size.x
    y = (M.f2 * h._q + M.f3 * h._r) * size.y
    return Point(x + origin.x, y + origin.y)

def pixel_to_hex(layout, p):
    M = layout.orientation
    size = layout.size
    origin = layout.origin
    pt = Point((p.x - origin.x) / size.x, (p.y - origin.y) / size.y)
    q = M.b0 * pt.x + M.b1 * pt.y
    r = M.b2 * pt.x + M.b3 * pt.y
    return (q, r, -q - r)

def hex_corner_offset(layout, corner):
    M = layout.orientation
    size = layout.size
    angle = 2.0 * math.pi * (M.start_angle - corner) / 6.0
    return Point(size.x * math.cos(angle), size.y * math.sin(angle))

def polygon_corners(layout, h: Hex):
    corners = []
    center = hex_to_pixel(layout, h)
    for i in range(0, 6):
        offset = hex_corner_offset(layout, i)
        corners.append(Point(center.x + offset.x, center.y + offset.y))
    return corners

def mouse_click_return_hex(pos, layout, map_data):
    pixel = Point(pos[0], pos[1])
    coords = hex_round(pixel_to_hex(layout, pixel))
    for h in map_data:
        if h._q == coords[0] and h._r == coords[1] and h._s == coords[2]:
            return h

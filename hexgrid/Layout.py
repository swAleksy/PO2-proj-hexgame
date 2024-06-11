import pygame, math, random
from .bpb import Point, COUNTRIES, INF_UNIT_PATH
from .Hex import *
from .SpriteCity import SpriteCity
from .Infobox import *
from game.Unit import Unit
from game.Player import Player

class Layout:
    def __init__(self, orientation, size, origin, screen) -> None:
        self.orientation = orientation
        self.size = size
        self.origin = origin
        self.infobox = None
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

    def add_city_to_hexagonal_map(self, is_player):
        while True:
            random_index = random.randint(0, len(self.map_array) - 1)
            city_hex = self.map_array[random_index]
            if not isinstance(city_hex, City):
                random_nation = random.choice(COUNTRIES)
                player = Player(random_nation[0], self.map_array[random_index],random_nation[2], is_player)
                city = City(city_hex._q, city_hex._r, city_hex._s, SpriteCity(city_hex.center),random_nation[1],random_nation[2], Unit(player ,city_hex.center, INF_UNIT_PATH))
                self.map_array[random_index] = city
                COUNTRIES.remove(random_nation) 
                break
        
        self.map_data = set(self.map_array)
        return player

    def draw_hexagonal_map(self, N: int) -> None:
        for hex in self.map_data:
            self.draw_hex(self.screen, hex)

    def redraw_hexagonal_map(self, N: int) -> None:
        buff = []
        for hex in self.map_data:   
            if isinstance(hex, City):
                buff.append(hex)
            else:
                self.draw_hex(hex)
                if isinstance(hex.unit, Unit):
                    hex.unit.draw_unit(self.screen)
        
        for hex in buff:
            self.draw_hex( hex)
            hex.draw_city(self.screen)
            hex.unit.draw_unit(self.screen)

    def draw_hex(self, h):
        corners = polygon_corners(self, h)
        point_list = [(p.x, p.y) for p in corners]
        pygame.draw.polygon(self.screen, h.color, point_list, 0)
        if (isinstance(h, City)):
            pygame.draw.polygon(self.screen, h.border_color, point_list, 3)
        else:
            pygame.draw.polygon(self.screen, (0,0,0), point_list, 1)

    def set_city_infobox(self,window_x, window_y):
        self.infobox = CityInfoBox(self.screen, window_x, window_y)

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

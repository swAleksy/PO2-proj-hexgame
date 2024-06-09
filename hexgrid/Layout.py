import pygame, sys, math
from bpb import Point
from Hex import *
from Sprite import *
import random

class Layout:
    def __init__(self, orientation, size, origin) -> None:
        self.orientation = orientation
        self.size = size
        self.origin = origin
        self.map_data = {}
        
    def set_hexagonal_map(self, N):
        hex_map = set()

        for q in range(-N, N + 1):
            r1 = max(-N, -q - N)
            r2 = min(N, -q + N)
            for r in range(r1, r2 + 1):
                h = Hex(q, r, -q - r)
                h.set_hex_center(hex_to_pixel(layout, h))
                if r == 0 and q == 0:
                    h = City(q, r, -q-r, SpriteCity(h.center))
                hex_map.add(h)
        
        self.map_data = hex_map
        
    def draw_hexagonal_map(self, screen: pygame.Surface, N: int) -> None:

        for hex in self.map_data:

            self.draw_hex(screen, hex)


    def redraw_hexagonal_map(self, screen: pygame.Surface, N: int) -> None:

        for hex in self.map_data:

            self.draw_hex(screen, hex)

            if isinstance(hex, City):

                hex.draw_sprite(screen)

# def hexagonal_map_draw(screen, layout, N):
#     for q in range(-N, N + 1):
#         for r in range(-N, N + 1):       
#             if -N <= -q - r <= N:  
#                 draw_hex(screen, layout, Hex(q, r, -q - r))

# def hexagonal_map_redraw(screen, layout, N, hex_map):
#     for h in hex_map:
#         draw_hex(screen, layout, h)
#         if isinstance(h, City):
#             h.draw_sprite(screen)

def hexagonal_map_draw(screen: pygame.Surface, layout: Layout, N: int) -> None:

    for hex in layout.map_data:

        draw_hex(screen, layout, hex)


def hexagonal_map_redraw(screen: pygame.Surface, layout: Layout, N: int, map_data: set) -> None:

    for hex in map_data:

        draw_hex(screen, layout, hex)

        if isinstance(hex, City):

            hex.draw_sprite(screen)

def draw_hex(screen, layout, h):
    corners = polygon_corners(layout, h)
    point_list = [(p.x, p.y) for p in corners]
    pygame.draw.polygon(screen, h.color, point_list, 0)
    pygame.draw.polygon(screen, (0,0,0), point_list, 1)

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

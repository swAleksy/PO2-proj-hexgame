import pygame, sys, random
from Layout import *
from bpb import LAYOUT_POINTY, colors

pygame.init()
w ,h = 1300, 1000
screen = pygame.display.set_mode((w, h))

hexagon_size = 40
radius_of_hex_map = 7

clock = pygame.time.Clock()

layout = Layout(LAYOUT_POINTY, Point(hexagon_size, hexagon_size), Point(w // 2, h // 2))
#map_data = set_hexagonal_map(radius_of_hex_map, layout)
layout.set_hexagonal_map(radius_of_hex_map)
running = True
while running:
    screen.fill((colors["BROWN"]))
    hexagonal_map_redraw(screen, layout, radius_of_hex_map, layout.map_data)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            h = mouse_click_return_hex(pos, layout, layout.map_data)
            if h:
                h.switch_color(colors["GREEN"])

        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

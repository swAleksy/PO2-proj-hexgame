import pygame, sys, random
from hexgrid.Layout import *
from hexgrid.bpb import Point, LAYOUT_POINTY
from game.Player import Player

pygame.init()

w ,h = 1300, 1000
screen = pygame.display.set_mode((w, h))
hexagon_size = 40
radius_of_hex_map = 7

clock = pygame.time.Clock()

layout = Layout(LAYOUT_POINTY, Point(hexagon_size, hexagon_size), Point(w // 2, h // 2), screen)
layout.set_hexagonal_map(radius_of_hex_map)
p1 = layout.add_city_to_hexagonal_map(True)
p2 = layout.add_city_to_hexagonal_map(False)
layout.set_city_infobox(w,h)


running = True
while running:
    screen.fill((colors["DBLUE"]))
    layout.redraw_hexagonal_map(radius_of_hex_map)
    layout.infobox.draw_city_infobox()
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

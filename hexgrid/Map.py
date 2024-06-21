import pygame
from Layout import *
from bpb import LAYOUT_POINTY, colors, Point

pygame.init()
w ,h = 1300, 1000
screen = pygame.display.set_mode((w, h))

hexagon_size = 40
radius_of_hex_map = 7

clock = pygame.time.Clock()

layout = Layout(LAYOUT_POINTY, Point(hexagon_size, hexagon_size), Point(w // 2, h // 2), screen)
layout.set_hexagonal_map(radius_of_hex_map)
layout.set_infobox(w,h)


running = True
while running:
    screen.fill((colors["BROWN"]))
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

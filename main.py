import pygame, sys, random
from hexgrid.Layout import *
from hexgrid.bpb import Point, LAYOUT_POINTY, DENY_SFX_PATH
from game.Player import Player
from game.Unit import Unit

pygame.init()

w ,h = 1300, 1000
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Sedecjasz Major's Cywilizacja VII")
hexagon_size = 40
radius_of_hex_map = 7

clock = pygame.time.Clock()

layout = Layout(LAYOUT_POINTY, Point(hexagon_size, hexagon_size), Point(w // 2, h // 2), screen)
layout.set_hexagonal_map(radius_of_hex_map)

p1 = layout.add_city_to_hexagonal_map(True)
p2 = layout.add_city_to_hexagonal_map(False)
players = [p1, p2]

layout.add_wonders_to_hexagonal_map()
layout.set_city_infobox(w,h)
turn = 0
screen.fill(colors["DBLUE"])
font = pygame.font.SysFont("Tahoma", 36)
button_rect = pygame.Rect(10 , 10, 100, 50)
button_text = font.render(f'End Turn: {players[turn%2].name}', True, w)
deny_sfx = pygame.mixer.Sound(DENY_SFX_PATH)

running = True
unit_move_mode = False
selected_unit = None

while running:
    current_player = players[turn%2]
    # print(selected_unit)
    pygame.draw.rect(screen, (200,24,110), button_rect)
    screen.blit(button_text, (button_rect.x + 10, button_rect.y + 10))

    layout.redraw_hexagonal_map(radius_of_hex_map)
    layout.infobox.draw_city_infobox()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            if button_rect.collidepoint(event.pos):   
                current_player.refill_movement()
                unit_move_mode = False
                selected_unit = None
                turn += 1
                continue

            if unit_move_mode == False:
                pos = pygame.mouse.get_pos()
                h = mouse_click_return_hex(pos, layout, layout.map_data)
                if isinstance(h.unit, Unit) and h.unit.owner == current_player:
                    unit_move_mode = True
                    selected_unit = h.unit
                    print(selected_unit)
                elif isinstance(h.unit, Unit):
                    deny_sfx.play()

            elif unit_move_mode == True:

                where_to = pygame.mouse.get_pos()
                dest_hex = mouse_click_return_hex(where_to, layout, layout.map_data)
                if dest_hex is not h and selected_unit.moves > 0:
                    h.unit.move_to(dest_hex)
                    unit_move_mode = False
                    selected_unit = None
            


        elif event.type == pygame.KEYDOWN:
            print(f"test -- unit-m:{ unit_move_mode}; selectedu:{selected_unit}")
            if unit_move_mode == True:
                if event.key == pygame.K_UP:
                    selected_unit.take_over_hex()

        elif event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

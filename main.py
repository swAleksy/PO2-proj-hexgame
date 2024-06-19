import pygame, sys, random
from hexgrid.Layout import *
from hexgrid.bpb import Point, LAYOUT_POINTY, DENY_SFX_PATH
from game.Player import Player
from game.Unit import Unit

pygame.init()

w ,h = 1300, 1000
screen = pygame.display.set_mode((w, h))
hexagon_size = 40
radius_of_hex_map = 7

clock = pygame.time.Clock()

layout = Layout(LAYOUT_POINTY, Point(hexagon_size, hexagon_size), Point(w // 2, h // 2), screen, w, h)
layout.set_hexagonal_map(radius_of_hex_map)

p1 = layout.add_city_to_hexagonal_map()
p2 = layout.add_city_to_hexagonal_map()
players = [p1, p2]

layout.add_wonders_to_hexagonal_map()

font = pygame.font.SysFont("Tahoma", 20)
button_rect = pygame.Rect(w - 100, h - 100, 90, 90)
button_text = font.render(f'End Turn', True, w)
player1_font_render = font.render(players[0].name, True, w)
player2_font_render = font.render(players[1].name, True, w)
deny_sfx = pygame.mixer.Sound(DENY_SFX_PATH)

running = True

unit_move_mode = False
selected_unit = None
selected_hex = None

turn = 0
while running:
    screen.fill(colors["DBLUE"])
    current_player = players[turn % 2]
    # print(selected_unit)
    pygame.draw.rect(screen, colors["SANDISH"], button_rect)
    screen.blit(button_text, (button_rect.x + 6, button_rect.y + 30))

    layout.redraw_hexagonal_map(radius_of_hex_map)

    if turn % 2 == 0:
        screen.blit(player1_font_render, (button_rect.x + 6, button_rect.y - 30))
    else:
        screen.blit(player2_font_render, (button_rect.x + 6, button_rect.y - 30))

    # if selected_hex != None and isinstance(selected_hex, City):
    #     selected_hex.draw_infobox()

    # elif selected_unit != None:
    #     selected_unit.draw_unit_infobox()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            h = mouse_click_return_hex(pos, layout, layout.map_data)

            if button_rect.collidepoint(event.pos):
                current_player.refill_movement()
                unit_move_mode = False
                selected_unit = None
                turn += 1
                continue

            if not unit_move_mode:
                if isinstance(h.unit, Unit) and h.unit.owner == current_player:
                    unit_move_mode = True
                    selected_unit = h.unit
                    print(selected_unit)

                elif isinstance(h, Hex) and h.unit and h.unit.owner == current_player:
                    selected_hex = h

                elif h.unit is not None and isinstance(h.unit, Unit):
                    unit_move_mode = False
                    selected_unit = None
                    deny_sfx.play()

            elif unit_move_mode:
                where_to = pygame.mouse.get_pos()
                dest_hex = mouse_click_return_hex(where_to, layout, layout.map_data)
                if dest_hex is not selected_hex and selected_unit and selected_unit.moves > 0:
                    selected_unit.move_to(dest_hex)
                    unit_move_mode = False
                    selected_unit = None

        elif event.type == pygame.KEYDOWN:
            print(f"test -- unit-m:{unit_move_mode}; selectedu:{selected_unit}")
            if unit_move_mode:
                if event.key == pygame.K_UP and selected_unit:
                    selected_unit.take_over_hex()

        elif event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

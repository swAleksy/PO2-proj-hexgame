import pygame, sys, random
from hexgrid.Layout import *
from hexgrid.Buttons import *
from hexgrid.bpb import Point, LAYOUT_POINTY, DENY_SFX_PATH, INF_UNIT_PATH
from game.Player import Player
from game.Unit import Unit

pygame.init()

WIDTH, HEIGHT = 1300, 1000
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
hexagon_size = 40
radius_of_hex_map = 7

clock = pygame.time.Clock()

layout = Layout(LAYOUT_POINTY, Point(hexagon_size, hexagon_size), Point(WIDTH // 2, HEIGHT // 2), SCREEN, WIDTH, HEIGHT)
layout.set_hexagonal_map(radius_of_hex_map)

p1 = layout.add_city_to_hexagonal_map()
p2 = layout.add_city_to_hexagonal_map()
players = [p1, p2]

layout.add_wonders_to_hexagonal_map()

font = pygame.font.SysFont("Tahoma", 20)
# button_rect = pygame.Rect(w - 100, h - 100, 90, 90)
# button_text = font.render(f'End Turn', True, w)
player1_font_render = font.render(players[0].name, True, WIDTH)
player2_font_render = font.render(players[1].name, True, WIDTH)

next_turn_button = Button(WIDTH - 100, HEIGHT - 150, 90, 90, "Next Turn", colors["SANDISH"], (123, 63, 0))
new_unit_button = Button(0, HEIGHT - 50, 100, 50, "Buy unit", colors["SANDISH"], (123, 63, 0))
take_over_tile = Button(200, HEIGHT - 50, 100, 50, "Take tile", colors["SANDISH"], (123, 63, 0))
deny_sfx = pygame.mixer.Sound(DENY_SFX_PATH)

running = True

unit_move_mode = False
selected_unit = None
selected_hex = None

turn = 0
while running:
    SCREEN.fill(colors["DBLUE"])
    current_player = players[turn % 2]

    next_turn_button.draw(SCREEN)
    
    
    layout.redraw_hexagonal_map(radius_of_hex_map)

    
    button_center_x = (WIDTH - 100) + 90 // 2
    text_x1 = button_center_x - player1_font_render.get_width() // 2
    text_x2 = button_center_x - player2_font_render.get_width() // 2
    if turn % 2 == 0:
        SCREEN.blit(player1_font_render, (text_x1, HEIGHT - 60))
    else:
        SCREEN.blit(player2_font_render, (text_x2, HEIGHT - 60))

    if selected_hex != None and isinstance(selected_hex, City) and current_player == selected_hex.owner:
        selected_hex.draw_infobox()
        new_unit_button.draw(SCREEN)

    elif selected_unit != None:
        selected_unit.draw_unit_infobox()
        take_over_tile.draw(SCREEN)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            h = mouse_click_return_hex(pos, layout, layout.map_data)

            if next_turn_button.check_click(event):
                current_player.refill_movement()
                unit_move_mode = False
                selected_unit = None
                selected_hex = None
                turn += 1
                continue

            if new_unit_button.check_click(event):
                new_unit = Infantry(current_player, selected_hex, INF_UNIT_PATH, UnitInfoBox(SCREEN, WIDTH, HEIGHT))
                selected_hex.add_unit(new_unit)
                current_player.add_unit(new_unit)
                

            if take_over_tile.check_click(event):
                selected_unit.take_over_hex()

            if unit_move_mode == False and h != None:
                if isinstance(h.unit, Unit) and h.unit.owner == current_player:
                    unit_move_mode = True
                    selected_unit = h.unit
                    selected_hex = None
                    print(selected_unit)

                elif isinstance(h, City):
                    unit_move_mode = False
                    selected_unit = None
                    selected_hex = h

                elif h.unit is not None and isinstance(h.unit, Unit):
                    unit_move_mode = False
                    selected_unit = None
                    deny_sfx.play()

            elif unit_move_mode == True and h != None:
                where_to = pygame.mouse.get_pos()
                dest_hex = mouse_click_return_hex(where_to, layout, layout.map_data)
                selected_hex = None
                if dest_hex is not selected_hex and selected_unit is not None and selected_unit.moves > 0:
                    selected_unit.move_to(dest_hex)
                    unit_move_mode = False
                    selected_unit = None
                else:
                    unit_move_mode = False
                    selected_unit = None

        elif event.type == pygame.KEYDOWN:
            print(f"test -- unit-m:{unit_move_mode}; selectedu:{selected_unit}")
            if unit_move_mode:
                if event.key == pygame.K_UP and selected_unit:
                    selected_unit.take_over_hex()

        elif event.type == pygame.QUIT:
            running = False

    mouse_pos = pygame.mouse.get_pos()
    next_turn_button.check_hover(mouse_pos)
    new_unit_button.check_hover(mouse_pos)
    take_over_tile.check_hover(mouse_pos)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

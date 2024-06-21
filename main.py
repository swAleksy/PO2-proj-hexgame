import pygame, sys
from hexgrid.Layout import *
from hexgrid.Buttons import *
from hexgrid.bpb import Point, LAYOUT_POINTY, DENY_SFX_PATH, INF_UNIT_PATH
from game.Player import Player
from game.Unit import Unit

def start_menu():
    running = True
    font = pygame.font.SysFont("Tahoma", 70)
    start_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 60, 200, 50, "Start Game", colors["SANDISH"], (123, 63, 0))
    exit_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 10, 200, 50, "Exit", colors["SANDISH"], (123, 63, 0))

    big_text = font.render("CYWILIZACJA VII", True, (255, 255, 255))
    big_text_rect = big_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))

    while running:
        SCREEN.fill(colors["DBLUE"])
        SCREEN.blit(big_text, big_text_rect)
        start_button.draw(SCREEN)
        exit_button.draw(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if start_button.check_click(event):
                    return True
                if exit_button.check_click(event):
                    pygame.quit()
                    sys.exit()

        mouse_pos = pygame.mouse.get_pos()
        start_button.check_hover(mouse_pos)
        exit_button.check_hover(mouse_pos)

        pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    layout = Layout(LAYOUT_POINTY, Point(HEX_SIZE, HEX_SIZE), Point(WIDTH // 2, HEIGHT // 2), SCREEN, WIDTH, HEIGHT)
    layout.set_hexagonal_map(MAP_RADIOUS)

    p1 = layout.add_city_to_hexagonal_map()
    p2 = layout.add_city_to_hexagonal_map()
    players = [p1, p2]

    layout.add_wonders_to_hexagonal_map()

    font = pygame.font.SysFont("Tahoma", 20)
    # button_rect = pygame.Rect(w - 100, h - 100, 90, 90)
    # button_text = font.render(f'End Turn', True, w)
    player1_font_render = font.render(players[0].name, True, p1.color)
    player2_font_render = font.render(players[1].name, True, p2.color)

    next_turn_button = Button(WIDTH - 100, HEIGHT - 150, 90, 90, "Next Turn", colors["SANDISH"], (123, 63, 0))
    new_unit_button = Button(0, HEIGHT - 50, 100, 50, "Buy unit", colors["SANDISH"], (123, 63, 0))
    new_unit_button_flag = 0
    take_over_tile = Button(200, HEIGHT - 50, 100, 50, "Take tile", colors["SANDISH"], (123, 63, 0))
    take_over_tile_flag = 0

    deny_sfx = pygame.mixer.Sound(DENY_SFX_PATH)

    running = True

    unit_move_mode = False
    selected_unit = None
    selected_hex = None

    turn = 0
    while running:
        SCREEN.fill(colors["DBLUE"])
        current_player = players[turn % 2]
        other_player = players[(turn + 1) % 2]
        next_turn_button.draw(SCREEN)
        
        layout.redraw_hexagonal_map(MAP_RADIOUS)

        button_center_x = (WIDTH - 100) + 90 // 2
        text_x1 = button_center_x - player1_font_render.get_width() // 2
        text_x2 = button_center_x - player2_font_render.get_width() // 2
        if turn % 2 == 0:
            SCREEN.blit(player1_font_render, (text_x1, HEIGHT - 60))
        else:
            SCREEN.blit(player2_font_render, (text_x2, HEIGHT - 60))

        if selected_hex != None and isinstance(selected_hex, City) and current_player == selected_hex.owner:
            selected_hex.draw_infobox()
            if selected_hex.unit == None and selected_hex.money >= 50:
                new_unit_button.draw(SCREEN)
                new_unit_button_flag = 1

        elif selected_unit != None:
            selected_unit.draw_unit_infobox()
            if selected_unit.current_hex.owner != current_player and selected_unit.moves > 0:
                take_over_tile.draw(SCREEN)
                take_over_tile_flag = 1

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

                if new_unit_button.check_click(event) and new_unit_button_flag == 1:
                    new_unit = Infantry(current_player, selected_hex, INF_UNIT_PATH, UnitInfoBox(SCREEN, WIDTH, HEIGHT), 0)
                    selected_hex.money -= 50
                    selected_hex.add_unit(new_unit)
                    current_player.add_unit(new_unit)
                    
                if take_over_tile.check_click(event) and take_over_tile_flag == 1:
                    selected_unit.take_over_hex()
                    if isinstance(selected_unit.current_hex, Wonder):
                        current_player.add_wonder(selected_unit.current_hex)
                        print("test")
                        if selected_unit.current_hex in other_player.wonders:
                            print("test 2 ")
                            other_player.rm_wonder(selected_unit.current_hex)


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
                        selected_unit.move_to(dest_hex) ### move and attack
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


        new_unit_button_flag = 0
        take_over_tile_flag = 0

        if check_game_over(players):
            running = False

        pygame.display.flip()
        clock.tick(30)

def draw_game_over(winner):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # semi-transparent black
    SCREEN.blit(overlay, (0, 0))
    
    game_over_font = pygame.font.SysFont("Tahoma", 50)
    text = game_over_font.render(f"Game Over! {winner.name} Wins!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    SCREEN.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)  # wait for 3 seconds before closing

def check_game_over(players):
    if players[0].city.hp <= 0:
        draw_game_over(players[1])
        return True
    elif players[1].city.hp <= 0:
        draw_game_over(players[0])
        return True

    for player in players:
        if len(player.wonders) >= 3:
            draw_game_over(player)
            return True

    return False

pygame.quit()
if __name__ == "__main__":
    
    pygame.init()

    WIDTH, HEIGHT = 1300, 1000
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    HEX_SIZE = 40
    MAP_RADIOUS = 7
    start_menu()
    main()
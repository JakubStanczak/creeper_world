import pygame
import ground
import side_menu
from screen import screen_width, screen_height, win

pygame.init()

pygame.display.set_caption("Gray goo by Kuba")
map_ground = ground.Ground()
menu = side_menu.SideMenu()

def draw():
    win.fill((255, 255, 255))
    map_ground.draw()
    menu.draw()
    if game_mode == "map_generator":
        pygame.draw.line(win, (255, 0, 0), (map_ground.starting_pos_width, 0), (map_ground.starting_pos_width, screen_height))
        pygame.draw.line(win, (255, 0, 0), (screen_width - map_ground.starting_pos_width, 0), (screen_width - map_ground.starting_pos_width, screen_height))
    pygame.display.update()

pygame.key.set_repeat(2, 30)
run = True
game_mode = "map_generator"
map_completed = False
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if game_mode == "map_generator":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    map_completed = map_ground.add_segment(False)
                elif event.key == pygame.K_UP:
                    map_completed = map_ground.add_segment(True)
                elif event.key == pygame.K_RIGHT:
                    map_completed = map_ground.add_segment()
                if map_completed:
                    game_mode = "game_paused"
    draw()

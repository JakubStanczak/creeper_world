import pygame
import csv

import ground
import side_menu
import goo
from screen import screen_width, screen_height, win

pygame.init()

pygame.display.set_caption("Gray goo by Kuba")
map_ground = ground.Ground()
gray_goo = goo.Goo(map_ground.segment_width)
menu = side_menu.SideMenu()

def save_level():
    with open("level.csv", "w") as level_csv:
        fields = ["x", "y", "width"]
        log_writer = csv.DictWriter(level_csv, fieldnames=fields)
        log_writer.writeheader()
        for segment in map_ground.segments:
            line_csv = segment.csv_data()
            log_writer.writerow(line_csv)
    print("Map saved")

def load_level():
    # try:
    with open("level.csv") as level_csv:
        map_reader = csv.DictReader(level_csv)
        for segment in map_reader:
            map_ground.segments.append(ground.GroundSegment(int(segment["x"]), int(segment["y"]), int(segment["width"])))
    # except FileNotFoundError:
    #     global game_state
    #     game_state = "level maker"
    print("Map loaded")

def draw():
    win.fill((255, 255, 255))
    map_ground.draw()
    menu.draw()
    gray_goo.draw()
    if game_mode == "map_generator":
        pygame.draw.line(win, (255, 0, 0), (map_ground.starting_pos_width, 0), (map_ground.starting_pos_width, screen_height))
        pygame.draw.line(win, (255, 0, 0), (screen_width - map_ground.starting_pos_width, 0), (screen_width - map_ground.starting_pos_width, screen_height))
    pygame.display.update()

def time():
    gray_goo.gravity(map_ground)

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

                # save
                elif event.key == pygame.K_s:
                    save_level()
                elif event.key == pygame.K_l:
                    load_level()
                # more goo test
                elif event.key == pygame.K_g:
                    mouse_pos = pygame.mouse.get_pos()
                    gray_goo.more_goo(*mouse_pos)


                # if map_completed:
                #     game_mode = "game_paused"
    # pygame.time.delay(50)
    time()
    draw()

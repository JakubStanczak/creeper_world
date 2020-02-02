import pygame
import csv
from itertools import chain

import ground
import side_menu
import goo
import weapons
from screen import screen_width, screen_height, win

pygame.init()

pygame.display.set_caption("Gray goo by Kuba")
map_ground = ground.Ground()
gray_goo = goo.Goo(map_ground.segment_width, map_ground.segment_step)
menu = side_menu.SideMenu()
used_weapons = weapons.Weapons()

def save_level():
    with open("level.csv", "w") as level_csv:
        fields = ["object_type", "x", "y", "width"]
        log_writer = csv.DictWriter(level_csv, fieldnames=fields)
        log_writer.writeheader()
        for segment in map_ground.segments:
            line_csv = segment.csv_data()
            log_writer.writerow(line_csv)
        for goo_pix in chain.from_iterable(gray_goo.goo_grid):
            if goo_pix is not None:
                line_csv = goo_pix.csv_data(gray_goo)
                log_writer.writerow(line_csv)
    print("Map saved")

def load_level():
    map_ground.clear()
    gray_goo.clear()
    with open("level.csv") as level_csv:
        map_reader = csv.DictReader(level_csv)
        for line in map_reader:
            if line["object_type"] == "ground":
                map_ground.segments.append(ground.GroundSegment(int(line["x"]), int(line["y"]), int(line["width"])))
            if line["object_type"] == "goo_pix":
                gray_goo.more_goo(int(line["x"]), int(line["y"]))
    print("Map loaded")

def draw():
    win.fill((255, 255, 255))
    map_ground.draw()
    menu.draw()
    gray_goo.draw()
    used_weapons.draw()
    if game_mode == "map_generator":
        pygame.draw.line(win, (255, 0, 0), (map_ground.starting_pos_width, 0), (map_ground.starting_pos_width, screen_height))
        pygame.draw.line(win, (255, 0, 0), (screen_width - map_ground.starting_pos_width, 0), (screen_width - map_ground.starting_pos_width, screen_height))
    pygame.display.update()

def time():
    gray_goo.gravity(map_ground)
    used_weapons.time(map_ground, gray_goo)

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

                # save/load
                elif event.key == pygame.K_s:
                    save_level()
                elif event.key == pygame.K_l:
                    load_level()
                # goo test
                elif event.key == pygame.K_g:
                    mouse_pos = pygame.mouse.get_pos()
                    gray_goo.more_goo(*mouse_pos)
                # bomb test
                elif event.key == pygame.K_b:
                    mouse_pos = pygame.mouse.get_pos()
                    used_weapons.add_weapon("bomb", *mouse_pos)
                elif event.key == pygame.K_n:
                    mouse_pos = pygame.mouse.get_pos()
                    used_weapons.add_weapon("bullet", *mouse_pos)

                # if map_completed:
                #     game_mode = "game_paused"
    time()
    draw()

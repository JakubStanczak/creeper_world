import pygame
import csv
from itertools import chain

import ground as ground_class
import side_menu
import goo as goo_class
import weapons as weapon_class
import buildings as buildings_class
from screen import screen_width, screen_height, win

pygame.init()
main_font = pygame.font.SysFont("calibri", 20, bold=False)
pygame.display.set_caption("Gray goo by Kuba")


ground = ground_class.Ground()
goo = goo_class.Goo(ground.segment_width, ground.segment_step)
menu = side_menu.SideMenu()
weapons = weapon_class.Weapons()
buildings = buildings_class.Buildings()


def save_level():
    with open("level.csv", "w") as level_csv:
        fields = ["object_type", "x", "y", "width"]
        log_writer = csv.DictWriter(level_csv, fieldnames=fields)
        log_writer.writeheader()
        for segment in ground.segments:
            line_csv = segment.csv_data()
            log_writer.writerow(line_csv)
        for goo_pix in chain.from_iterable(goo.goo_grid):
            if goo_pix is not None:
                line_csv = goo_pix.csv_data(goo)
                log_writer.writerow(line_csv)
    print("Map saved")


def load_level():

    try:
        ground.clear()
        goo.clear()
        with open("level.csv") as level_csv:
            map_reader = csv.DictReader(level_csv)
            for line in map_reader:
                if line["object_type"] == "ground":
                    ground.segments.append(ground_class.GroundSegment(int(line["x"]), int(line["y"]), int(line["width"])))
                if line["object_type"] == "goo_pix":
                    goo.more_goo(int(line["x"]), int(line["y"]))
        print("Map loaded")
        global map_completed
        map_completed = True
        innit_game()
        return True
    except FileNotFoundError:
        print("level file not found")
        return False



def draw():
    win.fill((255, 255, 255))
    ground.draw()
    buildings.draw()
    goo.draw()
    weapons.draw()
    menu.draw()
    if not map_completed:
        text = "Use arrows to make the map \n press S to save map \n press L to load map"
        pygame.draw.line(win, (255, 0, 0), (ground.starting_pos_width, 0), (ground.starting_pos_width, screen_height))
        pygame.draw.line(win, (255, 0, 0), (screen_width - ground.starting_pos_width, 0), (screen_width - ground.starting_pos_width, screen_height))

    elif not first_click:
        text = """
        Target is simple: destroy the creep generating building.
        Build barracks, torrents and aircraft bases - but remember they need energy
        To produce energy dig tunnels (starting from your base) and build energy plants
        """
    else:
        text = ""
    text_lines = text.split("\n")
    for i, line in enumerate(text_lines):
        rendered_line = main_font.render(line, True, (0, 0, 0))
        win.blit(rendered_line, (100, 5 + 20 * i))

    pygame.display.update()


def time():
    buildings.time(ground, goo, weapons)
    weapons.time(ground, goo)
    goo.gravity(ground)
    pygame.time.set_timer(pygame.USEREVENT, 50)


def innit_game():
    goo.analyze_map(ground)
    buildings.add_building("mother", ground, 10)
    buildings.add_building("base", ground, screen_width - ground.starting_pos_width)
    buildings.mother.active = True
    buildings.base.active = True
    ground.add_coal(15)
    global first_click
    first_click = False

pygame.key.set_repeat(2, 30)
run = True
map_completed = False
map_analyzed = False
selected_building_type = None
mouse_clicked = False
time()
first_click = False
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.USEREVENT:
            time()
        elif event.type == pygame.KEYDOWN and not map_completed:
            if event.key == pygame.K_DOWN:
                map_completed = ground.add_segment(False)
            elif event.key == pygame.K_UP:
                map_completed = ground.add_segment(True)
            elif event.key == pygame.K_RIGHT:
                map_completed = ground.add_segment()
            elif event.key == pygame.K_l:
                map_completed = load_level()
            if map_completed:
                innit_game()
        elif event.type == pygame.KEYDOWN:
            # save/load
            if event.key == pygame.K_s:
                save_level()
            if event.key == pygame.K_ESCAPE:
                selected_building_type = menu.unselect_all()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_clicked = True
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] > screen_width:
                selected_building_type = menu.select(*mouse_pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_clicked = False

    if mouse_clicked:
        if not first_click:
            first_click = True
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] < screen_width:
            if selected_building_type is not None:
                if selected_building_type in buildings_class.building_types:
                    buildings.add_building(selected_building_type, ground, mouse_pos[0])
                elif selected_building_type == "tunnel":
                    ground.add_tunnel(*mouse_pos, buildings.base)
                elif selected_building_type == "target":
                    weapons.target = mouse_pos

    draw()

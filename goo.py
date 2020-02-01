import pygame
from screen import win, screen_height, screen_width
from itertools import chain

class Goo:
    def __init__(self, ground_width, ground_step):
        self.pix_width = ground_width
        self.pix_height = ground_step
        self.grid_x_dim = screen_width // self.pix_width
        self.grid_y_dim = screen_height // self.pix_height
        self.goo_grid = []
        for _ in range(self.grid_x_dim):
            line = []
            for _ in range(self.grid_y_dim):
                line.append(None)
            self.goo_grid.append(line)
        print("goo y dim = {}".format(self.grid_y_dim))
        print("goo x dim = {}".format(self.grid_x_dim))

    def more_goo(self, x, y):
        x_idx = x // self.pix_width
        y_idx = y // self.pix_height
        if self.goo_grid[x_idx][y_idx] is None:
            self.goo_grid[x_idx][y_idx] = GooPix(x_idx, y_idx, self.pix_width, self.pix_height)
            print(self.goo_grid[x_idx][y_idx])

    def draw(self):
        for goo_pix in chain.from_iterable(self.goo_grid):
            if goo_pix is not None:
                goo_pix.draw()

    def gravity(self, map_ground):
        for goo_pix in reversed(list(chain.from_iterable(self.goo_grid))):
            if goo_pix is not None:
                goo_pix.gravity(map_ground, self)

class GooPix:
    def __init__(self, x_idx, y_idx, width, height):
        self.x_idx = x_idx
        self.y_idx = y_idx
        self.width = width
        self.height = height
        self.color = (39, 196, 196)

    def draw(self):
        pygame.draw.rect(win, self.color, (self.x_idx * self.width, self.y_idx * self.height, self.width, self.height))

    def gravity(self, map_ground, goo):
        ground_y_idx = map_ground.segments[self.x_idx].y // self.height
        goo_y_idx = goo.grid_y_dim
        # find closest goo below
        for y in range(goo.grid_y_dim - 1, self.y_idx, -1):
            if goo.goo_grid[self.x_idx][y] is not None:
                goo_y_idx = y

        # TODO what if goo source is under the surface
        if goo_y_idx > ground_y_idx:
            if self.y_idx < ground_y_idx:
                self.move_to(goo, self.x_idx, self.y_idx + 1)
        else:
            if self.y_idx < goo_y_idx - 1:
                self.move_to(goo, self.x_idx, self.y_idx + 1)
            else:
                left_border_idx = self.find_border(map_ground, "L")
                right_border_idx = self.find_border(map_ground, "R")
                space_on_left = False
                for x_idx in range(self.x_idx, left_border_idx, -1):
                    if goo.goo_grid[x_idx][self.y_idx+1] is None:
                        self.move_to(goo, x_idx, self.y_idx+1)
                        space_on_left = True
                        break
                if not space_on_left:
                    for x_idx in range(self.x_idx, right_border_idx - 1):
                        if goo.goo_grid[x_idx][self.y_idx+1] is None:
                            self.move_to(goo, x_idx, self.y_idx+1)
                            break

    def find_border(self, map_ground, direction):
        y_idx = self.y_idx + 1
        x_idx = self.x_idx
        border_found = False
        while not border_found:
            if direction == "L":
                x_idx -= 1
            else:
                x_idx += 1
            if map_ground.segments[x_idx].y <= y_idx * self.height or x_idx == 0 or x_idx == len(map_ground.segments) - 1:
                return x_idx

    def move_to(self, goo, x_idx, y_idx):
        goo.goo_grid[self.x_idx][self.y_idx] = None
        self.x_idx = x_idx
        self.y_idx = y_idx
        goo.goo_grid[self.x_idx][self.y_idx] = self


    def __repr__(self):
        return "x_idx:{} y_idx:{}".format(self.x_idx, self.y_idx)
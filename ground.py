import pygame
import random
from itertools import chain
from screen import screen_width, screen_height, win

class Ground:
    def __init__(self):
        self.segment_width = 10
        self.segment_step = 10
        start_y = screen_height // 4
        self.start_y = start_y - (start_y % self.segment_step)
        self.current_y = self.start_y
        self.min_y = screen_height - 10
        self.current_x = 0
        self.starting_pos_width = 50

        self.segments = []
        self.coals = []
        self.tunnel_grid = []
        for _ in range(screen_width // self.segment_width):
            line = []
            for _ in range(screen_height // self.segment_step):
                line.append(None)
            self.tunnel_grid.append(line)
        print(self.tunnel_grid)


    def draw(self):
        for segment in self.segments:
            segment.draw()

        for tunnel in chain.from_iterable(self.tunnel_grid):
            if tunnel is not None:
                 tunnel.draw()

        for coal in self.coals:
            coal.draw()


    def add_segment(self, up=None):
        if self.current_x > screen_width - self.segment_width:
            return True
        # print("adding segment")
        if self.starting_pos_width < self.current_x < screen_width - self.starting_pos_width:
            if up is False and self.current_y < self.min_y:
                self.current_y += self.segment_step
            elif up is True and self.current_y > self.start_y:
                self.current_y -= self.segment_step
        self.segments.append(GroundSegment(self.current_x, self.current_y, self.segment_width))
        self.current_x += self.segment_width
        return False

    def add_coal(self, quantity):
        for _ in range(quantity):
            x_idx = random.randint(1, len(self.segments) - 2)
            x = self.segments[x_idx].x
            y = random.randint(self.segments[x_idx].y + self.segment_width, screen_height - self.segment_width)
            y = y - (y % self.segment_step)
            self.coals.append(Coal(x, y, self.segment_width))

    def add_tunnel(self, x, y, base):
        x = x - (x % self.segment_width)
        y = y - (y % self.segment_step)
        x_idx = x // self.segment_width
        y_idx = y // self.segment_step
        if x_idx > len(self.segments) - 2 or y_idx == (screen_height // self.segment_step) - 1:
            return
        print("adding tunnel x_idx{} y_idx{}".format(x_idx, y_idx))
        print("x-1 is {}".format(self.tunnel_grid[x_idx-1][y_idx]))
        if (x == base.x and y == base.y + base.size) or y > self.segments[x_idx].y:
            if (x == base.x and y == base.y + base.size) or self.tunnel_grid[x_idx-1][y_idx] is not None or self.tunnel_grid[x_idx+1][y_idx] is not None or self.tunnel_grid[x_idx][y_idx+1] is not None or self.tunnel_grid[x_idx][y_idx-1] is not None:
                if self.tunnel_grid[x_idx][y_idx] is None:
                    self.tunnel_grid[x_idx][y_idx] = Tunnel(x_idx, y_idx, self.segment_width)

                    for coal in self.coals:
                        if coal.x == x and coal.y == y:
                            coal.connected = True



    def clear(self):
        self.segments.clear()

    def __repr__(self):
        return str(self.segments)


class GroundSegment:
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        self.color = (205, 133, 63)

    def draw(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, screen_height))

    def csv_data(self):
        segment_data = {"object_type": "ground", "x": self.x, "y": self.y, "width": self.width}
        return segment_data

    def __repr__(self):
        return "x: {} y:{}".format(self.x, self.y)

class Coal:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.start_quantity = 100
        self.current_quantity = self.start_quantity
        self.connected = False


    def draw(self):
        if self.connected:
            color = (250, 180, 0)
        else:
            color = (0, 0, 0)
        pygame.draw.rect(win, color, (self.x, self.y, self.size, self.size))

class Tunnel:
    def __init__(self, x_ind, y_ind, size):
        self.x_ind = x_ind
        self.y_ind = y_ind
        self.color = (200, 200, 200)
        self.size = size

    def draw(self):
        pygame.draw.rect(win, self.color, (self.x_ind * self.size, self.y_ind * self.size, self.size, self.size))
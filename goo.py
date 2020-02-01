import pygame
from screen import win, screen_height

class Goo:
    def __init__(self, ground_segment_width):
        self.goo_pixes = []
        self.goo_pix_width = ground_segment_width
        self.goo_pix_height = 2

    def more_goo(self, x, y):
        ground_seg_num = x // self.goo_pix_width
        x = ground_seg_num * self.goo_pix_width
        for goo_pix in self.goo_pixes:
            if goo_pix.x == x and goo_pix.y == y:
                return
        self.goo_pixes.append(GooPix(x, y, self.goo_pix_width, self.goo_pix_height))
        # print("number of goo_pix on map is {}".format(len(self.goo_pixes)))

    def draw(self):
        for goo_pix in self.goo_pixes:
            goo_pix.draw()

    def gravity(self, map_ground):
        self.goo_pixes.sort(key=lambda x: x.y, reverse=True)
        for goo_pix in self.goo_pixes:
            goo_pix.gravity(map_ground, self)



class GooPix:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (39, 196, 196)

    def draw(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def gravity(self, map_ground, goo):
        ground_seg_idx = self.x // self.width
        ground_y = map_ground.segments[ground_seg_idx].y
        goo_pix_index = goo.goo_pixes.index(self)

        goo_y = screen_height
        for lower_goo_pix in goo.goo_pixes[:goo_pix_index]:
            if lower_goo_pix.x == self.x and lower_goo_pix.y < goo_y:
                goo_y = lower_goo_pix.y
        if goo_y < ground_y:
            if self.y + self.height > goo_y - self.height:
                self.y = goo_y - self.height
            else:
                self.y += self.height
        else:
            if self.y + self.height > ground_y - self.height:
                self.y = ground_y - self.height
            else:
                self.y += self.height


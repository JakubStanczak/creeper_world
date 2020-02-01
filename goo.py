import pygame
from screen import win

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
        print("number of goo_pix on board is {}".format(len(self.goo_pixes)))

    def draw(self):
        for goo_pix in self.goo_pixes:
            goo_pix.draw()

    def gravity(self):
        self.goo_pixes.sort(key=lambda x: x.y)
        for goo_pix in self.goo_pixes:
            pass



class GooPix:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (39, 196, 196)

    def draw(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

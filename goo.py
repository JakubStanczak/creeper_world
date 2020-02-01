import pygame
from screen import win, screen_height

class Goo:
    def __init__(self, ground_segment_width):
        self.goo_pixels = []
        self.goo_pix_width = ground_segment_width
        self.goo_pix_height = 4

    def more_goo(self, x, y):
        ground_seg_num = x // self.goo_pix_width
        x = ground_seg_num * self.goo_pix_width
        for goo_pix in self.goo_pixels:
            if goo_pix.x == x and goo_pix.y == y:
                return
        self.goo_pixels.append(GooPix(x, y, self.goo_pix_width, self.goo_pix_height))
        print("number of goo_pix on map is {}".format(len(self.goo_pixels)))

    def draw(self):
        for goo_pix in self.goo_pixels:
            goo_pix.draw()

    def gravity(self, map_ground):
        self.goo_pixels.sort(key=lambda x: x.y, reverse=True)
        for goo_pix in self.goo_pixels:
            goo_pix.gravity(map_ground, self)

    def __repr__(self):
        return str(self.goo_pixels)



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

        goo_y = screen_height
        for goo_pix in goo.goo_pixels:
            if goo_pix.y > self.y and goo_pix.x == self.x:
                if goo_pix.y < goo_y and goo_pix is not self:
                    goo_y = goo_pix.y
        if goo_y < ground_y:
            if self.y + self.height > goo_y - self.height:
                self.y = goo_y

                # check if lower level full
                left_bank_idx = self.find_bank("L", map_ground)
                right_bank_idx = self.find_bank("R", map_ground)
                for idx in range(ground_seg_idx, left_bank_idx, - 1):
                    location_ok = True
                    for goo_pix in goo.goo_pixels:
                        if goo_pix.x == map_ground.segments[idx].x and goo_pix.y == self.y:
                            location_ok = False
                            break
                    if location_ok:
                        self.x = map_ground.segments[idx].x
                        break
                if not location_ok:
                    self.y -= self.height
            else:
                self.y += self.height
        else:
            if self.y + self.height > ground_y - self.height:
                self.y = ground_y - self.height
            else:
                self.y += self.height

    def find_bank(self, side, map_ground):
        found_bank = False
        bank_idx = self.x // self.width
        while not found_bank:
            if side == "L":
                bank_idx -= 1
            else:
                bank_idx += 1
            bank_y = map_ground.segments[bank_idx].y
            if bank_y <= self.y or bank_idx == 0 or bank_idx == len(map_ground.segments) - 1:
                found_bank = True
        return bank_idx

    def __repr__(self):
        return "x:{} y:{}".format(self.x, self.y)


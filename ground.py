import pygame
from screen import screen_width, screen_height, win

class Ground:
    def __init__(self):
        self.start_y = screen_height // 4
        self.current_y = self.start_y
        self.min_y = screen_height - 10
        self.current_x = 0
        self.segment_width = 10
        self.segment_step = 10
        self.segments = []
        self.starting_pos_width = 50

    def draw(self):
        for segment in self.segments:
            segment.draw()

    def add_segment(self, up=None):
        if self.current_x > screen_width:
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


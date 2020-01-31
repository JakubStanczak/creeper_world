import pygame
from screen import win, screen_width, screen_height

class SideMenu:
    def __init__(self):
        self.buttons = []
        self.buttons.append(MenuButton("b1", screen_width + 30, 20, 50))

    def draw(self):
        pygame.draw.line(win, (0, 0, 0), (screen_width, 0), (screen_width, screen_height), 10)
        for button in self.buttons:
            button.draw()

class MenuButton:
    def __init__(self, name, x, y, size):
        self.name = name
        self.x = x
        self.y = y
        self.size = size
        self.color = (0, 255, 0)

    def draw(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size), 5)

import pygame
from screen import win, screen_width, screen_height

class SideMenu:
    def __init__(self):
        self.buttons = []
        self.button_size = 30
        self.button_space = 10
        self.add_button("gun")
        self.add_button("tunnel")

    def draw(self):
        pygame.draw.line(win, (0, 0, 0), (screen_width, 0), (screen_width, screen_height), 10)
        for button in self.buttons:
            button.draw()

    def add_button(self, name):
        self.buttons.append(MenuButton(name, screen_width + 10, len(self.buttons) * (self.button_size + self.button_space) + self.button_space, self.button_size))

    def select(self, x, y):
        self.unselect_all()
        for button in self.buttons:
            if button.x < x < button.x + button.size and button.y < y < button.y + button.size:
                button.selected = True
                return button.name
        return None

    def unselect_all(self):
        for button in self.buttons:
            button.selected = False


class MenuButton:
    def __init__(self, name, x, y, size):
        self.name = name
        self.x = x
        self.y = y
        self.size = size
        self.selected = False
        self.color = (0, 255, 0)


    def draw(self):
        if self.selected:
            thickness = 0
        else:
            thickness = 5
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size), thickness)

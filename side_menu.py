import pygame
from screen import win, screen_width, screen_height

class SideMenu:
    def __init__(self):
        self.buttons = []
        self.button_size = 30
        self.button_space = 10
        self.add_button("gun", "Torrent")
        self.add_button("tunnel", "Tunnel")
        self.add_button("barracks", "Barracks")
        self.add_button("aircraft_base", "Aircraft base")
        self.add_button("plant", "Energy Plant")
        self.add_button("target", "Set target")



    def draw(self):
        pygame.draw.line(win, (0, 0, 0), (screen_width, 0), (screen_width, screen_height), 10)
        for button in self.buttons:
            button.draw()

    def add_button(self, function_name, description):
        self.buttons.append(MenuButton(function_name, description, screen_width + 10, len(self.buttons) * (self.button_size + self.button_space) + self.button_space, self.button_size))

    def select(self, x, y):
        self.unselect_all()
        for button in self.buttons:
            if button.x < x < button.x + button.size and button.y < y < button.y + button.size:
                button.selected = True
                return button.function_name
        return None

    def unselect_all(self):
        for button in self.buttons:
            button.selected = False
        return None


class MenuButton:
    def __init__(self, function_name, description, x, y, size):
        self.function_name = function_name
        self.description = description
        self.x = x
        self.y = y
        self.size = size
        self.selected = False
        self.color = (0, 255, 0)
        self.font = pygame.font.SysFont("calibri", 15, bold=True)
        self.font_color = (0, 0, 0)


    def draw(self):
        if self.selected:
            thickness = 0
        else:
            thickness = 5
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size), thickness)
        rendered_text = self.font.render(str(self.description), True, self.font_color)
        win.blit(rendered_text, (self.x + self.size * 1.3, self.y + self.size / 4))

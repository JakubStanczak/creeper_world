import pygame
from screen import win

weapon_types = {
    "bomb": {"explosion_delay": 20, "explosion_time": 5, "explosion_size": 20, "explosion_color": (255, 0, 0), "weapon_size": 5, "weapon_color": (185, 190, 0), },
    "bullet": {"explosion_delay": 0, "explosion_time": 2, "explosion_size": 1, "explosion_color": (255, 0, 0), "weapon_size": 2, "weapon_color": (0, 0, 0)}
    }

class Weapons:
    def __init__(self):
        self.weapon_list = []

    def add_weapon(self, weapon_type, x, y):
        self.weapon_list.append(Weapon(weapon_type, x, y))

    def draw(self):
        for weapon in self.weapon_list:
            weapon.draw()

    def time(self, map_ground, goo):
        for weapon in self.weapon_list:
            destroyed = weapon.time(goo, map_ground)
            if destroyed:
                self.weapon_list.pop(self.weapon_list.index(weapon))
                return


class Weapon:
    def __init__(self, weapon_type, x, y):
        self.weapon_size = weapon_types[weapon_type]["weapon_size"]
        self.weapon_color = weapon_types[weapon_type]["weapon_color"]
        self.explosion_delay = weapon_types[weapon_type]["explosion_delay"]
        self.explosion_size = weapon_types[weapon_type]["explosion_size"]
        self.explosion_color = weapon_types[weapon_type]["explosion_color"]
        self.explosion_time = weapon_types[weapon_type]["explosion_time"]
        self.x = x
        self.y = y
        self.falling_speed = 10
        self.exploded = False

    def time(self, goo, ground):
        if not self.exploded:
            if self.explosion_delay == 0:
                self.exploded = True
                goo.explosion(self.explosion_size, self.x, self.y)
            else:
                self.explosion_delay -= 1
                self.gravity(ground)
        else:
            if self.explosion_time == 0:
                return True
            else:
                self.explosion_time -= 1
        return False

    def gravity(self, map_ground):
        for ground in map_ground.segments:
            if ground.x <= self.x < ground.x + ground.width:
                if self.y + self.falling_speed < ground.y:
                    self.y += self.falling_speed
                else:
                    self.y = ground.y


    def draw(self):
        if not self.exploded:
            pygame.draw.circle(win, self.weapon_color, (self.x, self.y), self.weapon_size)
        else:
            pygame.draw.circle(win, self.explosion_color, (self.x, self.y), self.explosion_size)


import pygame
from screen import win

building_types = {"mother": {"size": 20, "color": (0, 0, 255), "symbol": "M", "charge_time": 5, "health": 100, "cost": 100, "range": None},
                    "base": {"size": 20, "color": (0, 255, 0), "symbol": "B", "charge_time": None, "health": 100, "cost": 100, "range": None}
                    }


class Buildings:
    def __init__(self):
        self.building_list = []

    def draw(self):
        for building in self.building_list:
            building.draw()

    def add_building(self, building_type, ground, x):
        y = ground.segments[x // ground.segment_width].y - building_types[building_type]["size"]
        x = x - (x % ground.segment_width)
        for building in self.building_list:
            if building.x - building_types[building_type]["size"] < x < building.x + building.size:
                return
        self.building_list.append(Building(building_type, ground, x, y))

    def time(self, goo):
        for building in self.building_list:
            building.time(goo)


class Building:
    def __init__(self, building_type, ground, x, y):
        self.building_type = building_type
        self.size = building_types[self.building_type]["size"]
        self.charge_time = building_types[self.building_type]["charge_time"]
        self.current_charge = 0
        self.health = building_types[self.building_type]["health"]
        self.cost = building_types[self.building_type]["cost"]
        self.range = building_types[self.building_type]["range"]
        self.color = building_types[self.building_type]["color"]
        self.symbol = building_types[self.building_type]["symbol"]
        self.x = x
        self.y = y
        self.active = False

    def draw(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size), 2)
        # TODO add symbol

    def time(self, goo):
        if self.charge_time is not None:
            if self.current_charge < self.charge_time:
                self.current_charge += 1
                # print("{} will activate in{}".format(self.building_type, self.charge_time - self.current_charge))
            else:
                self.current_charge = 0
                self.activate(goo)

    def activate(self, goo):
        if self.building_type == "mother":
            goo.more_goo(self.x + self.size // 2, self.y - self.size // 2)


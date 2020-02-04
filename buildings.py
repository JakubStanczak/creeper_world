import pygame
from screen import win

building_types = {"mother": {"size": 20, "color": (0, 0, 255), "symbol": "M", "charge_time": 5, "health": 100, "cost": 100, "energy": 0, "range": None},
                  "base": {"size": 20, "color": (0, 255, 0), "symbol": "BB", "charge_time": None, "health": 100, "cost": 100, "energy": 20, "range": None},
                  "barracks": {"size": 10, "color": (0, 255, 0), "symbol": "B", "charge_time": 50, "health": 100, "cost": 100, "energy": -10, "range": None},
                  # "infantry": {"size": 5, "color": (0, 255, 0), "symbol": "I", "charge_time": 10, "health": 1, "cost": None, "energy": 20, "range": 2},
                  "aircraft_base": {"size": 10, "color": (0, 255, 0), "symbol": "A", "charge_time": 100, "health": 100, "cost": 100, "energy": -20, "range": None},
                  "gun": {"size": 10, "color": (0, 255, 0), "symbol": "G", "charge_time": 10, "health": 100, "cost": 100, "energy": -10, "range": 5},
                  "plant": {"size": 10, "color": (0, 255, 0), "symbol": "P", "charge_time": 100, "health": 100, "cost": 100, "energy": 20, "range": 5}
                    }


class Buildings:
    def __init__(self):
        self.building_list = []
        self.energy_balance = 0

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

    def time(self, ground, goo, weapons):
        self.update_energy_balance()
        for building in self.building_list:
            building.time(ground, goo, weapons, self.building_list)

    def update_energy_balance(self):
        energy_balance = 0
        for building in self.building_list:
            energy_balance += building.energy
        self.energy_balance = energy_balance


class Building:
    def __init__(self, building_type, ground, x, y):
        self.building_type = building_type
        if building_type == "tunnel":
            self.size = ground.segment_width
        else:
            self.size = building_types[self.building_type]["size"]
        self.charge_time = building_types[self.building_type]["charge_time"]
        self.current_charge = 0
        self.health = building_types[self.building_type]["health"]
        self.cost = building_types[self.building_type]["cost"]
        self.range = building_types[self.building_type]["range"]
        self.color = building_types[self.building_type]["color"]
        self.symbol = building_types[self.building_type]["symbol"]
        self.energy = building_types[self.building_type]["energy"]
        self.x = x
        self.y = y

        self.active = False
        self.child = None

    def draw(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size), 2)
        # TODO add symbol

    def time(self, ground, goo, weapons, building_list):
        if self.charge_time is not None:
            if self.current_charge < self.charge_time:
                self.current_charge += 1
                # print("{} will activate in{}".format(self.building_type, self.charge_time - self.current_charge))
            else:
                self.current_charge = 0
                self.activate(ground, goo, weapons, building_list)

    def activate(self, ground, goo, weapons, building_list):
        if self.building_type == "mother":
            goo.more_goo(self.x + self.size // 2, self.y - self.size // 2)

        if self.range is not None:
            x_idx = self.x // goo.pix_width
            y_inx = self.y // goo.pix_height
            for x_range in range(x_idx + self.range, x_idx - self.range, -1):
                for y_range in range(y_inx - self.range, y_inx + self.range):
                    if goo.goo_grid[x_range][y_range] is not None:
                        weapons.add_weapon("bullet", x_range * goo.pix_width + goo.pix_width // 2, y_range * goo.pix_height + goo.pix_height // 2)
                        return

        # if self.building_type == "barracks" and self.child is None:
        #     self.child = Building("infantry", ground, self.x, self.y + self.size - building_types["infantry"]["size"])
        #     building_list.append(self.child)


        # if self.building_type == "infantry":
        #     x_idx = self.x // goo.pix_width
        #     y_inx = self.y // goo.pix_height
        #     for x_range in range(x_idx + self.range, x_idx - self.range, -1):
        #         for y_range in range(y_inx - self.range, y_inx + self.range):
        #             if goo.goo_grid[x_range][y_range] is not None:
        #                 weapons.add_weapon("bullet", x_range * goo.pix_width + goo.pix_width // 2, y_range * goo.pix_height + goo.pix_height // 2)
        #                 return
        #     self.x -= 2
        #     self.y = ground.segments[x_idx].y - self.size


class Tunnel:
    def __init__(self, x, y, num):
        pass


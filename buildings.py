import pygame
from screen import win

building_types = {"mother": {"size": 20, "color": (0, 0, 255), "symbol": "M", "charge_time": 5, "health": 100, "cost": 100, "energy": 0, "range": None},
                  "base": {"size": 20, "color": (0, 255, 0), "symbol": "BB", "charge_time": None, "health": 100, "cost": 100, "energy": 20, "range": None},
                  "barracks": {"size": 10, "color": (0, 255, 0), "symbol": "B", "charge_time": 50, "health": 100, "cost": 100, "energy": -10, "range": None},
                  "aircraft_base": {"size": 10, "color": (0, 255, 0), "symbol": "A", "charge_time": 100, "health": 100, "cost": 100, "energy": -20, "range": None},
                  "gun": {"size": 10, "color": (0, 255, 0), "symbol": "G", "charge_time": 10, "health": 100, "cost": 100, "energy": -10, "range": 5},
                  "plant": {"size": 10, "color": (0, 255, 0), "symbol": "P", "charge_time": 100, "health": 100, "cost": 100, "energy": 20, "range": None}
                    }

unit_types = {"infantry": {"width": 2, "height": 5, "movement_speed": 2, "color": (0, 0, 255), "symbol": "I", "charge_time": 10, "health": 1, "range": 2},
              "plane": {"width": 10, "height": 5, "movement_speed": 5,  "color": (0, 0, 255), "symbol": "I", "charge_time": None, "health": None, "range": None}
              }


class Buildings:
    def __init__(self):
        self.building_list = []
        self.tunnel_grid = []
        self.energy_balance = 0
        self.mother = None
        self.base = None
        self.target = [0, 0]

    def draw(self):
        for building in self.building_list:
            building.draw()

    def add_building(self, building_type, ground, x):
        y = ground.segments[x // ground.segment_width].y - building_types[building_type]["size"]
        x = x - (x % ground.segment_width)
        for building in self.building_list:
            if building.x - building_types[building_type]["size"] < x < building.x + building.size:
                return
        if building_type == "mother":
            self.mother = Building("mother", x, y)
        elif building_type == "base":
            self.base = Building("base", x, y)
        self.building_list.append(Building(building_type, x, y))

    def time(self, ground, goo, weapons):
        self.update_energy_balance()
        for building in self.building_list:
            building.time(ground, goo, weapons)

    def update_energy_balance(self):
        energy_balance = 0
        for building in self.building_list:
            energy_balance += building.energy
        self.energy_balance = energy_balance

class Building:
    def __init__(self, building_type, x, y):
        self.building_type = building_type
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
        self.unit = None
        self.symbol_color = (0, 0, 0)
        self.symbol_font = pygame.font.SysFont("calibri", 10, bold=True)

    def draw(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size), 2)
        rendered_symbol = self.symbol_font.render(str(self.symbol), True, self.symbol_color)
        win.blit(rendered_symbol, (self.x, self.y))
        if self.unit is not None:
            self.unit.draw()


    def time(self, ground, goo, weapons):
        if self.charge_time is not None:
            if self.current_charge < self.charge_time:
                self.current_charge += 1
                # print("{} will activate in{}".format(self.building_type, self.charge_time - self.current_charge))
            else:
                self.current_charge = 0
                self.activate(goo, weapons)

        if self.unit is not None:
            self.unit.time(ground, goo, weapons)

    def activate(self, goo, weapons):
        if self.building_type == "mother":
            goo.more_goo(self.x + self.size // 2, self.y - self.size // 2)
        elif self.building_type == "barracks":
            if self.unit is None:
                self.unit = Unit("infantry", self.x, self.y + self.size - unit_types["infantry"]["height"], self)
        elif self.building_type == "aircraft_base":
            if self.unit is None and weapons.target is not None:
                self.unit = Unit("plane", self.x, self.y + self.size - unit_types["infantry"]["height"], self)
                self.unit.bomb_dropped = False
                self.unit.flight_alt = 20
                self.unit.target = weapons.target

        if self.range is not None:
            _ = shoot(weapons, goo, self.x, self.y, self.range)

    def unit_dead(self):
        self.unit = None

class Unit:
    def __init__(self, unit_type, x, y, mother_building):
        self.x = x
        self.y = y
        self.unit_type = unit_type
        self.mother_building = mother_building
        self.width = unit_types[self.unit_type]["width"]
        self.height = unit_types[self.unit_type]["height"]
        self.movement_speed = unit_types[self.unit_type]["movement_speed"]
        self.color = unit_types[self.unit_type]["color"]
        self.symbol = unit_types[self.unit_type]["symbol"]
        self.charge_time = unit_types[self.unit_type]["charge_time"]
        self.current_charge = 0
        self.health = unit_types[self.unit_type]["health"]
        self.range = unit_types[self.unit_type]["range"]

    def draw(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))


    def time(self, ground, goo, weapons):
        if self.charge_time is not None:
            if self.current_charge < self.charge_time:
                self.current_charge += 1
            else:
                self.current_charge = 0
                self.activate(ground, goo, weapons)

        #  TODO what if target is right from aircraft base
        if self.unit_type == "plane":
            if self.bomb_dropped is False:
                if self.y > self.flight_alt:
                    self.y -= self.movement_speed
                elif self.x > self.target[0]:
                    self.x -= self.movement_speed
                else:
                    weapons.add_weapon("bomb", self.target[0], self.flight_alt)
                    self.bomb_dropped = True
            else:
                if self.x < self.mother_building.x:
                    self.x += self.movement_speed
                elif self.y < self.mother_building.y:
                    self.y += self.movement_speed
                else:
                    self.mother_building.unit_dead()


    def activate(self, ground, goo, weapons):
        if self.unit_type == "infantry":
            if_shot = shoot(weapons, goo, self.x, self.y, self.range)
            if not if_shot:
                self.x -= 2
                self.y = ground.segments[self.x // ground.segment_width].y - self.height


def shoot(weapons, goo, x, y, weapon_range):
    x_idx = x // goo.pix_width
    y_inx = y // goo.pix_height
    left_range_idx = x_idx - weapon_range
    right_range_idx = x_idx + weapon_range
    if left_range_idx < 0:
        left_range_idx = 0
    if right_range_idx > goo.grid_x_dim - 1:
        right_range_idx = goo.grid_x_dim - 1

    for x_range in range(right_range_idx, left_range_idx, -1):
        for y_range in range(y_inx - weapon_range, y_inx + weapon_range):
            if goo.goo_grid[x_range][y_range] is not None:
                weapons.add_weapon("bullet", x_range * goo.pix_width + goo.pix_width // 2, y_range * goo.pix_height + goo.pix_height // 2)
                return True
    return False


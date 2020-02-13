import pygame
from screen import win

building_types = {"mother": {"size": 20, "color": (0, 0, 255), "inactive_color": (0, 0, 255), "symbol": "M", "charge_time": 5, "health": 100, "cost": 0, "energy_usage": 0, "range": None},
                  "base": {"size": 20, "color": (0, 255, 0), "inactive_color": (0, 255, 0), "symbol": "BB", "charge_time": None, "health": 100, "cost": 0, "energy_usage": -20, "range": None},
                  "barracks": {"size": 10, "color": (0, 255, 0), "inactive_color": (255, 150, 0), "symbol": "B", "charge_time": 60, "health": 100, "cost": 1000, "energy_usage": 10, "range": None},
                  "aircraft_base": {"size": 10, "color": (0, 255, 0), "inactive_color": (255, 150, 0), "symbol": "A", "charge_time": 150, "health": 100, "cost": 1000, "energy_usage": 20, "range": None},
                  "gun": {"size": 10, "color": (0, 255, 0), "inactive_color": (255, 150, 0), "symbol": "G", "charge_time": 20, "health": 100, "cost": 1000, "energy_usage": 10, "range": 5},
                  "plant": {"size": 10, "color": (0, 255, 0), "inactive_color": (255, 150, 0), "symbol": "P", "charge_time": None, "health": 100, "cost": 3000, "energy_usage": -20, "range": None}
                    }

unit_types = {"infantry": {"width": 2, "height": 5, "movement_speed": 3, "color": (0, 0, 255), "symbol": "I", "charge_time": 30, "health": 1, "range": 3},
              "plane": {"width": 10, "height": 5, "movement_speed": 5,  "color": (0, 0, 255), "symbol": "I", "charge_time": None, "health": 5, "range": None}
              }

class Buildings:
    def __init__(self):
        self.building_list = []
        self.tunnel_grid = []
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
        new_building = Building(building_type, x, y)
        if building_type == "mother":
            self.mother = new_building
        elif building_type == "base":
            self.base = new_building
        self.building_list = self.building_list + [new_building]

    def time(self, ground, goo, weapons):
        for building in self.building_list:
            destroyed = building.check_damage(goo)
            if destroyed:
                self.building_destroyed(building)

        energy = self.produce_energy()
        # print("energy produced {}".format(energy))
        self.building_list.sort(key=lambda x: x.active)
        for building in reversed(self.building_list):
            if building.energy_usage > 0 or not building.active:
                if (building.active and energy >= building.energy_usage) or (not building.active and energy >= building.build_speed):
                    energy_used = building.time(ground, goo, weapons, self, True)
                    energy -= energy_used
                    # print("building {} used {} energy and there is {} left".format(building.building_type, energy_used, energy))
                else:
                    if building.active:
                        energy_needed = building.energy_usage - energy
                        energy_from_coal = self.get_energy_from_coal(ground, energy_needed)
                    else:
                        energy_needed = building.build_speed - energy
                        energy_from_coal = self.get_energy_from_coal(ground, energy_needed)
                    if energy_from_coal == energy_needed:
                        energy_used = building.time(ground, goo, weapons, self, True)
                        energy -= energy_used
                        # print("building {} used {} energy and there is {} left, {} was from coal".format(building.building_type, energy_used, energy, energy_from_coal))
                    else:
                        _ = building.time(ground, goo, weapons, self, False)
            else:
                _ = building.time(ground, goo, weapons, self, True)

    def produce_energy(self):
        energy_produced = 0
        for building in self.building_list:
            if building.active and building.energy_usage < 0:
                energy_produced += building.energy_usage
        energy_produced = abs(energy_produced)
        return energy_produced

    def get_energy_from_coal(self, ground, energy_needed):
        energy_gained = 0
        for coal in ground.coals:
            if coal.connected:
                if coal.current_quantity > 0:
                    if coal.current_quantity >= energy_needed:
                        energy_gained += energy_needed
                        coal.current_quantity -= energy_needed
                        energy_needed = 0
                    else:
                        energy_needed -= coal.current_quantity
                        energy_gained += coal.current_quantity
                        coal.current_quantity = 0
        return energy_gained

    def building_destroyed(self, building):
        building.unit = None
        if building.building_type == "mother":
            self.mother = None
        if building.building_type == "base":
            self.base = None
        self.building_list.pop(self.building_list.index(building))

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
        self.inactive_color = building_types[self.building_type]["inactive_color"]
        self.symbol = building_types[self.building_type]["symbol"]
        self.energy_usage = building_types[self.building_type]["energy_usage"]
        self.x = x
        self.y = y
        self.build_speed = 10
        self.active = False
        self.unit = None
        self.symbol_color = (0, 0, 0)
        self.symbol_font = pygame.font.SysFont("calibri", 10, bold=True)

    def draw(self):
        if self.active:
            color = self.color
        else:
            color = self.inactive_color
        pygame.draw.rect(win, color, (self.x, self.y, self.size, self.size), 2)
        rendered_symbol = self.symbol_font.render(str(self.symbol), True, self.symbol_color)
        win.blit(rendered_symbol, (self.x, self.y))
        if self.unit is not None:
            self.unit.draw()

        #  and health energy bar
        health_bar_color = (255, 0, 0)
        health_line_offset = 5
        energy_bar_color = (0, 0, 255)
        energy_bar_offset = 10
        if self.active:
            health_fraction = self.health / building_types[self.building_type]["health"]
            if self.charge_time is not None:
                energy_fraction = self.current_charge / self.charge_time
                energy_bar_len = self.size * energy_fraction
                pygame.draw.line(win, energy_bar_color, (self.x, self.y - energy_bar_offset), (self.x + energy_bar_len, self.y - energy_bar_offset))
        elif building_types[self.building_type]["cost"] != 0:
            health_fraction = (building_types[self.building_type]["cost"] - self.cost) / building_types[self.building_type]["cost"]
        else:
            health_fraction = 1
        health_bar_len = self.size * health_fraction
        pygame.draw.line(win, health_bar_color, (self.x, self.y - health_line_offset), (self.x + health_bar_len, self.y - health_line_offset))

    def time(self, ground, goo, weapons, buildings, enough_energy):
        if self.unit is not None:
            self.unit.time(ground, goo, weapons, buildings)

        if enough_energy:
            if self.active:
                if self.charge_time is not None:
                    if self.current_charge < self.charge_time:
                        self.current_charge += 1
                        return self.energy_usage
                    else:
                        activated = self.activate(goo, weapons, buildings)
                        if activated:
                            self.current_charge = 0
            else:
                self.cost -= self.build_speed
                if self.cost <= 0:
                    self.active = True
                return self.build_speed
        return 0

    def activate(self, goo, weapons, buildings):
        if self.building_type == "mother":
            goo.more_goo(self.x + self.size // 2, self.y - self.size // 2)
            return True
        elif self.building_type == "barracks":
            if self.unit is None:
                self.unit = Unit("infantry", self.x, self.y + self.size - unit_types["infantry"]["height"], self)
                return True
        elif self.building_type == "aircraft_base":
            if self.unit is None and weapons.target is not None:
                self.unit = Unit("plane", self.x, self.y + self.size - unit_types["infantry"]["height"], self)
                self.unit.bomb_dropped = False
                self.unit.flight_alt = 20
                self.unit.target = weapons.target
                return True

        if self.range is not None:
            if_shot = shoot(goo, weapons, buildings, self.x, self.y, self.range)
            if if_shot:
                return True
        return False

    def check_damage(self, goo):

        if self.building_type != "mother":
            x_idx = (self.x + 1) // goo.pix_width
            y_idx = (self.y + self.size - 1) // goo.pix_height

            if goo.goo_grid[x_idx][y_idx] is not None:
                self.health -= 1
                print("building taking damage")

            if self.unit is not None:
                unit_x_idx = (self.unit.x + 1) // goo.pix_width
                unit_y_idx = (self.unit.y + self.unit.height - 1) // goo.pix_height
                if goo.goo_grid[unit_x_idx][unit_y_idx] is not None:
                    print("unit taking damage")
                    self.unit.health -= 1
                if self.unit.health <= 0:
                    self.unit = None
        if self.health <= 0:
            return True
        else:
            return False

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

    def time(self, ground, goo, weapons, buildings):
        if self.charge_time is not None:
            if self.current_charge < self.charge_time:
                self.current_charge += 1
            else:
                self.current_charge = 0
                self.activate(ground, goo, weapons, buildings)

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

    def activate(self, ground, goo, weapons, buildings):
        if self.unit_type == "infantry":
            if_shot = shoot(goo, weapons, buildings, self.x, self.y, self.range)
            if not if_shot:
                self.x -= self.movement_speed
                self.y = ground.segments[self.x // ground.segment_width].y - self.height


def shoot(goo, weapons, buildings, x, y, weapon_range):
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
                if not goo.goo_grid[x_range][y_range].targeted:
                    goo.goo_grid[x_range][y_range].targeted = True
                    weapons.add_weapon("bullet", x_range * goo.pix_width + goo.pix_width // 2, y_range * goo.pix_height + goo.pix_height // 2)
                    return True

    if buildings.mother is not None:
        if buildings.mother.x + buildings.mother.size > x - weapon_range * goo.pix_width:
            weapons.add_weapon("bullet", buildings.mother.x + buildings.mother.size, buildings.mother.y + buildings.mother.size // 2)
            buildings.mother.health -= 2
            return True
    return False



building_types = {"Mother": {"charge_time": 120, "health": 20, "cost": 100}}


class Building:
    dim = 50
    def __init__(self, building_type, map_ground, x_idx):
        self.charge_time = building_types[building_type]["charge_time"]
        self.x = map_ground.segments[x_idx].x

from .bpb import Point, colors, CITI_LEVEL
from .SpriteCity import SpriteCity

class Hex:
    def __init__(self, q, r, s) -> None:
        self._q = q
        self._r = r
        self._s = s
        assert self._q + self._r + self._s == 0        
        
        self.owner = None
        self.center = None
        self.color = colors["SANDISH"]
        self.border_color = (0, 0, 0)
        self.unit = None
        self.neighbor_list = []
        self.hex_directions = [
        (1, 0, -1), 
        (1, -1, 0), 
        (0, -1, 1), 
        (-1, 0, 1), 
        (-1, 1, 0), 
        (0, 1, -1)
        ]
        for direction in self.hex_directions:
            self.neighbor_list.append(self.hex_add(direction))


    def hex_add(self, other):
        return (self._q + other[0], self._r + other[1], self._s + other[2])

    def hex_sub(self, other):
        return Hex(self._q - other._q, self._r - other._r, self._s - other._s)
    
    def hex_direction(self, direction):
        assert 0 <= direction < 6, "Invalid direction"
        return Hex.hex_directions[direction]

    def hex_ret_coords(self):
        return (self._q, self._r, self._s)

    def set_hex_center(self, p: Point):
        self.center = p

    def switch_color(self, col):
        self.color = col

    def add_unit(self, unit):
        self.unit = unit

    def remove_unit(self):
        self.unit.rm_unit()
        self.unit = None

    def set_owner(self, player):
        self.owner = player
        self.border_color = self.owner.color
        
    def __eq__(self, other) -> bool:
        if isinstance(other, Hex):
            return self._q == other._q and self._r == other._r and self._s == other._s
        return False
    
    def __hash__(self):
        return hash((self._q, self._r, self._s))
    
    def __repr__(self) -> str:
        return f"Hex(q={self._q}, r={self._r}, s={self._s}, cent={self.center})"
    
def hex_round(h):
    q,r,s = h
    qi = int(round(q))
    ri = int(round(r))
    si = int(round(s))
    q_diff = abs(qi - q)
    r_diff = abs(ri - r)
    s_diff = abs(si - s)
    if q_diff > r_diff and q_diff > s_diff:
        qi = -ri - si
    elif r_diff > s_diff:
        ri = -qi - si
    else:
        si = -qi - ri
    return (qi, ri, si)


class City(Hex):
    def __init__(self, q, r, s, city_sprite,city_name, color, owner) -> None:
        super().__init__(q, r, s)
        self.city_sprite = city_sprite
        self.border_color = color
        self.city_name = city_name
        self.set_owner(owner)

        self.max_hp = 40
        self.hp = 40
        self.money = 100
        self.resources = 10

        self.is_destroyed = False


    def draw(self, screen):
        self.city_sprite.draw_city(screen)

    def draw_info(self, screen):
        self.city_sprite.draw_city_info(screen, self.max_hp, self.hp, self.city_name, self.border_color)


    def update_city_sprite(self):
        hp_percent = (self.hp / self.max_hp) * 100
        if 50 < hp_percent <= 75:
            self.city_sprite = SpriteCity(self.center, CITI_LEVEL[2])
        elif 25 < hp_percent <= 50:
            self.city_sprite = SpriteCity(self.center, CITI_LEVEL[3])
        elif 0 < hp_percent <= 25:
            self.city_sprite = SpriteCity(self.center, CITI_LEVEL[4])
        elif hp_percent <= 0:
            self.city_sprite = SpriteCity(self.center, CITI_LEVEL[5])

    def deploy_unit(self, screen):
        pass



class Wonder(Hex):
    def __init__(self, q, r, s, wonder_sprite, wonder_name) -> None:
        super().__init__(q, r, s)
        self.wonder_sprite = wonder_sprite
        self.wonder_name = wonder_name

    def draw(self, screen):
        self.wonder_sprite.draw_wonder_sprite(screen)

    def draw_info(self, screen):
        self.wonder_sprite.draw_wonder_info(screen, self.wonder_name)
#             _____
#            /     \
#           /       \
#     ,----<    #3   >----.
#    /      \       /      \
#   /        \_____/        \
#   \   #4   /  q  \   #2   /
#    \      /       \      /
#     >----<         >----<
#    /      \ s   r /  +1  \
#   /        \_____/        \
#   \   #5   /     \   #1   /
#    \      /       \-1   0/
#     `----<   #6    >----'
#           \       /
#            \_____/
# 
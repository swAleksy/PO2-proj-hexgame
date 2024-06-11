from .bpb import Point, colors
import pygame

class Hex:
    hex_directions = [
        (1, 0, -1), 
        (1, -1, 0), 
        (0, -1, 1), 
        (-1, 0, 1), 
        (-1, 1, 0), 
        (0, 1, -1)
    ]
    
    def __init__(self, q, r, s) -> None:
        self._q = q
        self._r = r
        self._s = s
        assert self._q + self._r + self._s == 0
        
        self.center = None
        self.color = colors["SANDISH"]

        self.unit = None

    def hex_add(self, other):
        return Hex(self._q + other._q, self._r + other._r, self._s + other._s)

    def hex_sub(self, other):
        return Hex(self._q - other._q, self._r - other._r, self._s - other._s)
    
    def hex_direction(self, direction):
        assert 0 <= direction < 6, "Invalid direction"
        return Hex.hex_directions[direction]

    def hex_neighbor(self, direction):
        return self.hex_add(self.hex_direction(direction))

    def set_hex_center(self, p: Point):
        self.center = p

    def switch_color(self, col):
        self.color = col

    def add_unit(self, unit):
        self.unit = unit

    def remove_unit(self):
        self.unit = None

    def __eq__(self, other) -> bool:
        if isinstance(other, Hex):
            return self._q == other._q and self._r == other._r and self._s == other._s
        return False
    
    def __hash__(self):
        return hash((self._q, self._r, self._s))
    
    def __repr__(self) -> str:
        return f"Hex(q={self._q}, r={self._r}, s={self._s})"
    
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
    def __init__(self, q, r, s, city_sprite,city_name, color, unit) -> None:
        super().__init__(q, r, s)
        self.city_sprite = city_sprite
        self.border_color = color
        self.city_name = city_name

        self.max_hp = 100
        self.hp = 100
        self.money = 100
        self.resources = 10

        self.add_unit(unit)

        self.is_destroyed = False


    def draw_city(self, screen):
        self.city_sprite.draw_city(screen)
        self.city_sprite.draw_city_info(screen, self.max_hp, self.hp, self.city_name)

    def deploy_unit(self, screen):
        pass


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
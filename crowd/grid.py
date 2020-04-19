
import numpy as np
from collections import defaultdict, namedtuple

Coord = namedtuple('Coord', ('x', 'y'), defaults=(0,0))

class Grid:
    def __init__(self, width:int, height:int, wrap:bool =True, oob:str = 'block'):
        self.width = width
        self.height = height
        self._wrap = wrap

        if not wrap and oob not in ('block', 'die', 'bounce'):
            raise ValueError("oob must be one of 'block', 'bounce', or 'die'")
        self.oob = oob

        # accesses to grid are self.grid[x][y], so we actually index columns first
        self.grid = defaultdict(lambda: defaultdict(list))

    def wrap(self, coord:Coord) -> Coord:
        if not self._wrap: return coord

        if coord.x >= self.width: coord.x -= self.width
        elif coord.x < 0: coord.x += self.width

        if coord.y >= self.width: coord.y -= self.width
        elif coord.y < 0: coord.y += self.width

        return coord

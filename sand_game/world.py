"""
The simulation. A grid of element ids updated one cell at a time.

Design notes:
  * Grid is a Python list-of-lists of ints (faster per-cell access than numpy
    scalar indexing in a hot Python loop). A numpy view is built only for
    rendering, in main.py.
  * Each frame we scan rows bottom->top so falling material settles in one
    pass without teleporting. Horizontal scan direction flips randomly to
    avoid a left/right drift bias.
  * `_moved` marks cells already handled this frame so nothing moves twice.
  * Movement is density-driven: a cell sinks into / rises through any FLUID
    cell whose density is on the wrong side of its own.
"""

import random

from elements import (
    ACID, ACID_EATS, DENSITY, EMPTY, FIRE, FLUID, GASES, GUNPOWDER, ICE,
    LAVA, LIQUIDS, OIL, PLANT, POWDERS, SMOKE, STEAM, STONE, WATER, WOOD,
)

NB4 = ((-1, 0), (1, 0), (0, -1), (0, 1))


class World:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.cells = [[EMPTY] * w for _ in range(h)]
        self.life = [[0] * w for _ in range(h)]
        self._moved = [[False] * w for _ in range(h)]
        self.frame = 0

    # -- editing -----------------------------------------------------------
    def clear(self):
        for y in range(self.h):
            row = self.cells[y]
            lrow = self.life[y]
            for x in range(self.w):
                row[x] = EMPTY
                lrow[x] = 0

    def paint(self, gx, gy, radius, element):
        c, li, h, w = self.cells, self.life, self.h, self.w
        r2 = radius * radius
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx * dx + dy * dy > r2:
                    continue
                ny, nx = gy + dy, gx + dx
                if 0 <= ny < h and 0 <= nx < w:
                    c[ny][nx] = element
                    li[ny][nx] = self._fresh_life(element)

    @staticmethod
    def _fresh_life(element):
        if element == FIRE:
            return random.randint(45, 95)
        if element == STEAM:
            return random.randint(150, 280)
        if element == SMOKE:
            return random.randint(60, 140)
        return 0

    # -- main update -------------------------------------------------------
    def step(self):
        self.frame += 1
        w, h = self.w, self.h
        c = self.cells
        self._moved = [[False] * w for _ in range(h)]
        moved = self._moved
        for y in range(h - 1, -1, -1):
            xs = range(w) if random.random() < 0.5 else range(w - 1, -1, -1)
            mrow = moved[y]
            crow = c[y]
            for x in xs:
                if mrow[x]:
                    continue
                e = crow[x]
                if e == EMPTY or e == STONE:
                    continue

                # ---- reactions (may transform this cell / neighbors) ----
                if e == FIRE:
                    if self._fire(y, x):
                        continue
                elif e == LAVA:
                    if self._lava(y, x):
                        continue
                elif e == ACID:
                    if self._acid(y, x):
                        continue
                elif e == WOOD:
                    continue  # static; ignition handled by fire/lava
                elif e == PLANT:
                    self._plant(y, x)
                    continue
                elif e == ICE:
                    self._ice(y, x)
                    continue
                elif e == STEAM:
                    if self._steam(y, x):
                        continue
                elif e == SMOKE:
                    if self._smoke(y, x):
                        continue
                elif e == GUNPOWDER:
                    if self._gunpowder(y, x):
                        continue

                # ---- movement ----
                if e in POWDERS:
                    self._fall_powder(e, y, x)
                elif e in LIQUIDS:
                    self._fall_liquid(e, y, x)
                elif e in GASES:
                    self._rise(e, y, x)

    # -- movement primitives ----------------------------------------------
    def _swap(self, y1, x1, y2, x2):
        c, li = self.cells, self.life
        c[y1][x1], c[y2][x2] = c[y2][x2], c[y1][x1]
        li[y1][x1], li[y2][x2] = li[y2][x2], li[y1][x1]
        self._moved[y2][x2] = True

    def _fall_powder(self, e, y, x):
        c, h, w, de = self.cells, self.h, self.w, DENSITY[e]
        ny = y + 1
        if ny >= h:
            return
        t = c[ny][x]
        if t == EMPTY or (t in FLUID and DENSITY[t] < de):
            self._swap(y, x, ny, x)
            return
        order = (x - 1, x + 1) if random.random() < 0.5 else (x + 1, x - 1)
        for nx in order:
            if 0 <= nx < w:
                t = c[ny][nx]
                if t == EMPTY or (t in FLUID and DENSITY[t] < de):
                    self._swap(y, x, ny, nx)
                    return

    def _fall_liquid(self, e, y, x):
        c, h, w, de = self.cells, self.h, self.w, DENSITY[e]
        ny = y + 1
        if ny < h:
            t = c[ny][x]
            if t == EMPTY or (t in FLUID and DENSITY[t] < de):
                self._swap(y, x, ny, x)
                return
            order = (x - 1, x + 1) if random.random() < 0.5 else (x + 1, x - 1)
            for nx in order:
                if 0 <= nx < w:
                    t = c[ny][nx]
                    if t == EMPTY or (t in FLUID and DENSITY[t] < de):
                        self._swap(y, x, ny, nx)
                        return
        # horizontal flow into open space
        order = (x - 1, x + 1) if random.random() < 0.5 else (x + 1, x - 1)
        for nx in order:
            if 0 <= nx < w and c[y][nx] == EMPTY:
                self._swap(y, x, y, nx)
                return

    def _rise(self, e, y, x):
        c, w, de = self.cells, self.w, DENSITY[e]
        ny = y - 1
        if ny >= 0:
            t = c[ny][x]
            if t == EMPTY or (t in FLUID and DENSITY[t] > de):
                self._swap(y, x, ny, x)
                return
            order = (x - 1, x + 1) if random.random() < 0.5 else (x + 1, x - 1)
            for nx in order:
                if 0 <= nx < w:
                    t = c[ny][nx]
                    if t == EMPTY or (t in FLUID and DENSITY[t] > de):
                        self._swap(y, x, ny, nx)
                        return
        if random.random() < 0.4:  # lazy sideways drift
            order = (x - 1, x + 1) if random.random() < 0.5 else (x + 1, x - 1)
            for nx in order:
                if 0 <= nx < w and c[y][nx] == EMPTY:
                    self._swap(y, x, y, nx)
                    return

    # -- reactions ---------------------------------------------------------
    def _fire(self, y, x):
        c, li, h, w = self.cells, self.life, self.h, self.w
        li[y][x] -= 1
        doused = False
        for dy, dx in NB4:
            ny, nx = y + dy, x + dx
            if not (0 <= ny < h and 0 <= nx < w):
                continue
            t = c[ny][nx]
            if t == WOOD or t == PLANT:
                if random.random() < 0.35:
                    c[ny][nx] = FIRE
                    li[ny][nx] = random.randint(40, 90)
                    self._moved[ny][nx] = True
            elif t == OIL:
                c[ny][nx] = FIRE
                li[ny][nx] = random.randint(30, 70)
                self._moved[ny][nx] = True
            elif t == WATER:
                if random.random() < 0.25:
                    c[ny][nx] = STEAM
                    li[ny][nx] = random.randint(150, 280)
                    self._moved[ny][nx] = True
                doused = True
            elif t == ICE:
                c[ny][nx] = WATER
                self._moved[ny][nx] = True
        if doused or li[y][x] <= 0:
            if not doused and random.random() < 0.5:
                c[y][x] = SMOKE
                li[y][x] = random.randint(50, 120)
            else:
                c[y][x] = EMPTY
                li[y][x] = 0
            return True
        return False

    def _lava(self, y, x):
        c, li, h, w = self.cells, self.life, self.h, self.w
        solidify = False
        for dy, dx in NB4:
            ny, nx = y + dy, x + dx
            if not (0 <= ny < h and 0 <= nx < w):
                continue
            t = c[ny][nx]
            if t == WATER:
                c[ny][nx] = STEAM
                li[ny][nx] = random.randint(150, 280)
                self._moved[ny][nx] = True
                solidify = True
            elif t == ICE:
                c[ny][nx] = WATER
                self._moved[ny][nx] = True
                solidify = True
            elif t == WOOD or t == PLANT:
                if random.random() < 0.5:
                    c[ny][nx] = FIRE
                    li[ny][nx] = random.randint(40, 90)
                    self._moved[ny][nx] = True
            elif t == OIL:
                c[ny][nx] = FIRE
                li[ny][nx] = random.randint(30, 70)
                self._moved[ny][nx] = True
            elif t == GUNPOWDER:
                self._explode(ny, nx)
        if solidify:
            c[y][x] = STONE
            li[y][x] = 0
            return True
        if y - 1 >= 0 and c[y - 1][x] == EMPTY and random.random() < 0.03:
            c[y - 1][x] = FIRE
            li[y - 1][x] = random.randint(15, 35)
            self._moved[y - 1][x] = True
        return False

    def _acid(self, y, x):
        c, h, w = self.cells, self.h, self.w
        for dy, dx in NB4:
            ny, nx = y + dy, x + dx
            if not (0 <= ny < h and 0 <= nx < w):
                continue
            if c[ny][nx] in ACID_EATS and random.random() < 0.18:
                c[ny][nx] = EMPTY
                self._moved[ny][nx] = True
                if random.random() < 0.45:  # acid is consumed as it eats
                    c[y][x] = EMPTY
                    self.life[y][x] = 0
                    return True
        return False

    def _plant(self, y, x):
        if random.random() > 0.06:
            return
        c, h, w = self.cells, self.h, self.w
        waters, empties = [], []
        for dy, dx in NB4:
            ny, nx = y + dy, x + dx
            if not (0 <= ny < h and 0 <= nx < w):
                continue
            t = c[ny][nx]
            if t == WATER:
                waters.append((ny, nx))
            elif t == EMPTY:
                empties.append((ny, nx))
        if waters and empties:
            ey, ex = random.choice(empties)
            c[ey][ex] = PLANT
            self._moved[ey][ex] = True
            wy, wx = random.choice(waters)  # plant drinks the water to grow
            c[wy][wx] = EMPTY
            self._moved[wy][wx] = True

    def _ice(self, y, x):
        c, h, w = self.cells, self.h, self.w
        for dy, dx in NB4:
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and c[ny][nx] in (FIRE, LAVA):
                c[y][x] = WATER
                self.life[y][x] = 0
                return
        if random.random() < 0.01:  # slowly freeze touching water
            for dy, dx in NB4:
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w and c[ny][nx] == WATER:
                    c[ny][nx] = ICE
                    self._moved[ny][nx] = True
                    break

    def _steam(self, y, x):
        li = self.life
        li[y][x] -= 1
        if li[y][x] <= 0 or random.random() < 0.003:
            self.cells[y][x] = WATER
            li[y][x] = 0
            return True
        return False

    def _smoke(self, y, x):
        li = self.life
        li[y][x] -= 1
        if li[y][x] <= 0:
            self.cells[y][x] = EMPTY
            li[y][x] = 0
            return True
        return False

    def _gunpowder(self, y, x):
        c, h, w = self.cells, self.h, self.w
        for dy, dx in NB4:
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and c[ny][nx] in (FIRE, LAVA):
                self._explode(y, x)
                return True
        return False

    def _explode(self, cy, cx, radius=4):
        c, li, h, w = self.cells, self.life, self.h, self.w
        r2 = radius * radius
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dy * dy + dx * dx > r2:
                    continue
                ny, nx = cy + dy, cx + dx
                if not (0 <= ny < h and 0 <= nx < w):
                    continue
                t = c[ny][nx]
                if t == STONE:
                    continue
                if t == WATER:
                    c[ny][nx] = STEAM
                    li[ny][nx] = random.randint(120, 220)
                else:
                    c[ny][nx] = FIRE
                    li[ny][nx] = random.randint(15, 40)
                self._moved[ny][nx] = True

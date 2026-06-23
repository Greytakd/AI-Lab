"""
Element registry for the falling-sand sandbox.

Each element is a small integer id. Physical behavior is data-driven:
  - DENSITY decides who sinks/floats/rises through whom.
  - FLUID/LIQUIDS/GASES/POWDERS/STATIC group elements by how they move.
  - FLAMMABLE / ACID_EATS drive a few reactions.
The actual rules live in world.py; this file is just the "what exists" table.
"""

import numpy as np

# --- element ids -----------------------------------------------------------
EMPTY = 0
SAND = 1
WATER = 2
STONE = 3      # indestructible-ish wall (acid still eats it, nothing else)
WOOD = 4
FIRE = 5
OIL = 6
LAVA = 7
STEAM = 8
SMOKE = 9
ACID = 10
PLANT = 11
ICE = 12
GUNPOWDER = 13

N = 14

NAMES = [
    "Empty", "Sand", "Water", "Wall", "Wood", "Fire", "Oil",
    "Lava", "Steam", "Smoke", "Acid", "Plant", "Ice", "Gunpowder",
]

# --- rendering palette (base RGB per element) ------------------------------
PALETTE = np.array([
    (12, 12, 18),     # EMPTY  (background)
    (194, 178, 128),  # SAND
    (40, 110, 210),   # WATER
    (105, 105, 118),  # STONE
    (120, 78, 40),    # WOOD
    (255, 120, 24),   # FIRE
    (58, 48, 38),      # OIL
    (228, 78, 18),    # LAVA
    (205, 208, 218),  # STEAM
    (62, 62, 68),     # SMOKE
    (124, 222, 44),   # ACID
    (42, 162, 64),    # PLANT
    (164, 214, 238),  # ICE
    (48, 48, 54),     # GUNPOWDER
], dtype=np.uint8)

# --- physical properties ---------------------------------------------------
# Density: heavier sinks below lighter. Gases are negative (lighter than air).
# Statics use a huge value but are flagged STATIC so they never actually move.
_HEAVY = 9999
DENSITY = [
    0,        # EMPTY (air reference)
    150,      # SAND
    50,       # WATER
    _HEAVY,   # STONE
    _HEAVY,   # WOOD
    -5,       # FIRE  (rises)
    30,       # OIL   (floats on water)
    80,       # LAVA  (heaviest liquid)
    -10,      # STEAM (rises)
    -12,      # SMOKE (rises fastest)
    45,       # ACID  (just under water)
    _HEAVY,   # PLANT
    _HEAVY,   # ICE
    140,      # GUNPOWDER
]

POWDERS = frozenset({SAND, GUNPOWDER})
LIQUIDS = frozenset({WATER, OIL, ACID, LAVA})
GASES = frozenset({FIRE, STEAM, SMOKE})
STATIC = frozenset({STONE, WOOD, PLANT, ICE})
# Things a moving cell can swap through (it can flow/sink/rise into these):
FLUID = LIQUIDS | GASES

# Reaction sets
FLAMMABLE = frozenset({WOOD, OIL, PLANT})          # gunpowder handled separately
ACID_EATS = frozenset({SAND, WOOD, STONE, PLANT, ICE, GUNPOWDER})

# Order shown in the on-screen palette / used for click selection.
SELECTABLE = [
    SAND, WATER, STONE, WOOD, FIRE, OIL, LAVA,
    ACID, PLANT, ICE, GUNPOWDER, STEAM, SMOKE,
]

# Label shown on each palette swatch (its hotkey).
HOTKEY_LABEL = {
    SAND: "1", WATER: "2", STONE: "3", WOOD: "4", FIRE: "5", OIL: "6",
    LAVA: "7", ACID: "8", PLANT: "9", ICE: "0", GUNPOWDER: "G",
    STEAM: "V", SMOKE: "B",
}

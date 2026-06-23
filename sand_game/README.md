# Falling Sand — a sandbox

A little cellular-automaton sandbox. Paint elements with the mouse and watch
them fall, flow, burn, dissolve, freeze, and grow into each other.

## Run

```bash
uv run python sand_game/main.py
```

## Controls

| Input | Action |
|---|---|
| Left mouse (drag) | Paint the current element |
| Right mouse (drag) | Erase |
| Mouse wheel / `[` `]` | Brush size |
| Click a swatch (bottom bar) | Select element |
| `1`–`0`, `G`, `V`, `B` | Element hotkeys |
| `Space` | Pause / resume |
| `S` | Single-step (while paused) |
| `C` | Clear the world |
| `Esc` | Quit |

## The elements & how they behave

| Element | Behavior |
|---|---|
| **Sand** | Powder. Falls, piles in slopes, sinks through liquids. |
| **Water** | Liquid. Flows and finds its level. |
| **Wall** | Static. Doesn't move; blocks everything (but acid eats it). |
| **Wood** | Static, flammable — fire and lava set it alight. |
| **Fire** | Rises, flickers, burns out. Ignites wood/oil/plant, melts ice, turns water to steam, dies in water (sometimes leaving smoke). |
| **Oil** | Flammable liquid. **Lighter than water, so it floats** — try layering them. |
| **Lava** | Heavy glowing liquid. Ignites flammables; **water cools it into wall + steam**; melts ice. |
| **Steam** | Gas. Rises, then condenses back into water. |
| **Smoke** | Gas. Rises and fades away. |
| **Acid** | Liquid that dissolves sand, wood, wall, plant, ice — and is used up as it eats. |
| **Plant** | Static. **Grows into empty space when it touches water**, drinking the water to spread. Flammable. |
| **Ice** | Static. Melts near fire/lava; slowly freezes water it touches. |
| **Gunpowder** | Powder. **Explodes** on contact with fire or lava — chain reactions included. |

## Things worth trying

- Pour **water onto lava** to forge walls and belch steam.
- Float **oil on water**, then drop **fire** on top.
- Trap **gunpowder** in a wall box and poke it with a single fire pixel.
- Grow a **plant** along a thin stream of water, then burn the whole vine.
- Carve through a **wall** with a drip of **acid**.
- Freeze a **water** pool by seeding one **ice** pixel and waiting.

## Code layout

- `elements.py` — the element table: ids, colors, densities, behavior groups.
- `world.py` — the simulation (movement + reactions), framework-free.
- `main.py` — pygame rendering, HUD, and input.

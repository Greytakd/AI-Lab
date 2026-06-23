"""
Falling-sand sandbox — entry point. Renders the World with pygame and handles
mouse painting + keyboard controls.

Run:  uv run python sand_game/main.py
"""

import sys

import numpy as np
import pygame

from elements import (
    ACID, EMPTY, FIRE, GUNPOWDER, HOTKEY_LABEL, ICE, LAVA, NAMES, OIL,
    PALETTE, PLANT, SAND, SELECTABLE, SMOKE, STEAM, STONE, WATER, WOOD,
)
from world import World

GRID_W, GRID_H, CELL = 150, 100, 5
HUD_H = 66
SIM_W, SIM_H = GRID_W * CELL, GRID_H * CELL
WIN_W, WIN_H = SIM_W, SIM_H + HUD_H

KEYMAP = {
    pygame.K_1: SAND, pygame.K_2: WATER, pygame.K_3: STONE, pygame.K_4: WOOD,
    pygame.K_5: FIRE, pygame.K_6: OIL, pygame.K_7: LAVA, pygame.K_8: ACID,
    pygame.K_9: PLANT, pygame.K_0: ICE, pygame.K_g: GUNPOWDER,
    pygame.K_v: STEAM, pygame.K_b: SMOKE,
}


def build_swatches(font):
    n = len(SELECTABLE)
    sw = SIM_W // n
    rects = []
    for i, el in enumerate(SELECTABLE):
        rect = pygame.Rect(i * sw, SIM_H + 24, sw - 2, HUD_H - 26)
        rects.append((rect, el))
    return rects


def render_world(world, screen, flicker_rng):
    cells = np.asarray(world.cells, dtype=np.uint8)
    colors = PALETTE[cells].astype(np.int16)
    # static per-frame grain so flat surfaces aren't dead-flat
    colors += flicker_rng.integers(-12, 13, size=colors.shape, dtype=np.int16)
    # extra flicker for the glowy stuff
    for el, lo, hi in ((FIRE, -45, 75), (LAVA, -35, 45)):
        mask = cells == el
        cnt = int(mask.sum())
        if cnt:
            colors[mask] += flicker_rng.integers(lo, hi, size=(cnt, 3), dtype=np.int16)
    np.clip(colors, 0, 255, out=colors)
    arr = colors.astype(np.uint8).swapaxes(0, 1)  # (w, h, 3) for pygame
    surf = pygame.surfarray.make_surface(arr)
    surf = pygame.transform.scale(surf, (SIM_W, SIM_H))
    screen.blit(surf, (0, 0))


def render_hud(screen, font, swatches, current, brush, paused, fps):
    pygame.draw.rect(screen, (20, 20, 26), (0, SIM_H, WIN_W, HUD_H))
    status = (f"{NAMES[current]}   brush:{brush}   "
              f"{'PAUSED' if paused else 'running'}   {fps:>3} fps   "
              f"[LMB] paint  [RMB] erase  [wheel/ [ ]] brush  "
              f"[space] pause  [s] step  [c] clear  [esc] quit")
    screen.blit(font.render(status, True, (210, 210, 220)), (6, SIM_H + 4))
    for rect, el in swatches:
        screen.fill(tuple(int(v) for v in PALETTE[el]), rect)
        label = HOTKEY_LABEL.get(el, "")
        if label:
            txt = font.render(label, True, (12, 12, 14))
            screen.blit(txt, (rect.x + 3, rect.y + 2))
        if el == current:
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)


def main():
    pygame.init()
    pygame.display.set_caption("Falling Sand — sandbox")
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 13)
    flicker_rng = np.random.default_rng()

    world = World(GRID_W, GRID_H)
    swatches = build_swatches(font)
    current = SAND
    brush = 3
    paused = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_s and paused:
                    world.step()
                elif event.key == pygame.K_c:
                    world.clear()
                elif event.key == pygame.K_LEFTBRACKET:
                    brush = max(1, brush - 1)
                elif event.key == pygame.K_RIGHTBRACKET:
                    brush = min(24, brush + 1)
                elif event.key in KEYMAP:
                    current = KEYMAP[event.key]
            elif event.type == pygame.MOUSEWHEEL:
                brush = max(1, min(24, brush + event.y))
            elif event.type == pygame.MOUSEBUTTONDOWN and event.pos[1] >= SIM_H:
                for rect, el in swatches:
                    if rect.collidepoint(event.pos):
                        current = el
                        break

        # continuous painting while a button is held
        mx, my = pygame.mouse.get_pos()
        if my < SIM_H:
            buttons = pygame.mouse.get_pressed()
            if buttons[0]:
                world.paint(mx // CELL, my // CELL, brush, current)
            elif buttons[2]:
                world.paint(mx // CELL, my // CELL, brush, EMPTY)

        if not paused:
            world.step()

        render_world(world, screen, flicker_rng)
        render_hud(screen, font, swatches, current, brush, paused,
                   int(clock.get_fps()))
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()

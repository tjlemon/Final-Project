# ============================================================
# grid_logic.py — Grid Rendering & Disease Simulation Logic
# ============================================================

import pygame
from config import *
import random
import math


# -------------------------------------------------------------------
# Create initial empty grid (all susceptible)
# -------------------------------------------------------------------
def make_grid():
    return [[SUS for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]


# -------------------------------------------------------------------
# Draw the grid to the screen
# -------------------------------------------------------------------
def draw_grid(screen, grid, hospitals=None, quarantines=None):
    if hospitals is None:
        hospitals = []
    if quarantines is None:
        quarantines = []
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            x = c * CELL_SIZE
            y = r * CELL_SIZE

            state = grid[r][c]

            if state == SUS:
                color = COLOR_SUSCEPTIBLE
            elif state == INF:
                color = COLOR_INFECTED
            elif state == REC:
                color = COLOR_RECOVERED
            elif state == DED:
                color = COLOR_DEAD
            elif state == QUA:
                color = COLOR_QUARANTINE
            else:
                color = (255, 0, 255)

            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))

            # -----------------------------
            # HOSPITAL VISUAL (+ symbol)
            # -----------------------------
            if (r, c) in hospitals:
                cx = x + CELL_SIZE // 2
                cy = y + CELL_SIZE // 2
                pygame.draw.line(screen, WHITE, (cx - 6, cy), (cx + 6, cy), 2)
                pygame.draw.line(screen, WHITE, (cx, cy - 6), (cx, cy + 6), 2)
            # -----------------------------
            # HOSPITAL RADIUS OUTLINE
            # -----------------------------
            for (hr, hc) in hospitals:
                if abs(hr - r) <= 2 and abs(hc - c) <= 2:
                    # Only draw border ONCE per hospital, at the corner tile
                    if r == hr - 2 and c == hc - 2:
                        rect_x = (hc - 2) * CELL_SIZE
                        rect_y = (hr - 2) * CELL_SIZE
                        rect_w = CELL_SIZE * 5
                        rect_h = CELL_SIZE * 5
                        pygame.draw.rect(screen, (255, 255, 255), (rect_x, rect_y, rect_w, rect_h), 2)


            # -----------------------------
            # QUARANTINE VISUAL (3x3 box)
            # -----------------------------
            for (qr, qc) in quarantines:
                if abs(qr - r) <= 1 and abs(qc - c) <= 1:
                    # subtle yellow overlay
                    overlay = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                    overlay.fill((255, 255, 0, 180))  
                    screen.blit(overlay, (x, y))



def check_end_conditions(grid):
    has_inf = any(INF in row for row in grid)
    has_susc = any(SUS in row for row in grid)

    if not has_inf:
        return "VICTORY! Infection eliminated."

    total_cells = len(grid) * len(grid[0])
    infected_count = sum(row.count(INF) for row in grid)

    if infected_count == total_cells:
        return "DEFEAT! Entire map infected."

    return None

# -------------------------------------------------------------------
# Count infected neighbors
# -------------------------------------------------------------------
def count_infected_neighbors(grid, r, c):
    neighbors = [
        (-1, 0), (1, 0), (0, -1), (0, 1),
        (-1, -1), (-1, 1), (1, -1), (1, 1)
    ]
    count = 0
    for dr, dc in neighbors:
        nr = r + dr
        nc = c + dc
        if 0 <= nr < GRID_ROWS and 0 <= nc < GRID_COLS:
            if grid[nr][nc] == INF:
                count += 1
    return count


# -------------------------------------------------------------------
# Hospital detection near a tile
# -------------------------------------------------------------------
def hospital_near(hospitals, r, c):
    for hr, hc in hospitals:
        if abs(hr - r) <= 2 and abs(hc - c) <= 2:
            return True
    return False


# -------------------------------------------------------------------
# Quarantine zone detection
# -------------------------------------------------------------------
def in_quarantine(qzones, r, c):
    for (qr, qc) in qzones:
        # quarantine = 3x3 area (
        if abs(qr - r) <= 1 and abs(qc - c) <= 1:
            return True
    return False


# -------------------------------------------------------------------
# MAIN SIMULATION: runs 1 day
# -------------------------------------------------------------------
def simulate_day(grid, difficulty_mult, hospitals, qzones):
    new_grid = [row[:] for row in grid]

    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            state = grid[r][c]

            # Dead stays dead
            if state == DED:
                continue

            # Quarantine stays a static zone
            if state == QUA:
                continue

            # Recovery from INF
            if state == INF:
                recover_rate = BASE_RECOVER_RATE
                death_rate = BASE_DEATH_RATE

                # Hospitals help nearby tiles
                if hospital_near(hospitals, r, c):
                    recover_rate += HOSPITAL_BOOST

                if random.random() < recover_rate:
                    new_grid[r][c] = REC
                    continue

                # Death check
                if random.random() < death_rate:
                    new_grid[r][c] = DED
                    continue

            # Infection spread (only if susceptible)
            if state == SUS:
                neighbors = count_infected_neighbors(grid, r, c)
                if neighbors > 0:

                    spread_rate = BASE_INFECT_RATE * difficulty_mult

                    # quarantine reduces spread
                    if in_quarantine(qzones, r, c):
                        spread_rate *= (1 - QUARANTINE_REDUCTION)

                    # multiple neighbors = more chance
                    spread_chance = 1 - (1 - spread_rate)**neighbors

                    if random.random() < spread_chance:
                        new_grid[r][c] = INF

    return new_grid

# ============================================================
# tools.py — Player Actions (Vaccine, Quarantine, Hospital)
# ============================================================

from config import *
import math


# -------------------------------------------------------------
# Apply Vaccine — converts infected → recovered, and
# boosts immunity in a radius.
# -------------------------------------------------------------
def place_vaccine(grid, r, c):

    for rr in range(GRID_ROWS):
        for cc in range(GRID_COLS):

            dx = (cc - c) * CELL_SIZE
            dy = (rr - r) * CELL_SIZE

            if math.sqrt(dx*dx + dy*dy) <= VACCINE_RADIUS:
                # Infecteds recover
                if grid[rr][cc] == INF:
                    grid[rr][cc] = REC
                # Susceptible turn immune
                elif grid[rr][cc] == SUS:
                    grid[rr][cc] = REC

    return grid


# -------------------------------------------------------------
# Place Quarantine — sets a 3×3 zone of QUA tiles
# -------------------------------------------------------------
def place_quarantine(qzones, r, c):
    """
    qzones stores the CENTER (r,c) of each quarantine zone.
    We do NOT change the grid tiles — grid_logic checks qzones.
    """
    qzones.append((r, c))


# -------------------------------------------------------------
# Place Hospital — adds a healing structure
# -------------------------------------------------------------
def place_hospital(grid, hospitals, r, c):
    """
    hospitals stores the tile of each hospital so simulate_day()
    can boost recovery around them.
    """
    hospitals.append((r, c))

    # Draw a visible plus symbol by marking the tile recovered
    if grid[r][c] != DED:
        grid[r][c] = REC

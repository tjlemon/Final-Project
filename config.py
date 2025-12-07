# ============================================================
# config.py — Global Settings & Game Constants
# ============================================================

# --- GRID SETTINGS ---
GRID_ROWS = 40
GRID_COLS = 60
CELL_SIZE = 15

# Screen dimensions
SCREEN_WIDTH = GRID_COLS * CELL_SIZE + 260  # 260 for sidebar
SCREEN_HEIGHT = GRID_ROWS * CELL_SIZE



# --- GAME STATE VALUES ---
SUS = 0   # susceptible
INF = 1   # infected
REC = 2   # recovered (immune)
DED = 3   # dead
QUA = 4   # quarantine zone

# Colors
COLOR_SUSCEPTIBLE = (60, 120, 255)
COLOR_INFECTED = (255, 60, 60)
COLOR_RECOVERED = (60, 220, 60)
COLOR_DEAD = (100, 100, 100)
COLOR_QUARANTINE = (255, 255, 0)

WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
GRAY   = (100, 100, 100)
LIGHT_GRAY = (170, 170, 170)
DARK_GRAY = (50, 50, 50)

RED    = (200, 40, 40)
GREEN  = (40, 200, 40)
BLUE   = (50, 100, 220)
YELLOW = (230, 230, 40)
ORANGE = (255, 165, 0)
PURPLE = (150, 50, 250)
CYAN   = (0, 200, 200)


# --- TURN SYSTEM ---
STARTING_ENERGY = 10
MAX_ENERGY = 40
ENERGY_REGEN = 10     # energy gained every turn (10 days)

# --- COSTS ---
COST_VACCINE = 25
COST_QUARANTINE = 10
COST_HOSPITAL = 15

# --- DIFFICULTY MULTIPLIERS ---
DIFFICULTY_LEVELS = {
    "Easy": 0.7,
    "Normal": 1.0,
    "Hard": 1.4
}

# --- SIMULATION RATES ---
BASE_INFECT_RATE = 0.18
BASE_RECOVER_RATE = 0.07
BASE_DEATH_RATE = 0.03

# Hospitals give local recovery boost
HOSPITAL_BOOST = 0.20

# Quarantine reduces spread
QUARANTINE_REDUCTION = 0.40

# Vaccine radius
VACCINE_RADIUS = 50


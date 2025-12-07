# ============================================================
# main.py — Pandemic Strategy Game (Main Engine)
# ============================================================

import pygame, sys, time
from config import *
from grid_logic import make_grid, draw_grid, simulate_day
from tools import place_vaccine, place_quarantine, place_hospital
from turn_menu import create_turn_buttons
from ui import draw_start_screen, draw_settings_screen, draw_stats, draw_turn_popup
import os

pygame.mixer.init()


# =============================
# LOAD SOUND EFFECTS
# =============================

SFX_VACCINE = pygame.mixer.Sound("sounds/vaccine.wav")
SFX_QUARANTINE = pygame.mixer.Sound("sounds/quarantine.wav")
SFX_HOSPITAL = pygame.mixer.Sound("sounds/hospital.wav")
SFX_CLICK = pygame.mixer.Sound("sounds/click.wav")
SFX_VICTORY = pygame.mixer.Sound("sounds/victory.wav")
SFX_DEFEAT = pygame.mixer.Sound("sounds/defeat.wav")

# =============================
# LOAD BACKGROUND MUSIC
# =============================
pygame.mixer.music.load("sounds/soundtrack.mp3")
pygame.mixer.music.set_volume(0.4)


HIGH_SCORE_FILE = "highscore.txt"

def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as f:
            return int(f.read().strip())
    return None

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))


# ------------------------------------------------------------
# Smooth animated grid transition for 10-day simulation
# ------------------------------------------------------------
def animate_simulation(screen, old_grid, new_grid, hospitals, quarantines):
    steps = 8
    for i in range(steps):
        # Linear reveal animation
        blend = [
            [new_grid[r][c] if i == steps-1 else old_grid[r][c]
             for c in range(GRID_COLS)]
            for r in range(GRID_ROWS)
        ]

        draw_grid(screen, blend, hospitals, quarantines)
        pygame.display.flip()
        pygame.time.delay(40)


# ------------------------------------------------------------
# MAIN GAME LOOP
# ------------------------------------------------------------
def game_loop(screen, difficulty, speed):

    # DIFFICULTY MULTIPLIER
    diff_mult = DIFFICULTY_LEVELS[difficulty]

    # SPEED MULTIPLIER
    if speed == "0.5x":
        turn_delay = 0.25
    elif speed == "1x":
        turn_delay = 0.5
    else:
        turn_delay = 1.0

    # CREATE INITIAL GRID
    grid = make_grid()
    hospitals = []
    quarantines = []
    day = 0
    energy = STARTING_ENERGY

    # NEW FLAG
    first_turn = True

    # -------------------------------------------
    # STARTING INFECTION SELECTION WITH PROMPT
    # -------------------------------------------
    picking = True
    font = pygame.font.SysFont("arial", 32)

    while picking:
        draw_grid(screen, grid, hospitals, quarantines)

        msg = font.render(
            "Click a cell to choose the infection starting point",
            True, WHITE
        )
        screen.blit(msg, (40, 20))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = e.pos
                if mx < GRID_COLS * CELL_SIZE:
                    r = my // CELL_SIZE
                    c = mx // CELL_SIZE
                    grid[r][c] = INF
                    picking = False

    # -------------------------------------------
    # MAIN TURN-BY-TURN LOOP
    # -------------------------------------------
    while True:

        # -------------------------------
        # TURN POPUP ACTION SELECTION
        # BUT ONLY AFTER FIRST 10 DAYS
        # -------------------------------
        action_mode = None

        if not first_turn:   
            buttons = create_turn_buttons()
            choosing = True

            while choosing:

                # Hover update
                mpos = pygame.mouse.get_pos()
                for b in buttons.values():
                    b.update_hover(mpos)

                draw_grid(screen, grid, hospitals, quarantines)
                draw_stats(
                    screen,
                    infected=sum(cell == INF for row in grid for cell in row),
                    recovered=sum(cell == REC for row in grid for cell in row),
                    dead=sum(cell == DED for row in grid for cell in row),
                    energy=energy,
                    day=day
                )
                draw_turn_popup(screen, buttons, energy)
                pygame.display.flip()

                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        pygame.quit(); sys.exit()
                    if e.type == pygame.MOUSEBUTTONDOWN:

                        if buttons["vaccine"].clicked(e.pos) and energy >= COST_VACCINE:
                            action_mode = "vaccine"
                            choosing = False

                        if buttons["quarantine"].clicked(e.pos) and energy >= COST_QUARANTINE:
                            action_mode = "quarantine"
                            choosing = False

                        if buttons["hospital"].clicked(e.pos) and energy >= COST_HOSPITAL:
                            action_mode = "hospital"
                            choosing = False

                        if buttons["endturn"].clicked(e.pos):
                            action_mode = None
                            choosing = False

        # ----------------------------------------
        # PLAYER PLACES THE CHOSEN ACTION
        # (Only happens after turn 1)
        # ----------------------------------------
        if action_mode:
            placed = False

            while not placed:

                draw_grid(screen, grid, hospitals, quarantines)

                mx, my = pygame.mouse.get_pos()
                r = my // CELL_SIZE
                c = mx // CELL_SIZE

                if mx < GRID_COLS * CELL_SIZE:

                    if action_mode == "vaccine":
                        pygame.draw.circle(
                            screen, (0, 150, 255),
                            (c * CELL_SIZE, r * CELL_SIZE),
                            VACCINE_RADIUS, 3
                        )

                    elif action_mode == "quarantine":
                        pygame.draw.rect(
                            screen, (255, 255, 0),
                            (c * CELL_SIZE - 20, r * CELL_SIZE - 20, 60, 60),
                            3
                        )

                    elif action_mode == "hospital":
                        pygame.draw.line(
                            screen, WHITE,
                            (c * CELL_SIZE - 10, r * CELL_SIZE),
                            (c * CELL_SIZE + 10, r * CELL_SIZE), 3
                        )
                        pygame.draw.line(
                            screen, WHITE,
                            (c * CELL_SIZE, r * CELL_SIZE - 10),
                            (c * CELL_SIZE, r * CELL_SIZE + 10), 3
                        )
                        # draw hospital radius preview (5x5 area)
                        pygame.draw.rect(
                            screen, WHITE,
                            (c * CELL_SIZE - 2 * CELL_SIZE,
                             r * CELL_SIZE - 2 * CELL_SIZE,
                             CELL_SIZE * 5,
                             CELL_SIZE * 5),
                            2
                        )

                draw_stats(
                    screen,
                    infected=sum(cell == INF for row in grid for cell in row),
                    recovered=sum(cell == REC for row in grid for cell in row),
                    dead=sum(cell == DED for row in grid for cell in row),
                    energy=energy,
                    day=day
                )
                pygame.display.flip()

                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        pygame.quit(); sys.exit()
                    if e.type == pygame.MOUSEBUTTONDOWN:

                        mx, my = e.pos
                        if mx < GRID_COLS * CELL_SIZE:
                            rr = my // CELL_SIZE
                            cc = mx // CELL_SIZE

                            if action_mode == "vaccine":
                                grid = place_vaccine(grid, rr, cc)
                                energy -= COST_VACCINE
                                SFX_VACCINE.play()

                            elif action_mode == "quarantine":
                                place_quarantine(quarantines, rr, cc)
                                energy -= COST_QUARANTINE
                                SFX_QUARANTINE.play()

                            elif action_mode == "hospital":
                                place_hospital(grid, hospitals, rr, cc)
                                energy -= COST_HOSPITAL
                                SFX_HOSPITAL.play()

                            placed = True
                            action_mode = None

        # -----------------------------------------------------
        # END TURN → SIMULATE TEN DAYS
        # -----------------------------------------------------
        for _ in range(10):
            old = [row[:] for row in grid]
            new = simulate_day(grid, diff_mult, hospitals, quarantines)
            animate_simulation(screen, old, new, hospitals, quarantines) 
            grid = new
            day += 1

        # After simulating FIRST 10 days → allow actions
        if first_turn:
            first_turn = False

        # -----------------------------------------------------
        # END CONDITIONS
        # -----------------------------------------------------
        total_cells = GRID_ROWS * GRID_COLS
        infected_count = sum(cell == INF for row in grid for cell in row)
        susceptible_count = sum(cell == SUS for row in grid for cell in row)

        if infected_count == 0:
            pygame.mixer.music.pause()
            SFX_VICTORY.play()
            # WIN!
            high = load_high_score()

            # If no high score yet OR new score is better
            if high is None or day < high:
                save_high_score(day)
                msg = f"NEW HIGH SCORE! Won in {day} days."
            else:
                msg = f"Victory! Won in {day} days. High Score: {high}"

            end_screen(screen, msg)
            return


        if susceptible_count == 0:
            pygame.mixer.music.pause()
            SFX_DEFEAT.play()
            end_screen(screen, "DEFEAT! Entire population infected.")
            return

        # Energy regeneration
        energy = min(MAX_ENERGY, energy + ENERGY_REGEN)

        # Refresh frame
        draw_grid(screen, grid, hospitals, quarantines)
        draw_stats(
            screen,
            infected=infected_count,
            recovered=sum(cell == REC for row in grid for cell in row),
            dead=sum(cell == DED for row in grid for cell in row),
            energy=energy,
            day=day
        )
        pygame.display.flip()






def end_screen(screen, message):
    pygame.font.init()
    font_big = pygame.font.SysFont("arial", 48)
    font_small = pygame.font.SysFont("arial", 28)

    while True:
        screen.fill((0, 0, 0))

        # multi-line message support
        lines = message.split("\n")
        y = SCREEN_HEIGHT//2 - 40 - 30*len(lines)

        for line in lines:
            text = font_big.render(line, True, (255, 255, 255))
            screen.blit(text, (80, y))
            y += 60

        sub = font_small.render("Press ENTER to return to main menu", True, (200, 200, 200))
        screen.blit(sub, (80, SCREEN_HEIGHT//2 + 80))

        pygame.display.flip()

        # --------------------------
        # CRITICAL: EVENT LOOP
        # --------------------------
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    return



# ------------------------------------------------------------
# ENTRY POINT
# ------------------------------------------------------------
def main():
    pygame.init()
    pygame.mixer.music.play(-1)  
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pandemic Strategy Game")

    while True:   # <-- MAIN LOOP

        draw_start_screen(screen)
        difficulty, speed = draw_settings_screen(screen)

        # This runs the game
        game_loop(screen, difficulty, speed)

        # When game_loop returns (end of game), show start screen again
        # loop continues automatically



if __name__ == "__main__":
    main()

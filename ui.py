# ============================================================
# ui.py — UI Elements, Screens, Buttons, Stats, Popups
# ============================================================

import pygame
from config import *

# -----------------------------------------------------------
# Tooltip descriptions for turn menu
# -----------------------------------------------------------
ACTION_DESCRIPTIONS = {
    "vaccine": "Heals infections in a large radius and grants immunity.",
    "quarantine": "Reduces spread by 40% in a 3x3 zone.",
    "hospital": "Boosts recovery chance by +20% in a 5x5 area.",
    "endturn": "Skip action and advance 10 days."
}



# ------------------------------------------------------------
# Fonts & Colors
# ------------------------------------------------------------
pygame.font.init()

FONT = pygame.font.SysFont("segoeui", 26)
FONT_BIG = pygame.font.SysFont("segoeui", 48, bold=True)
FONT_SMALL = pygame.font.SysFont("segoeui", 20)

WHITE = (245, 245, 245)
GRAY = (160, 160, 160)
GRAY_H = (190, 190, 190)
BLUE = (80, 140, 255)
DARK = (25, 25, 35)
POP_BG = (20, 20, 30, 240) 


# ============================================================
# BUTTON
# ============================================================
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.hovered = False

    def update_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

    def draw(self, screen):
        color = GRAY_H if self.hovered else GRAY
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, DARK, self.rect, 3, border_radius=10)

        label = FONT.render(self.text, True, WHITE)
        screen.blit(label, (
            self.rect.centerx - label.get_width() // 2,
            self.rect.centery - label.get_height() // 2

        ))


def draw_selected_button(screen, button):
    pygame.draw.rect(screen, (255, 255, 255), button.rect, 4, border_radius=10)

# ============================================================
# STATS SIDEBAR
# ============================================================
def draw_stats(screen, infected, recovered, dead, energy, day):
    sidebar_x = GRID_COLS * CELL_SIZE

    pygame.draw.rect(
        screen, DARK,
        (sidebar_x, 0, SCREEN_WIDTH - sidebar_x, SCREEN_HEIGHT)
    )

    y = 40

    # Title
    header = FONT_BIG.render("Stats", True, WHITE)
    screen.blit(header, (sidebar_x + 25, y))
    y += 90

    stats = [
        ("Day", day, WHITE),
        ("Infected", infected, (255, 80, 80)),
        ("Recovered", recovered, (80, 255, 80)),
        ("Dead", dead, (130, 130, 130)),
        ("Energy", f"{energy}/{MAX_ENERGY}", BLUE)
    ]

    for label, value, color in stats:
        line = FONT.render(f"{label}: {value}", True, color)
        screen.blit(line, (sidebar_x + 25, y))
        y += 50


# ============================================================
# START GAME SCREEN
# ============================================================
def draw_start_screen(screen):

    start_btn = Button(SCREEN_WIDTH//2 - 150, 430, 300, 60, "Start Game")

    while True:
        screen.fill(DARK)

        title = FONT_BIG.render("Pandemic Strategy Game", True, WHITE)
        screen.blit(title, (
            SCREEN_WIDTH//2 - title.get_width()//2,
            180
        ))

        # Hover effect
        mpos = pygame.mouse.get_pos()
        start_btn.update_hover(mpos)

        start_btn.draw(screen)
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.clicked(e.pos):
                    return  # continue to settings screen


# ============================================================
# DIFFICULTY + SPEED SCREEN
# ============================================================
def draw_settings_screen(screen):

    # Difficulty buttons
    diff_buttons = {
        "Easy": Button(SCREEN_WIDTH//2 - 150, 300, 300, 55, "Easy"),
        "Normal": Button(SCREEN_WIDTH//2 - 150, 360, 300, 55, "Normal"),
        "Hard": Button(SCREEN_WIDTH//2 - 150, 420, 300, 55, "Hard"),
    }

    # Corrected speed buttons
    speed_buttons = {
        "0.5x": Button(SCREEN_WIDTH//2 - 150, 530, 140, 55, "0.5x"),
        "1x":   Button(SCREEN_WIDTH//2 + 10, 530, 140, 55, "1x")
    }

    chosen_difficulty = None
    chosen_speed = None

    while True:
        screen.fill(DARK)

        # Titles
        title = FONT_BIG.render("Choose Difficulty & Speed", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 180))

        diff_label = FONT.render("Difficulty:", True, WHITE)
        screen.blit(diff_label, (SCREEN_WIDTH//2 - diff_label.get_width()//2, 255))

        speed_label = FONT.render("Game Speed:", True, WHITE)
        screen.blit(speed_label, (SCREEN_WIDTH//2 - speed_label.get_width()//2, 490))

        # Hover states
        mpos = pygame.mouse.get_pos()
        for b in diff_buttons.values():
            b.update_hover(mpos)
        for b in speed_buttons.values():
            b.update_hover(mpos)

        # Draw difficulty buttons
        for name, b in diff_buttons.items():
            b.draw(screen)
            if chosen_difficulty == name:
                draw_selected_button(screen, b)

        # Draw speed buttons
        for name, b in speed_buttons.items():
            b.draw(screen)
            if chosen_speed == name:
                draw_selected_button(screen, b)

        pygame.display.flip()   

        # Click detection
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()

            if e.type == pygame.MOUSEBUTTONDOWN:

                # Difficulty
                for name, b in diff_buttons.items():
                    if b.clicked(e.pos):
                        chosen_difficulty = name

                # Speed
                for name, b in speed_buttons.items():
                    if b.clicked(e.pos):
                        chosen_speed = name

                # If both chosen, return
                if chosen_difficulty and chosen_speed:
                    return chosen_difficulty, chosen_speed
# ============================================================
# TURN ACTION POPUP
# ============================================================
def draw_turn_popup(screen, buttons, energy):

    # Semi-transparent overlay
    popup = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(
        popup,
        POP_BG,
        (SCREEN_WIDTH//2 - 250, 180, 500, 420),
        border_radius=22
    )
    screen.blit(popup, (0, 0))

    # Title
    title = FONT_BIG.render("Choose an Action", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 210))

    # Energy
    energy_label = FONT.render(f"Energy: {energy}/{MAX_ENERGY}", True, BLUE)
    screen.blit(energy_label, (SCREEN_WIDTH//2 - energy_label.get_width()//2, 260))

    # ------------------------------
    # UPDATE HOVER STATES
    # ------------------------------
    mpos = pygame.mouse.get_pos()
    for b in buttons.values():
        b.update_hover(mpos)

    # ------------------------------
    # DRAW BUTTONS + DETECT HOVER
    # ------------------------------
    hover_key = None
    for key, b in buttons.items():
        b.draw(screen)
        if b.hovered:
            hover_key = key

    # ------------------------------
    # DRAW TOOLTIP (if hovering)
    # ------------------------------
    if hover_key:
        desc = ACTION_DESCRIPTIONS.get(hover_key, "")
        tooltip = FONT_SMALL.render(desc, True, WHITE)
        rect = tooltip.get_rect()
        rect.centerx = SCREEN_WIDTH // 2
        rect.top = 550  

        pygame.draw.rect(
            screen, DARK,
            (rect.left - 10, rect.top - 6, rect.width + 20, rect.height + 12),
            border_radius=8
        )
        screen.blit(tooltip, rect)



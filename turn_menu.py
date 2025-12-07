# ============================================================
# turn_menu.py — Turn Popup Buttons
# ============================================================

from ui import Button
from config import *


def create_turn_buttons():

    # Button geometry
    btn_w = 300
    btn_h = 55
    gap = 70

    cx = SCREEN_WIDTH//2 - btn_w//2
    start_y = 310

    return {
        "quarantine": Button(
            cx, start_y + 0*gap, btn_w, btn_h,
            f"Place Quarantine ({COST_QUARANTINE})"
        ),

        "hospital": Button(
            cx, start_y + 1*gap, btn_w, btn_h,
            f"Build Hospital ({COST_HOSPITAL})"
        ),

        "vaccine": Button(
            cx, start_y + 2*gap, btn_w, btn_h,
            f"Deploy Vaccine ({COST_VACCINE})"
        ),

        "endturn": Button(
            cx, start_y + 3*gap + 20, btn_w, btn_h,
            "End Turn"
        ),
    }


"""CONSTANTS"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(__file__, "../waveshare/")))

# GPIO Pins
RST_PIN = 25
CS_PIN = 8
DC_PIN = 24

class KEYS:
    # ----------------------------------------------------------
    # CHANGED UP/DOWN - LEFT/RIGHT MAPPING DUE TO PORTRAIT USAGE
    # DEFAULT VALUES LEFT AS COMMENTS
    KEY_UP_PIN = 26  # 6
    KEY_DOWN_PIN = 5  # 19
    KEY_LEFT_PIN = 6  # 5
    KEY_RIGHT_PIN = 19  # 26
    # ----------------------------------------------------------
    KEY_PRESS_PIN = 13
    KEY1_PIN = 21
    KEY2_PIN = 20
    KEY3_PIN = 16

# SCREEN VALUES
OUTLINE = 255
FILL_ZERO = 0
FILL_ONE = 1

EXPECTED_BULB_NAMES = ["bongoNC", "beddyboi"]
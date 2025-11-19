"""
This file contains all the constants used in the game.
"""

# Screen dimensions
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256

# Game states
STATE_PLAYING = 1
STATE_GAME_OVER = 2
STATE_TRUCK_AWAY = 3
STATE_PAUSED = 4


# --- Sprites ---
# This is a placeholder for the image bank file.
# I will assume image bank 0 for all sprites.
IMG_BANK = 0

# Mario: (img_bank, u, v, w, h, colkey)
MARIO_SPRITES = {
    "right": (IMG_BANK, 32, 0, 16, 16, 0),
    "left": (IMG_BANK, 32, 16, 16, 16, 0),
}
# Luigi: (img_bank, u, v, w, h, colkey)
LUIGI_SPRITES = {
    "right": (IMG_BANK, 48, 0, 16, 16, 0),
    "left": (IMG_BANK, 48, 16, 16, 16, 0),
}
# Boss: (img_bank, u, v, w, h, colkey)
BOSS_SPRITE = (IMG_BANK, 48, 96, 16, 16, 0)

# Package: (img_bank, u, v, w, h, colkey)
PACKAGE_SPRITE = (IMG_BANK, 0, 0, 16, 16, 0)

# Truck: (img_bank, u, v, w, h, colkey)
TRUCK_SPRITE = (IMG_BANK, 64, 0, 48, 16, 0)

# --- Game Layout ---
# Conveyor Belts
NUM_CONVEYORS = 5
CONVEYOR_Y_START = 200
CONVEYOR_Y_SPACING = 40
CONVEYOR_LENGTH = 240
CONVEYOR_X_START_RIGHT = SCREEN_WIDTH - 20
CONVEYOR_X_END_LEFT = 20

# Floors (y-positions for characters)
FLOOR_Y_POSITIONS = [CONVEYOR_Y_START + 8] + [
    CONVEYOR_Y_START - (i * CONVEYOR_Y_SPACING) + 8 for i in range(NUM_CONVEYORS)
]

# Character positions
MARIO_X = SCREEN_WIDTH - 40
LUIGI_X = 24

# Truck position
TRUCK_X = 5
TRUCK_Y = FLOOR_Y_POSITIONS[0] - 24

# Boss position
BOSS_X = (SCREEN_WIDTH // 2) - 12
BOSS_Y = 10


# --- Game Mechanics ---
# Controls
MARIO_UP = "up"
MARIO_DOWN = "down"
LUIGI_UP = "w"
LUIGI_DOWN = "s"

# Speeds
PACKAGE_SPEED = 1

# Timers
TRUCK_AWAY_DURATION = 300 # 5 seconds at 60fps
BOSS_APPEAR_DURATION = 120 # 2 seconds at 60fps

# Scoring
POINTS_PER_PACKAGE = 1
POINTS_PER_TRUCK = 10

# Failures
MAX_FAILURES = 3
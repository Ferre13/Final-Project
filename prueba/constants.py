"""
This file contains all the constants used in the game.
"""
import random

# Screen size
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256

# Game states
GAME_PLAYING = 1
GAME_OVER = 2
GAME_TRUCK = 3
GAME_PAUSE = 4
# BOSS???? Change


# SPRITES
SPRITES_FILE = "assets/my_resources.pyxres"

# img, x_ins, y_ins, w, h, colkey
# Mario sprites
MARIO_STATIC = (0, 32, 0, 16, 16, 0)
MARIO_WAIT = (0, 32, 16, 16, 16, 0)
MARIO_PCK = (0, 32, 32, 16, 16, 0)
MARIO_BOSS = (0, 32, 48, 16, 16, 0)
MARIO_REST1 = (0, 32, 64, 16, 16, 0)
MARIO_REST2 = (0, 32, 80, 16, 16, 0)

# Luigi sprites
LUIGI_STATIC = (0, 48, 0, 16, 16, 0)  
LUIGI_WAIT = (0, 48, 16, 16, 16, 0)  
LUIGI_PCK = (0, 48, 32, 16, 16, 0)  
LUIGI_BOSS = (0, 48, 48, 16, 16, 0)
LUIGI_REST1 = (0, 48, 64, 16, 16, 0)
LUIGI_REST2 = (0, 48, 80, 16, 16, 0)

# Boss sprites
BOSS_1 = (0, 32, 96, 16, 16, 0)
BOSS_2 = (0, 48, 96, 16, 16, 0)

# Package sprites
PCK_LVL1 = (0, 0, 0, 16, 16, 0)  
PCK_LVL1_FALL = (0, 16, 0, 16, 16, 0)  
PCK_LVL2 = (0, 0, 16, 16, 16, 0)  
PCK_LVL2_FALL = (0, 16, 16, 16, 16, 0)  
PCK_LVL3 = (0, 0, 32, 16, 16, 0)  
PCK_LVL3_FALL = (0, 16, 32, 16, 16, 0)  
PCK_LVL4 = (0, 0, 48, 16, 16, 0)  
PCK_LVL4_FALL = (0, 16, 48, 16, 16, 0) 
PCK_LVL5 = (0, 0, 64, 16, 16, 0)  
PCK_LVL5_FALL = (0, 16, 64, 16, 16, 0)  
PCK_LVL6 = (0, 0, 80, 16, 16, 0)  
PCK_LVL6_FALL = (0, 16, 80, 16, 16, 0)  
PCK_LVL7 = (0, 0, 96, 16, 16, 0)  
PCK_LVL7_FALL = (0, 16, 96, 16, 16, 0)  
PCK_LVL8 = (0, 0, 112, 16, 16, 0)  
PCK_LVL8_FALL = (0, 16, 112, 16, 16, 0)  
PCK_LVL9 = (0, 0, 128, 16, 16, 0)  
PCK_LVL9_FALL = (0, 16, 128, 16, 16, 0)  
PCK_LVL10 = (0, 0, 144, 16, 16, 0)  
PCK_LVL10_FALL = (0, 16, 144, 16, 16, 0)  
PCK_EXPLODE = (0, 0, 160, 16, 16, 0)  

# Truck sprites
TRUCK_EMPTY = (0, 64, 0, 48, 16, 0)
TRUCK_1 = (0, 64, 16, 48, 16, 0)
TRUCK_2 = (0, 64, 32, 48, 16, 0)
TRUCK_3 = (0, 64, 48, 48, 16, 0)
TRUCK_4 = (0, 64, 64, 48, 16, 0)
TRUCK_5 = (0, 64, 80, 48, 16, 0)
TRUCK_6 = (0, 64, 96, 48, 16, 0)
TRUCK_7 = (0, 64, 112, 48, 16, 0)
TRUCK_8 = (0, 64, 128, 48, 16, 0)
TRUCK_FULL = (0, 64, 144, 48, 16, 0)


#Conveyor sprite
CONVEYOR_SPRITE = (0, 32, 152, 32, 8, 0)  

# Life sprite
LIFE_SPRITE = (0, 32, 112, 16, 16, 0)

# Platform sprite
PLATFORM_SPRITE = (0, 0, 16, 16, 16, 0)

# Exit signal sprite
EXIT_SIGNAL_SPRITE = (0, 112, 112, 16, 16, 0)

# Door sprites
DOOR_CLOSED = (0, 112, 128, 16, 16, 0)
DOOR_OPENING = (0, 128, 128, 16, 16, 0)
DOOR_OPEN = (0, 144, 128, 16, 16, 0)

# Number sprites
NUMBER_0 = (0, 0, 176, 8, 8, 0)
NUMBER_1 = (0, 8, 176, 8, 8, 0)
NUMBER_2 = (0, 16, 176, 8, 8, 0)
NUMBER_3 = (0, 24, 176, 8, 8, 0)
NUMBER_4 = (0, 32, 176, 8, 8, 0)
NUMBER_5 = (0, 40, 176, 8, 8, 0)
NUMBER_6 = (0, 48, 176, 8, 8, 0)
NUMBER_7 = (0, 56, 176, 8, 8, 0)
NUMBER_8 = (0, 64, 176, 8, 8, 0)
NUMBER_9 = (0, 72, 176, 8, 8, 0)

VERTICAL_STRUCTURE_SPRITE = (0, 160, 0, 12, 16, 0)
MACHINE_SPRITE = (0, 176, 0, 32, 32, 0)
WINDOW_SPRITE = (0, 112, 144, 32, 32, 0)

NUMBER_SPRITES = [NUMBER_0, NUMBER_1, NUMBER_2, NUMBER_3, NUMBER_4, NUMBER_5, NUMBER_6, NUMBER_7, NUMBER_8, NUMBER_9]


# GAME SETTINGS

# Conveyor settings
NUM_CONVEYORS_EASY = 5
NUM_CONVEYORS_MEDIUM = 7 
NUM_CONVEYORS_EXTREME = 9 
NUM_CONVEYORS_CRAZY = 5 
CONVEYOR_Y_START = 200
CONVEYOR_DISTANCE = 40
CONVEYOR_LENGTH = 240
CONVEYOR_X_RIGHT = SCREEN_WIDTH - 20
CONVEYOR_X_LEFT = 20

# Character positions
MARIO_X = SCREEN_WIDTH - 70
LUIGI_X = 50
MARIO_BOSS_X = SCREEN_WIDTH - 40
LUIGI_BOSS_X = 25


# Truck position
TRUCK_X = 15
TRUCK_Y = SCREEN_HEIGHT - 80

# Boss positions
BOSS_Y = 100
BOSS_MARIO = SCREEN_WIDTH - 20
BOSS_LUIGI = 10

# Floors (y positions)
FLOOR_Y_POSITIONS = [
    CONVEYOR_Y_START - (i * CONVEYOR_DISTANCE) + 8 for i in range(NUM_CONVEYORS_EASY + 1)
]

# Characters controls
MARIO_UP = "up"
MARIO_DOWN = "down"
LUIGI_UP = "w"
LUIGI_DOWN = "s"

# Speeds
SLOW_SPEED = 1  # For easy, conveyor0 and even conveyors (medium)
MEDIUM_SPEED = 1.5  # For odd conveyors (medium), even conveyors (extreme)
FAST_SPEED = 2  # For odd conveyors (extreme)
RANDOM_SPEED = random.uniform(1, 2)  # For each conveyor (except 0) in crazy

# Timers
TRUCK_AWAY_DURATION = 600
BOSS_SCENE = 400

# Scoring
POINTS_PER_PACKAGE = 1
POINTS_PER_TRUCK = 10

# Failures
MAX_FAILURES = 3
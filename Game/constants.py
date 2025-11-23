"""
This file contains all the constants used in the game.
"""
import random

# Screen size
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 156

# Game states
GAME_PLAYING = 1
GAME_OVER = 2
GAME_TRUCK = 3
GAME_PAUSE = 4

# SPRITES
SPRITES_FILE = "assets/my_resource.pyxres"

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
PCK_LVL1 = (0, 3, 5, 11, 6, 0)  
PCK_LVL1_FALL = (0, 16, 0, 11, 16, 0)  
PCK_LVL2 = (0, 0, 16, 11, 6, 0)  
PCK_LVL2_FALL = (0, 16, 16, 16, 16, 0)  
PCK_LVL3 = (0, 0, 32, 11, 6, 0)  
PCK_LVL3_FALL = (0, 16, 32, 16, 16, 0)  
PCK_LVL4 = (0, 0, 48, 11, 6, 0)  
PCK_LVL4_FALL = (0, 16, 48, 16, 16, 0) 
PCK_LVL5 = (0, 0, 64, 11, 6, 0)  
PCK_LVL5_FALL = (0, 16, 64, 16, 16, 0)  
PCK_LVL6 = (0, 0, 80, 11, 6, 0)  
PCK_LVL6_FALL = (0, 16, 80, 16, 16, 0)  
PCK_LVL7 = (0, 0, 96, 11, 6, 0)  
PCK_LVL7_FALL = (0, 16, 96, 16, 16, 0)  
PCK_LVL8 = (0, 0, 112, 11, 6, 0)  
PCK_LVL8_FALL = (0, 16, 112, 16, 16, 0)  
PCK_LVL9 = (0, 0, 128, 11, 6, 0)  
PCK_LVL9_FALL = (0, 16, 128, 16, 16, 0)  
PCK_LVL10 = (0, 0, 144, 11, 6, 0)  
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

# Conveyor sprite
CONVEYOR_SPRITE = (0, 32, 154, 32, 4, 0)  
LIFE_SPRITE = (0, 32, 112, 16, 16, 0)
PLATFORM_SPRITE = (0, 7, 187, 25, 13, 0)
PLATFORM_0_SPRITE = (1, 33, 34, 14, 2, 0)
EXIT_SIGNAL_SPRITE = (0, 32, 128, 16, 7, 0)
DOOR_CLOSED = (0, 32, 136, 16, 16, 0)
DOOR_OPENING = (0, 48, 136, 16, 16, 0)
DOOR_OPEN = (0, 48, 120, 16, 16, 0)

# Number sprites
NUMBER_0 = (1, 10, 32, 4, 8, 0)
NUMBER_1 = (1, 2, 0, 4, 8, 0)
NUMBER_2 = (1, 10, 0, 4, 8, 0)
NUMBER_3 = (1, 2, 8, 4, 8, 0)
NUMBER_4 = (1, 10, 8, 4, 8, 0)
NUMBER_5 = (1, 2, 16, 4, 8, 0)
NUMBER_6 = (1, 10, 16, 4, 8, 0)
NUMBER_7 = (1, 2, 24, 4, 8, 0)
NUMBER_8 = (1, 10, 24, 4, 8, 0)
NUMBER_9 = (1, 2, 32, 4, 8, 0)

VERTICAL_STRUCTURE_SPRITE = (1, 18, 17, 12, 35, 0)
MACHINE_SPRITE = (1, 32, 17, 14, 13, 0)
WINDOW_SPRITE = (1, 18, 2, 32, 12, 0)

NUMBER_SPRITES = [NUMBER_0, NUMBER_1, NUMBER_2, NUMBER_3, NUMBER_4, NUMBER_5, NUMBER_6, NUMBER_7, NUMBER_8, NUMBER_9]

# --- GAME SETTINGS ---

# Distances
CONVEYOR_Y_START = 140 
CONVEYOR_DISTANCE = 15

# Floors (Bottom to Top)
FLOORS_EASY = [CONVEYOR_Y_START - (i * CONVEYOR_DISTANCE) for i in range(5)]
FLOORS_CRAZY = FLOORS_EASY
FLOORS_MEDIUM = [CONVEYOR_Y_START - (i * CONVEYOR_DISTANCE) for i in range(7)]
FLOORS_EXTREME = [CONVEYOR_Y_START - (i * CONVEYOR_DISTANCE) for i in range(9)]

# Central Structure Logic
CENTER_SCREEN = SCREEN_WIDTH // 2  # 128
STRUCT_WIDTH_PX = 24 
STRUCT_X = CENTER_SCREEN - (STRUCT_WIDTH_PX // 2)

# Conveyor Dimensions (Split)
CONVEYOR_LENGTH = 48 
CONVEYOR_X_LEFT = STRUCT_X - CONVEYOR_LENGTH
CONVEYOR_X_RIGHT = STRUCT_X + STRUCT_WIDTH_PX

# Conveyor ends at approx 68 (Left side) and 188 (Right side)
# We reduced gap to 4px. Platform width is 25px.
LUIGI_X = 39
MARIO_X = 192

# Machine & Extra Conveyor
MACHINE_X = SCREEN_WIDTH - 20 # 236
# Moved 1px lower (156 - 24 = 132)
MACHINE_Y = SCREEN_HEIGHT - 24 

# The conveyor connected to the machine
MACHINE_CONV_LENGTH = 24
MACHINE_CONV_X = MACHINE_X - MACHINE_CONV_LENGTH

# Truck position (TOP LEFT)
TRUCK_X = 5
TRUCK_Y = 20  # Default fallback, actual Y is calculated dynamically

# Boss positions
BOSS_Y = 60
BOSS_MARIO = SCREEN_WIDTH - 20
BOSS_LUIGI = 10

# Characters controls
MARIO_UP = "up"
MARIO_DOWN = "down"
LUIGI_UP = "w"
LUIGI_DOWN = "s"

# Speeds
SLOW_SPEED = 1
MEDIUM_SPEED = 1.5
FAST_SPEED = 2
RANDOM_SPEED = random.uniform(1, 2)

# Timers
TRUCK_AWAY_DURATION = 600
BOSS_SCENE = 400

# Scoring
POINTS_PER_PACKAGE = 1
POINTS_PER_TRUCK = 10
MAX_FAILURES = 3
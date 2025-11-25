"""
This file contains all the constants used in the game.
"""
import random

# Screen size
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 128

# Game states. Not used?
GAME_PLAYING = 1
GAME_OVER = 2
GAME_TRUCK = 3
GAME_PAUSE = 4

# SPRITES
SPRITES_FILE = "assets/my_resource.pyxres"

# Mario sprites
MARIO_STATIC = (0, 36, 2, 10, 14, 0)
MARIO_WAIT = (0, 35, 18, 13, 14, 0)
MARIO_PCK = (0, 36, 33, 12, 15, 0)
MARIO_BOSS = (0, 35, 50, 10, 14, 0)
MARIO_REST1 = (0, 33, 66, 13, 13, 0)
MARIO_REST2 = (0, 33, 83, 14, 12, 0)

MARIO_SPRITES = [MARIO_STATIC, MARIO_WAIT, MARIO_PCK, MARIO_BOSS, MARIO_REST1, MARIO_REST2]

# Luigi sprites
LUIGI_STATIC = (0, 52, 1, 10, 15, 0)  
LUIGI_WAIT = (0, 50, 17, 13, 15, 0)  
LUIGI_PCK = (0, 50, 33, 13, 15, 0)  
LUIGI_BOSS = (0, 51, 50, 10, 14, 0)
LUIGI_REST1 = (0, 50, 66, 13, 13, 0)
LUIGI_REST2 = (0, 49, 83, 14, 12, 0)

LUIGI_SPRITES = [LUIGI_STATIC, LUIGI_WAIT, LUIGI_PCK, LUIGI_BOSS, LUIGI_REST1, LUIGI_REST2]

# Boss sprites
BOSS_1 = (0, 32, 96, 16, 16, 0)
BOSS_2 = (0, 48, 96, 16, 16, 0)

# Package sprites
PCK_LVL1 = (0, 3, 5, 11, 6, 0)  
PCK_LVL1_FALL = (0, 17, 4, 10, 12, 0)  
PCK_LVL2 = (0, 3, 21, 11, 6, 0)  
PCK_LVL2_FALL = (0, 17, 20, 10, 12, 0)  
PCK_LVL3 = (0, 3, 36, 11, 6, 0)  
PCK_LVL3_FALL = (0, 17, 36, 10, 12, 0)  
PCK_LVL4 = (0, 3, 52, 11, 6, 0)  
PCK_LVL4_FALL = (0, 17, 52, 10, 12, 0) 
PCK_LVL5 = (0, 3, 68, 11, 6, 0)  
PCK_LVL5_FALL = (0, 17, 68, 10, 12, 0)  
PCK_LVL6 = (0, 3, 84, 11, 6, 0)  
PCK_LVL6_FALL = (0, 17, 84, 10, 12, 0)  
PCK_LVL7 = (0, 3, 100, 11, 6, 0)  
PCK_LVL7_FALL = (0, 17, 100, 10, 12, 0)  
PCK_LVL8 = (0, 3, 116, 11, 6, 0)  
PCK_LVL8_FALL = (0, 17, 116, 10, 12, 0)  
PCK_LVL9 = (0, 3, 132, 11, 6, 0)  
PCK_LVL9_FALL = (0, 17, 132, 10, 12, 0)  
PCK_LVL10 = (0, 3, 148, 11, 6, 0)  
PCK_LVL10_FALL = (0, 17, 148, 10, 12, 0)  
PCK_EXPLODE = (0, 0, 160, 16, 16, 0)  

PCK_EASY_SPRITES = [PCK_LVL1, PCK_LVL1_FALL, PCK_LVL3, PCK_LVL3_FALL, PCK_LVL5, PCK_LVL5_FALL, 
                    PCK_LVL7, PCK_LVL7_FALL, PCK_LVL9, PCK_LVL9_FALL, PCK_LVL10, PCK_LVL10_FALL]
PCK_CRAZY_SPRITES = PCK_EASY_SPRITES
PCK_MEDIUM_SPRITES = [PCK_LVL1, PCK_LVL1_FALL, PCK_LVL2, PCK_LVL2_FALL, PCK_LVL3, PCK_LVL3_FALL, PCK_LVL5, PCK_LVL5_FALL,
                      PCK_LVL7, PCK_LVL7_FALL, PCK_LVL8, PCK_LVL8_FALL, PCK_LVL9, PCK_LVL9_FALL, PCK_LVL10, PCK_LVL10_FALL]
PCK_EXTREME_SPRITES = [PCK_LVL1, PCK_LVL1_FALL, PCK_LVL2, PCK_LVL2_FALL, PCK_LVL3, PCK_LVL3_FALL, PCK_LVL4, PCK_LVL4_FALL,
                       PCK_LVL5, PCK_LVL5_FALL, PCK_LVL6, PCK_LVL6_FALL, PCK_LVL7, PCK_LVL7_FALL, PCK_LVL8, PCK_LVL8_FALL,
                       PCK_LVL9, PCK_LVL9_FALL, PCK_LVL10, PCK_LVL10_FALL]

# Truck sprites
TRUCK_EMPTY = (0, 64, 0, 32, 16, 0)
TRUCK_1 = (0, 64, 16, 32, 16, 0)
TRUCK_2 = (0, 64, 32, 32, 16, 0)
TRUCK_3 = (0, 64, 48, 32, 16, 0)
TRUCK_4 = (0, 64, 64, 32, 16, 0)
TRUCK_5 = (0, 64, 80, 32, 16, 0)
TRUCK_6 = (0, 64, 96, 32, 16, 0)
TRUCK_7 = (0, 64, 112, 32, 16, 0)
TRUCK_8 = (0, 64, 128, 32, 16, 0)
TRUCK_FULL = (0, 64, 144, 32, 16, 0)

TRUCK_SPRITES = [TRUCK_EMPTY, TRUCK_1, TRUCK_2, TRUCK_3, TRUCK_4, TRUCK_5, TRUCK_6, TRUCK_7, TRUCK_8, TRUCK_FULL]

# Conveyor sprite
CONVEYOR_SPRITE = (0, 32, 154, 32, 4, 0)  

# Life sprite
LIFE_SPRITE = (0, 32, 112, 16, 16, 0)

# Platform & Floor sprites
PLATFORM_SPRITE = (0, 15, 187, 17, 19, 0)
FLOOR_SPRITE = (1, 33, 34, 8, 2, 0)

# Door & Exit Signal sprites
EXIT_SIGNAL_SPRITE = (0, 32, 128, 16, 7, 0)

DOOR_CLOSED = (0, 32, 136, 16, 16, 0)
DOOR_OPENING = (0, 48, 136, 16, 16, 0)
DOOR_OPEN = (0, 48, 120, 16, 16, 0)

DOOR_SPRITES = {'closed': DOOR_CLOSED, 'opening': DOOR_OPENING, 'open': DOOR_OPEN, 'closing': DOOR_OPENING}

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

NUMBER_SPRITES = [NUMBER_0, NUMBER_1, NUMBER_2, NUMBER_3, NUMBER_4, NUMBER_5, NUMBER_6, NUMBER_7, NUMBER_8, NUMBER_9]

# Level text sprites
LEVEL_EASY = (0, 33, 160, 15, 5, 0)
LEVEL_MEDIUM = (0, 32, 166, 21, 5, 0)
LEVEL_EXTREME = (0, 32, 172, 27, 5, 0)
LEVEL_CRAZY = (0, 32, 178, 19, 5, 0)

# Vertical Structure sprite. colkey 1 to block things behind it
VERTICAL_STRUCTURE_SPRITE = (1, 18, 17, 12, 35, 1)

# Machine sprite
MACHINE_SPRITE = (1, 32, 17, 14, 13, 0)

# Window sprite
WINDOW_SPRITE = (1, 18, 2, 32, 12, 0)

# GAME SETTINGS

# Distances
CONVEYOR_Y_START = SCREEN_HEIGHT - 16
CONVEYOR_DISTANCE = 11

# Floors
NUM_EASY_CRAZY = 5
NUM_MEDIUM = 7
NUM_EXTREME = 9

FLOORS_EASY_CRAZY = []
for floors in range(NUM_EASY_CRAZY):
    floor = CONVEYOR_Y_START - (floors * CONVEYOR_DISTANCE)
    FLOORS_EASY_CRAZY.append(floor)

FLOORS_MEDIUM = []
for floors in range(NUM_MEDIUM):
    floor = CONVEYOR_Y_START - (floors * CONVEYOR_DISTANCE)
    FLOORS_MEDIUM.append(floor)

FLOORS_EXTREME = []
for floors in range(NUM_EXTREME):
    floor = CONVEYOR_Y_START - (floors * CONVEYOR_DISTANCE)
    FLOORS_EXTREME.append(floor)

# Vertical Structure Logic
CENTER_SCREEN = SCREEN_WIDTH // 2
STRUCT_WIDTH_PX = VERTICAL_STRUCTURE_SPRITE[3] * 2
STRUCT_X = CENTER_SCREEN - (STRUCT_WIDTH_PX // 2)

CONVEYOR_SEGMENTS = 4  # Repeat 4 times
CONVEYOR_SPRITE_W = CONVEYOR_SPRITE[3] # 32px

# Calculate total pixel width for route calculations
CONVEYOR_TOTAL_WIDTH_PX = CONVEYOR_SEGMENTS * CONVEYOR_SPRITE_W

# Calculate Start X to center the 4 segments on the screen/structure
# Formula: Center Screen - (Total Width / 2)
CONVEYOR_X_START = CENTER_SCREEN - (CONVEYOR_TOTAL_WIDTH_PX // 2)

# Character & Platform positions
LUIGI_X = 45
MARIO_X = 194

# Machine position
MACHINE_X = SCREEN_WIDTH - 14
MACHINE_Y = SCREEN_HEIGHT - 24 

# Machine Conveyor Dimensions
CONVEYOR_0_LENGTH = 32
CONVEYOR_0_X = MACHINE_X - CONVEYOR_0_LENGTH

# Truck position
TRUCK_X = 8

# Boss positions
# Watch out
BOSS_Y = MACHINE_Y - 3
BOSS_MARIO = SCREEN_WIDTH - 16  # Right Margin
BOSS_LUIGI = 0                  # Left Margin

PUNISH_MARIO_X = SCREEN_WIDTH - 30
PUNISH_LUIGI_X = 18

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
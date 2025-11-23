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
# Change. Dont know how to implement this logic

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
# Screen dimensions used for the pyxel window
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 128
# The resource file containing all the graphics
SPRITES_FILE = "assets/my_resource.pyxres"

# Limits and timers for gameplay
# Limit for the package spawning timer (approx 6 seconds)
SPAWN_TIMER_LIMIT = 180       
# Time the truck waits before moving
TRUCK_WAIT_TIME = 60          
# Time the truck stays offscreen
TRUCK_OFFSCREEN_TIME = 30     
# How fast the truck moves (pixels per frame)
TRUCK_SPEED = 2               
# Duration of the boss yelling animation
BOSS_YELL_DURATION = 60       
# Speed of the door opening/closing animation
DOOR_ANIMATION_SPEED = 10     
# Minimum time between package spawns to prevent overlapping
SPAWN_TIMER_GAP = 45 

# Scoring and Game Rules
POINTS_PER_PACKAGE = 1
POINTS_PER_TRUCK = 10
# Maximum number of failures allowed before Game Over
MAX_FAILURES = 3
# Capacity of the truck
TRUCK_MAX_CAPACITY = 8

# Physics and Dimensions
# Falling speed for packages
PACKAGE_FALL_SPEED = 2
# How many pixels a package can stick out before falling
OVERHANG_LIMIT = 5            
GROUND_HEIGHT_PX = 6
GROUND_START_Y = SCREEN_HEIGHT - GROUND_HEIGHT_PX

# States for Characters
CHAR_STATE_STATIC = 0
CHAR_STATE_WAIT = 1
CHAR_STATE_PCK = 2
CHAR_STATE_BOSS = 3
CHAR_STATE_REST1 = 4
CHAR_STATE_REST2 = 5

# States for Packages
PKG_STATE_MOVING = "moving"
PKG_STATE_FALLING = "falling"

# Status codes used to communicate between Package and Board
PKG_STATUS_MOVING = 0
PKG_STATUS_REACHED_END = 1
PKG_STATUS_FALLEN_LUIGI = 2 
PKG_STATUS_FALLEN_MARIO = 3 

# States for the Boss
BOSS_STATE_IDLE = 0
BOSS_STATE_OPENING = 1
BOSS_STATE_YELLING = 2
BOSS_STATE_CLOSING = 3

# States for the Doors
DOOR_STATE_CLOSED = "closed"
DOOR_STATE_OPENING = "opening"
DOOR_STATE_OPEN = "open"
DOOR_STATE_CLOSING = "closing"

# Sprite Definitions for Mario
MARIO_STATIC = (0, 36, 2, 10, 14, 0)
MARIO_WAIT = (0, 35, 18, 13, 14, 0)
MARIO_PCK = (0, 36, 33, 12, 15, 0)
MARIO_BOSS = (0, 35, 50, 10, 14, 0)
MARIO_REST1 = (0, 33, 66, 13, 13, 0)
MARIO_REST2 = (0, 33, 83, 14, 12, 0)
# List of Mario sprites for easy access
MARIO_SPRITES = [MARIO_STATIC, MARIO_WAIT, MARIO_PCK, MARIO_BOSS, MARIO_REST1, MARIO_REST2]

# Sprite Definitions for Luigi
LUIGI_STATIC = (0, 52, 1, 10, 15, 0)  
LUIGI_WAIT = (0, 50, 17, 13, 15, 0)  
LUIGI_PCK = (0, 50, 33, 13, 15, 0)  
LUIGI_BOSS = (0, 51, 50, 10, 14, 0)
LUIGI_REST1 = (0, 50, 66, 13, 13, 0)
LUIGI_REST2 = (0, 49, 83, 14, 12, 0)
# List of Luigi sprites for easy access
LUIGI_SPRITES = [LUIGI_STATIC, LUIGI_WAIT, LUIGI_PCK, LUIGI_BOSS, LUIGI_REST1, LUIGI_REST2]

# Sprite Definitions for the Boss
BOSS_1 = (0, 32, 96, 16, 16, 0)
BOSS_2 = (0, 48, 96, 16, 16, 0)

# Sprite Definitions for Packages (Different levels and falling states)
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

# Lists of packages to use for each difficulty level
PCK_EASY_SPRITES = [PCK_LVL1, PCK_LVL1_FALL, PCK_LVL3, PCK_LVL3_FALL, PCK_LVL5, PCK_LVL5_FALL, 
                    PCK_LVL7, PCK_LVL7_FALL, PCK_LVL9, PCK_LVL9_FALL, PCK_LVL10, PCK_LVL10_FALL]
PCK_MEDIUM_SPRITES = [PCK_LVL1, PCK_LVL1_FALL, PCK_LVL2, PCK_LVL2_FALL, PCK_LVL3, PCK_LVL3_FALL, PCK_LVL5, PCK_LVL5_FALL,
                      PCK_LVL7, PCK_LVL7_FALL, PCK_LVL8, PCK_LVL8_FALL, PCK_LVL9, PCK_LVL9_FALL, PCK_LVL10, PCK_LVL10_FALL]
PCK_EXTREME_SPRITES = [PCK_LVL1, PCK_LVL1_FALL, PCK_LVL2, PCK_LVL2_FALL, PCK_LVL3, PCK_LVL3_FALL, PCK_LVL4, PCK_LVL4_FALL,
                       PCK_LVL5, PCK_LVL5_FALL, PCK_LVL6, PCK_LVL6_FALL, PCK_LVL7, PCK_LVL7_FALL, PCK_LVL8, PCK_LVL8_FALL,
                       PCK_LVL9, PCK_LVL9_FALL, PCK_LVL10, PCK_LVL10_FALL]
PCK_CRAZY_SPRITES = PCK_EASY_SPRITES

# Truck sprites based on how full it is
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

# Environment objects
CONVEYOR_SPRITE = (0, 32, 154, 32, 4, 0)  
PLATFORM_SPRITE = (0, 15, 187, 17, 19, 0)
FLOOR_SPRITE = (1, 33, 34, 8, 2, 0)
EXIT_SIGNAL_SPRITE = (0, 32, 128, 16, 7, 0)
VERTICAL_STRUCTURE_SPRITE = (1, 18, 17, 12, 35, 1)
MACHINE_SPRITE = (1, 32, 17, 14, 13, 0)
WINDOW_SPRITE = (1, 18, 2, 32, 12, 0)

# Sprites for the boss doors
DOOR_CLOSED = (0, 32, 136, 16, 16, 0)
DOOR_OPENING = (0, 48, 136, 16, 16, 0)
DOOR_OPEN = (0, 48, 120, 16, 16, 0)
# Dictionary to map states to sprites
DOOR_SPRITES = {'closed': DOOR_CLOSED, 'opening': DOOR_OPENING, 'open': DOOR_OPEN, 'closing': DOOR_OPENING}

# Sprites for the level indicators
LEVEL_EASY = (0, 33, 160, 15, 5, 0)
LEVEL_MEDIUM = (0, 32, 166, 21, 5, 0)
LEVEL_EXTREME = (0, 32, 172, 27, 5, 0)
LEVEL_CRAZY = (0, 32, 178, 19, 5, 0)

# Number sprites for HUD
NUM_1 = (1, 2, 0, 4, 7, 0)
NUM_2 = (1, 10, 0, 4, 7, 0)
NUM_3 = (1, 2, 8, 4, 7, 0)
NUM_4 = (1, 10, 8, 4, 7, 0)
NUM_5 = (1, 2, 16, 4, 7, 0)
NUM_6 = (1, 10, 16, 4, 7, 0)
NUM_7 = (1, 2, 24, 4, 7, 0)
NUM_8 = (1, 10, 24, 4, 7, 0)
NUM_9 = (1, 2, 32, 4, 7, 0)
NUM_0 = (1, 10, 32, 4, 7, 0)

NUMBER_SPRITES = [NUM_0, NUM_1, NUM_2, NUM_3, NUM_4, NUM_5, NUM_6, NUM_7, NUM_8, NUM_9]

# Life Icon (Mario's Face for "MISS")
LIFE_SPRITE = (0, 32, 112, 16, 16, 0) 

# Coordinates for HUD elements
SCORE_X = SCREEN_WIDTH - 20
SCORE_Y = 3
LIVES_X = SCREEN_WIDTH // 2 - 20
LIVES_Y = 3

# Coordinates used to build the layout
CONVEYOR_Y_START = SCREEN_HEIGHT - 16
CONVEYOR_DISTANCE = 11
CENTER_SCREEN = SCREEN_WIDTH // 2
STRUCT_WIDTH_PX = VERTICAL_STRUCTURE_SPRITE[3] * 2
STRUCT_X = CENTER_SCREEN - (STRUCT_WIDTH_PX // 2)
CONVEYOR_SEGMENTS = 4 
CONVEYOR_SPRITE_W = CONVEYOR_SPRITE[3]
CONVEYOR_TOTAL_WIDTH_PX = CONVEYOR_SEGMENTS * CONVEYOR_SPRITE_W
CONVEYOR_X_START = CENTER_SCREEN - (CONVEYOR_TOTAL_WIDTH_PX // 2)

# Start positions for characters and objects
LUIGI_X = 45
MARIO_X = 194
MACHINE_X = SCREEN_WIDTH - 14
MACHINE_Y = SCREEN_HEIGHT - 24 
CONVEYOR_0_X = MACHINE_X - 32
TRUCK_X = 8

# Boss and Punishment coordinates
BOSS_Y = MACHINE_Y - 3
BOSS_MARIO = SCREEN_WIDTH - 16
BOSS_LUIGI = 0
PUNISH_MARIO_X = SCREEN_WIDTH - 30
PUNISH_LUIGI_X = 18

# Number of floors for each difficulty level
NUM_EASY_CRAZY = 5
NUM_MEDIUM = 7
NUM_EXTREME = 9

# Lists containing the Y position for each conveyor
FLOORS_EASY_CRAZY = []
for i in range(NUM_EASY_CRAZY):
    FLOORS_EASY_CRAZY.append(CONVEYOR_Y_START - (i * CONVEYOR_DISTANCE))

FLOORS_MEDIUM = []
for i in range(NUM_MEDIUM):
    FLOORS_MEDIUM.append(CONVEYOR_Y_START - (i * CONVEYOR_DISTANCE))

FLOORS_EXTREME = []
for i in range(NUM_EXTREME):
    FLOORS_EXTREME.append(CONVEYOR_Y_START - (i * CONVEYOR_DISTANCE))

# This list is used by characters to know where to stand on each floor
FLOOR_Y_LEVELS = [GROUND_START_Y]
for i in range(10):
    c_y = CONVEYOR_Y_START - (i * CONVEYOR_DISTANCE)
    # +2 to align the feet correctly
    FLOOR_Y_LEVELS.append(c_y + 2)

# Conveyor speeds
SLOW_SPEED = 1.0
MEDIUM_SPEED = 1.5
HIGH_SPEED = 2.0

# Difficulty progression rules
BONUS_REQUIRED_EASY = 3
BONUS_REQUIRED_MEDIUM = 5
BONUS_REQUIRED_EXTREME = 5
SPAWN_SCORE_THRESHOLD_EASY = 50
SPAWN_SCORE_THRESHOLD_MEDIUM = 30
SPAWN_SCORE_THRESHOLD_EXTREME = 30
SPAWN_SCORE_THRESHOLD_CRAZY = 20
INITIAL_PACKAGE_LIMIT = 1
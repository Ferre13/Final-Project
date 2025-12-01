# Executive Summary

The codebase has been refactored to better align with Object-Oriented principles, focusing on improving encapsulation, simplifying logic, and increasing clarity. The most significant change was dismantling the "God Object" nature of the `Board` class by decoupling it from the `PackageManager`. This change restores the `Board` to its intended role as an orchestrator, rather than a micromanager of other objects' internal states.

Additional refactoring includes moving state management logic into the classes responsible for that state (e.g., `Character.reset()`), simplifying complex methods, and improving the naming of constants and methods to be more descriptive and "student-like". These changes make the code easier to understand, maintain, and extend.

# Refactored Code

## Game/board.py
```python
import pyxel
import constants
from game_info import GameInfo
from package_manager import PackageManager

class Board:
    """
    The main game board that manages all game objects, game states,
    and the main update and draw loops. It orchestrates the game's logic.
    """
    def __init__(self, difficulty: str, objects: dict):
        """
        Initializes the game board with all necessary game objects.
        
        :param difficulty: A string representing the chosen difficulty.
        :param objects: A dictionary containing all pre-created game objects.
        """
        self.difficulty = difficulty
        
        # Unpack objects from the dictionary
        self.mario = objects.get("mario")
        self.luigi = objects.get("luigi")
        self.boss = objects.get("boss")
        self.door_left = objects.get("door_left")
        self.door_right = objects.get("door_right")
        self.truck = objects.get("truck")
        self.conveyors = objects.get("conveyors", [])
        self.platforms = objects.get("platforms", [])
        self.windows = objects.get("windows", [])
        self.machine = objects.get("machine")
        self.level_sign = objects.get("level_sign")
        self.exit_signal = objects.get("exit_signal")
        self.vertical_structure = objects.get("vertical_structure")
        
        # Initialize board state and logic handlers
        self.package_manager = PackageManager(self.conveyors, self.difficulty)
        self.init_configuration()

        # Define the order for drawing static components
        self.__drawables = [
            self.windows, self.machine, self.exit_signal, self.door_left,
            self.door_right, self.boss, self.platforms, self.conveyors,
            self.vertical_structure, self.level_sign, self.mario, self.luigi,
            self.truck
        ]

    def init_configuration(self):
        """Sets up the initial configuration and state of the board."""
        self.score = 0
        self.failures = 0
        self.punished_char = None
        self.deliveries_count = 0
        self.game_info = GameInfo()
        self.state = constants.PLAYING

    def reset_game(self):
        """ Resets all game state to initial values without recreating objects. """
        self.init_configuration()
        self.package_manager = PackageManager(self.conveyors, self.difficulty)
        self.truck.reset()
        self.mario.reset()
        self.luigi.reset()

    def handle_truck_bonus(self):
        """Checks if a bonus for successful deliveries should be awarded."""
        self.deliveries_count += 1

        if self.difficulty == "CRAZY":
            return

        bonus_requirements = {
            "EASY": constants.BONUS_REQUIRED_EASY,
            "MEDIUM": constants.BONUS_REQUIRED_MEDIUM,
            "EXTREME": constants.BONUS_REQUIRED_EXTREME
        }
        
        required = bonus_requirements.get(self.difficulty)
        
        if required and (self.deliveries_count % required == 0) and self.failures > 0:
            self.failures -= 1

    def initiate_punishment(self, character_name: str):
        """Activates the boss sequence for a character's failure."""
        if character_name == "Mario":
            self.punished_char = self.mario
            self.boss.appear("MARIO_FAIL")
        else:
            self.punished_char = self.luigi
            self.boss.appear("LUIGI_FAIL")
        
        self.punished_char.enter_punishment_mode()
        self.state = constants.BOSS_SEQUENCE

    def update(self):
        """
        The main update loop, which dispatches to other update methods
        based on the current game state.
        """
        state_updaters = {
            constants.PLAYING: self.__update_playing,
            constants.TRUCK_SEQUENCE: self.__update_truck_sequence,
            constants.BOSS_SEQUENCE: self.__update_boss_sequence,
            constants.GAME_OVER: self.__update_game_over
        }
        
        update_method = state_updaters.get(self.state)
        if update_method:
            update_method()
        
        # Global actions
        self.door_left.update()
        self.door_right.update()
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def __update_playing(self):
        """Handles game logic when the game is in the 'PLAYING' state."""
        results = self.package_manager.update(self.score, self.mario, self.luigi, self.truck)
        
        self.score += results["score_change"]
        self.failures += results["failures"]
        
        if results["new_state"]:
            self.state = results["new_state"]
            if results["truck_bonus"]:
                self.handle_truck_bonus()

        if self.failures >= constants.MAX_FAILURES:
            self.state = constants.GAME_OVER
        elif results["culprit"]:
            self.initiate_punishment(results["culprit"])

        self.mario.update()
        self.luigi.update()

    def __update_truck_sequence(self):
        """Handles the truck delivery animation sequence."""
        self.truck.update()
        if self.mario.state != constants.CHAR_STATE_REST1 and self.mario.state != constants.CHAR_STATE_REST2:
            self.mario.enter_rest_mode()
            self.luigi.enter_rest_mode()
        self.mario.update()
        self.luigi.update()

        if not self.truck.is_delivering:
            self.score += constants.POINTS_PER_TRUCK
            self.boss.appear("BREAK")
            self.state = constants.BOSS_SEQUENCE

    def __update_boss_sequence(self):
        """Handles the boss appearance animation (for failures or breaks)."""
        self.boss.update()
        if not self.boss.is_active:
            if self.punished_char:
                self.punished_char.exit_punishment_mode()
                self.punished_char = None
            self.mario.exit_rest_mode()
            self.luigi.exit_rest_mode()
            self.state = constants.PLAYING

    def __update_game_over(self):
        """Handles the game over screen and input for restarting."""
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
            self.state = constants.MAIN_MENU

    def draw(self):
        """
        The main draw loop, which dispatches to other draw methods
        based on the current game state.
        """
        pyxel.cls(0)

        if self.state == constants.GAME_OVER:
            self.__draw_game_over()
        else:
            self.__draw_playing()

    def __draw_playing(self):
        """Draws all the elements for the main game screen."""
        for component in self.__drawables:
            if isinstance(component, list):
                for item in component:
                    if item: item.draw()
            elif component:
                component.draw()

        for p in self.package_manager.packages:
            p.draw()

        # HUD is drawn on top of everything
        self.game_info.draw_score(self.score)
        self.game_info.draw_lives(self.failures)

    def __draw_game_over(self):
        """Draws the game over screen."""
        sprite = constants.GAME_OVER_SPRITE
        img_w = sprite[3]
        img_h = sprite[4]
        x_img = (constants.SCREEN_WIDTH - img_w) / 2
        y_img = (constants.SCREEN_HEIGHT - img_h) / 2 - 10

        pyxel.blt(x_img, y_img, *sprite)

        score_y = y_img + img_h + 5
        score_str = str(self.score)
        score_w = len(score_str) * 4
        score_x = (constants.SCREEN_WIDTH - score_w) / 2
        self.game_info.draw_score(self.score, score_x, score_y)

        restart_text = "PRESS SPACE TO RETURN TO MENU"
        text_w = len(restart_text) * 4
        text_x = (constants.SCREEN_WIDTH - text_w) / 2
        pyxel.text(text_x, score_y + 10, restart_text, 7)
```

## Game/package_manager.py
```python
import constants
from package import Package

class PackageManager:
    """
    Manages all logic related to packages, including spawning, updating,
    and handling transfers and failures.
    """
    def __init__(self, conveyors: list, difficulty: str):
        """
        Initializes the package manager.
        
        :param conveyors: A list of the conveyor belt objects.
        :param difficulty: The game difficulty setting.
        """
        self.conveyors = conveyors
        self.difficulty = difficulty
        self.packages = []
        self.spawn_timer = 0

    def update(self, score: int, mario, luigi, truck) -> dict:
        """
        The main update method for all package-related logic.
        
        :param score: The current game score.
        :param mario: The Mario character object.
        :param luigi: The Luigi character object.
        :param truck: The Truck object.
        :return: A dictionary with the results of the update cycle.
        """
        self.spawn_timer += 1
        self.__spawn_package(score)
        
        results = {
            "failures": 0,
            "score_change": 0,
            "new_state": None,
            "culprit": None,
            "truck_bonus": False
        }
        
        self.__update_packages(mario, luigi, truck, results)
        
        return results

    def __calculate_max_packages(self, score: int) -> int:
        """Calculates the maximum number of packages allowed on screen based on score."""
        limit = constants.INITIAL_PACKAGE_LIMIT
        
        thresholds = {
            "EASY": constants.SPAWN_SCORE_THRESHOLD_EASY,
            "MEDIUM": constants.SPAWN_SCORE_THRESHOLD_MEDIUM,
            "EXTREME": constants.SPAWN_SCORE_THRESHOLD_EXTREME,
            "CRAZY": constants.SPAWN_SCORE_THRESHOLD_CRAZY
        }
        
        threshold = thresholds.get(self.difficulty, 1) # Default to 1 to avoid division by zero
        if threshold > 0:
            limit += (score // threshold)
            
        return limit

    def __spawn_package(self, score: int):
        """Handles the logic for spawning new packages onto the first conveyor."""
        max_packages = self.__calculate_max_packages(score)
        
        if self.conveyors and len(self.packages) < max_packages:
            if not self.packages or self.spawn_timer > constants.SPAWN_TIMER_GAP:
                new_pck = Package(self.difficulty, self.conveyors[0], 0)
                self.packages.append(new_pck)
                self.spawn_timer = 0

    def __update_packages(self, mario, luigi, truck, results: dict):
        """
        Updates all packages, checks their status, and tells the characters
        when to start their transfer animations.
        """
        for p in self.packages[:]:
            # Check if a character should start a transfer animation
            char_to_animate = None
            if mario.can_receive_package(p.floor_index):
                char_to_animate = mario
            elif luigi.can_receive_package(p.floor_index):
                char_to_animate = luigi
            
            if char_to_animate:
                distance_to_end = 0
                direction = p.current_conveyor.direction
                speed = p.current_conveyor.speed
                if direction == 1:
                    distance_to_end = p.current_conveyor.end_x - (p.x + p.width)
                else:
                    distance_to_end = p.x - p.current_conveyor.x
                
                if speed > 0 and (distance_to_end / speed) <= constants.TRANSFER_ANIMATION_TIME:
                    char_to_animate.start_transfer_animation()

            # Update package and handle its status
            status = p.update()
            
            if status == constants.PKG_STATUS_REACHED_END:
                self.__handle_package_transfer(p, mario, luigi, truck, results)
            elif status == constants.PKG_STATUS_FALLEN_MARIO:
                self.__handle_failure(p, "Mario", results)
            elif status == constants.PKG_STATUS_FALLEN_LUIGI:
                self.__handle_failure(p, "Luigi", results)

    def __handle_failure(self, p: Package, culprit: str, results: dict):
        """Handles the consequences of a package falling."""
        self.packages.remove(p)
        results["failures"] += 1
        results["culprit"] = culprit

    def __handle_package_transfer(self, p: Package, mario, luigi, truck, results: dict):
        """
        Handles the logic for transferring a package between conveyors or to the truck.
        """
        is_mario_turn = mario.floor == p.floor_index and p.floor_index % 2 == 0
        is_luigi_turn = luigi.floor == p.floor_index and p.floor_index % 2 != 0
        can_transfer = is_mario_turn or is_luigi_turn

        if can_transfer:
            next_idx = p.floor_index + 1
            
            if next_idx < len(self.conveyors):
                p.advance_to_conveyor(self.conveyors[next_idx])
                results["score_change"] += constants.POINTS_PER_PACKAGE
            else:
                if truck.receive_package():
                    results["new_state"] = constants.TRUCK_SEQUENCE
                    results["truck_bonus"] = True
                self.packages.remove(p)
                results["score_change"] += constants.POINTS_PER_PACKAGE
        else:
            p.fall()
```

## Game/characters.py
```python
import pyxel
import constants

class Character:
    """
    Represents a player character (Mario or Luigi), responsible for its own state,
    movement, and drawing. It handles user input and character-specific logic
    like being in a "punished" or "resting" state.
    """
    def __init__(self, name: str, x: int, difficulty: str, num_floors: int):
        """
        Initializes a character.

        :param name: The name of the character ("Mario" or "Luigi").
        :param x: The initial x-coordinate.
        :param difficulty: The game difficulty, used for input handling.
        :param num_floors: The total number of floors in the level.
        """
        self.__name = name
        self.x = x
        self.__difficulty = difficulty
        
        self.y = 0
        self.state = constants.CHAR_STATE_STATIC
        self.original_x = x 
        self.rest_timer = 0
        self.floor = 0
        self.transfer_timer = 0
        
        # The maximum floor index the character can be on.
        self.max_floor_index = num_floors

        if self.name == "Mario":
            self.floor = 0
        else:
            self.floor = 1

    @property
    def x(self) -> int: return self.__x
    @x.setter
    def x(self, value):
        if not isinstance(value, int): raise TypeError("x must be int")
        self.__x = value

    @property
    def y(self) -> int: return self.__y
    @y.setter
    def y(self, value):
        if not isinstance(value, int): raise TypeError("y must be int")
        self.__y = value

    @property
    def floor(self) -> int: return self.__floor
    @floor.setter
    def floor(self, value: int):
        if not isinstance(value, int): raise TypeError("floor must be int")
        self.__floor = value

    @property
    def name(self) -> str: return self.__name
    
    @property
    def width(self) -> int:
        """Returns the width of the character's static sprite."""
        return constants.MARIO_STATIC[3]

    @property
    def height(self) -> int:
        """Returns the height of the character's static sprite."""
        return constants.MARIO_STATIC[4]

    @property
    def state(self) -> int: return self.__state
    @state.setter
    def state(self, value: int):
        if not isinstance(value, int): raise TypeError("state must be int")
        self.__state = value

    @property
    def __sprites(self) -> list:
        """Returns the appropriate list of sprites based on the character's name."""
        if self.name == "Mario":
            return constants.MARIO_SPRITES
        else:
            return constants.LUIGI_SPRITES

    @property
    def key_up(self) -> int:
        """Returns the appropriate 'up' key based on the character's name."""
        if self.name == "Mario":
            return pyxel.KEY_UP
        else:
            return pyxel.KEY_W

    @property
    def key_down(self) -> int:
        """Returns the appropriate 'down' key based on the character's name."""
        if self.name == "Mario":
            return pyxel.KEY_DOWN
        else:
            return pyxel.KEY_S

    def can_receive_package(self, package_floor: int) -> bool:
        """
        Checks if the character is in the correct position and state to receive a package.
        """
        if self.state != constants.CHAR_STATE_STATIC or self.floor != package_floor:
            return False
        
        is_mario_turn = self.name == "Mario" and package_floor % 2 == 0
        is_luigi_turn = self.name == "Luigi" and package_floor % 2 != 0
        
        return is_mario_turn or is_luigi_turn

    def move_up(self):
        """Moves the character up by two floors if possible."""
        next_floor = self.floor + 2
        if next_floor <= self.max_floor_index:
            self.floor = next_floor

    def move_down(self):
        """Moves the character down by two floors if possible."""
        next_floor = self.floor - 2
        if next_floor >= 0:
            self.floor = next_floor

    def enter_rest_mode(self):
        """Puts the character into the resting state (during truck sequence)."""
        self.state = constants.CHAR_STATE_REST1
        self.rest_timer = 0

    def exit_rest_mode(self):
        """Takes the character out of the resting state."""
        self.state = constants.CHAR_STATE_STATIC
        self.update() 

    def enter_punishment_mode(self):
        """Puts the character into the punishment state (after a failure)."""
        self.state = constants.CHAR_STATE_PUNISHED
        if self.name == "Mario": self.x = constants.PUNISH_MARIO_X
        else: self.x = constants.PUNISH_LUIGI_X
        self.__update_physics_boss()

    def exit_punishment_mode(self):
        """Takes the character out of the punishment state."""
        self.state = constants.CHAR_STATE_STATIC
        self.x = self.original_x
        self.update()

    def reset(self):
        """Resets the character to its initial state and position."""
        self.state = constants.CHAR_STATE_STATIC
        self.x = self.original_x
        if self.name == "Mario":
            self.floor = 0
        else:
            self.floor = 1
        self.update()

    def start_transfer_animation(self):
        """Starts the two-part package transfer animation if the character is static."""
        if self.state == constants.CHAR_STATE_STATIC:
            self.state = constants.CHAR_STATE_TRANSFER_ANIM
            self.transfer_timer = constants.TRANSFER_ANIMATION_TIME * 2

    def __animate_rest(self):
        """Animates the character while in the resting state."""
        self.rest_timer += 1
        offset = (self.rest_timer // 15) % 2
        self.state = constants.CHAR_STATE_REST1 + offset

    def __update_physics_floor(self):
        """Calculates the character's y-position based on their current floor."""
        sprite_index = self.state
        if self.state == constants.CHAR_STATE_TRANSFER_ANIM:
            # For height calculation, use the 'has package' sprite as it's the tallest.
            sprite_index = constants.CHAR_STATE_HAS_PACKAGE
            
        current_sprite = self.__sprites[sprite_index]
        sprite_h = current_sprite[4]
        safe_floor = min(self.floor, len(constants.FLOOR_Y_LEVELS) - 1)
        self.y = constants.FLOOR_Y_LEVELS[safe_floor] - sprite_h

    def __update_physics_boss(self):
        """Calculates the character's y-position when in the boss area."""
        boss_sprite_h = self.__sprites[self.state][4]
        self.y = constants.BOSS_Y - boss_sprite_h

    def __handle_player_input(self):
        """Checks for and processes player input for movement."""
        up_pressed = pyxel.btnp(self.key_up)
        down_pressed = pyxel.btnp(self.key_down)

        if self.__difficulty == "CRAZY":
            up_pressed, down_pressed = down_pressed, up_pressed

        if up_pressed:
            self.state = constants.CHAR_STATE_STATIC
            self.move_up()
        elif down_pressed:
            self.state = constants.CHAR_STATE_STATIC
            self.move_down()
        
        elif self.state == constants.CHAR_STATE_TRANSFER_ANIM:
            self.transfer_timer -= 1
            if self.transfer_timer <= 0:
                self.state = constants.CHAR_STATE_STATIC

    def update(self):
        """Main update method for the character."""
        # State-specific logic that cannot be interrupted by player input.
        state_handlers = {
            constants.CHAR_STATE_REST1: self.__animate_rest,
            constants.CHAR_STATE_REST2: self.__animate_rest,
        }
        
        handler = state_handlers.get(self.state)
        if handler:
            handler()
        elif self.state != constants.CHAR_STATE_PUNISHED:
            self.__handle_player_input()

        # Update physics based on the final state for this frame.
        if self.state == constants.CHAR_STATE_PUNISHED:
            self.__update_physics_boss()
        else:
            self.__update_physics_floor()

    def draw(self):
        """Draws the character's current sprite at its x, y position."""
        sprite_index = self.state
        draw_w_mod = 1 # Used to flip sprite horizontally

        if self.state == constants.CHAR_STATE_TRANSFER_ANIM:
            # First half of animation: show "getting ready" sprite.
            if self.transfer_timer > constants.TRANSFER_ANIMATION_TIME:
                if self.name == "Mario" and self.floor == 0:
                    sprite_index = constants.CHAR_STATE_HAS_PACKAGE
                    draw_w_mod = -1 # Flipped
                else:
                    sprite_index = constants.CHAR_STATE_GETTING_PACKAGE
            # Second half of animation: show "has package" sprite.
            else:
                sprite_index = constants.CHAR_STATE_HAS_PACKAGE
        
        elif self.name == "Mario" and self.floor == 0 and self.state == constants.CHAR_STATE_STATIC:
             draw_w_mod = -1
             
        img, u, v, w, h, colkey = self.__sprites[sprite_index]
        pyxel.blt(self.x, self.y, img, u, v, w * draw_w_mod, h, colkey)
```

## Game/constants.py
```python
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 128
SPRITES_FILE = "assets/my_resource.pyxres"

TRUCK_WAIT_TIME = 60          # frames the truck waits before moving
TRUCK_OFFSCREEN_TIME = 30     # frames the truck stays off-screen
TRUCK_SPEED = 2               # pixels per frame
BOSS_YELL_DURATION = 60       # frames
DOOR_ANIMATION_SPEED = 10     # frames
SPAWN_TIMER_GAP = 45          # Minimum frames between package spawns
TRANSFER_ANIMATION_TIME = 18  # Frames for the character's package transfer animation

POINTS_PER_PACKAGE = 1
POINTS_PER_TRUCK = 10
MAX_FAILURES = 3
TRUCK_MAX_CAPACITY = 8
INITIAL_PACKAGE_LIMIT = 1

BONUS_REQUIRED_EASY = 3
BONUS_REQUIRED_MEDIUM = 5
BONUS_REQUIRED_EXTREME = 5

SPAWN_SCORE_THRESHOLD_EASY = 50
SPAWN_SCORE_THRESHOLD_MEDIUM = 30
SPAWN_SCORE_THRESHOLD_EXTREME = 30
SPAWN_SCORE_THRESHOLD_CRAZY = 20

PACKAGE_FALL_SPEED = 2
OVERHANG_LIMIT = 5            # pixels a package can hang over an edge before falling
GROUND_HEIGHT_PX = 6
GROUND_START_Y = SCREEN_HEIGHT - GROUND_HEIGHT_PX

CHAR_STATE_STATIC = 0
CHAR_STATE_GETTING_PACKAGE = 1
CHAR_STATE_HAS_PACKAGE = 2
CHAR_STATE_PUNISHED = 3
CHAR_STATE_REST1 = 4
CHAR_STATE_REST2 = 5
CHAR_STATE_TRANSFER_ANIM = 6

PKG_STATE_MOVING = "moving"
PKG_STATE_FALLING = "falling"

PKG_STATUS_MOVING = 0
PKG_STATUS_REACHED_END = 1
PKG_STATUS_FALLEN_LUIGI = 2 
PKG_STATUS_FALLEN_MARIO = 3 

BOSS_STATE_IDLE = 0
BOSS_STATE_OPENING = 1
BOSS_STATE_YELLING = 2
BOSS_STATE_CLOSING = 3

DOOR_STATE_CLOSED = "closed"
DOOR_STATE_OPENING = "opening"
DOOR_STATE_OPEN = "open"
DOOR_STATE_CLOSING = "closing"

MARIO_STATIC = (0, 36, 2, 10, 14, 0)
MARIO_WAIT = (0, 35, 18, 13, 14, 0)
MARIO_PCK = (0, 36, 33, 12, 15, 0)
MARIO_BOSS = (0, 35, 50, 10, 14, 0)
MARIO_REST1 = (0, 33, 66, 13, 13, 0)
MARIO_REST2 = (0, 33, 83, 14, 12, 0)
MARIO_SPRITES = [MARIO_STATIC, MARIO_WAIT, MARIO_PCK, MARIO_BOSS, MARIO_REST1, MARIO_REST2]

LUIGI_STATIC = (0, 52, 1, 10, 15, 0)  
LUIGI_WAIT = (0, 50, 17, 13, 15, 0)  
LUIGI_PCK = (0, 50, 33, 13, 15, 0)  
LUIGI_BOSS = (0, 51, 50, 10, 14, 0)
LUIGI_REST1 = (0, 50, 66, 13, 13, 0)
LUIGI_REST2 = (0, 49, 83, 14, 12, 0)
LUIGI_SPRITES = [LUIGI_STATIC, LUIGI_WAIT, LUIGI_PCK, LUIGI_BOSS, LUIGI_REST1, LUIGI_REST2]

BOSS_1 = (0, 32, 96, 16, 16, 0)
BOSS_2 = (0, 48, 96, 16, 16, 0)

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

PCK_EASY_SPRITES = [PCK_LVL1, PCK_LVL1_FALL, PCK_LVL3, PCK_LVL3_FALL, PCK_LVL5, PCK_LVL5_FALL, PCK_LVL7, PCK_LVL7_FALL, PCK_LVL9, PCK_LVL9_FALL, PCK_LVL10, PCK_LVL10_FALL]
PCK_MEDIUM_SPRITES = [PCK_LVL1, PCK_LVL1_FALL, PCK_LVL2, PCK_LVL2_FALL, PCK_LVL3, PCK_LVL3_FALL, PCK_LVL5, PCK_LVL5_FALL, PCK_LVL7, PCK_LVL7_FALL, PCK_LVL8, PCK_LVL8_FALL, PCK_LVL9, PCK_LVL9_FALL, PCK_LVL10, PCK_LVL10_FALL]
PCK_EXTREME_SPRITES = [PCK_LVL1, PCK_LVL1_FALL, PCK_LVL2, PCK_LVL2_FALL, PCK_LVL3, PCK_LVL3_FALL, PCK_LVL4, PCK_LVL4_FALL, PCK_LVL5, PCK_LVL5_FALL, PCK_LVL6, PCK_LVL6_FALL, PCK_LVL7, PCK_LVL7_FALL, PCK_LVL8, PCK_LVL8_FALL, PCK_LVL9, PCK_LVL9_FALL, PCK_LVL10, PCK_LVL10_FALL]
PCK_CRAZY_SPRITES = PCK_EASY_SPRITES

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

CONVEYOR_SPRITE = (0, 32, 154, 32, 4, 0)  
PLATFORM_SPRITE = (0, 15, 187, 17, 19, 0)
FLOOR_SPRITE = (1, 33, 34, 8, 2, 0)
EXIT_SIGNAL_SPRITE = (0, 32, 128, 16, 7, 0)
VERTICAL_STRUCTURE_SPRITE = (1, 18, 17, 12, 35, 1)
MACHINE_SPRITE = (1, 32, 17, 14, 13, 0)
WINDOW_SPRITE = (1, 18, 2, 32, 12, 0)
DOOR_CLOSED = (0, 32, 136, 16, 16, 0)
DOOR_OPENING = (0, 48, 136, 16, 16, 0)
DOOR_OPEN = (0, 48, 120, 16, 16, 0)
DOOR_SPRITES = {'closed': DOOR_CLOSED, 'opening': DOOR_OPENING, 'open': DOOR_OPEN, 'closing': DOOR_OPENING}

LEVEL_EASY = (0, 33, 160, 15, 5, 0) 
LEVEL_MEDIUM = (0, 32, 166, 21, 5, 0)
LEVEL_EXTREME = (0, 32, 172, 27, 5, 0) 
LEVEL_CRAZY = (0, 32, 178, 19, 5, 0)
GAME_OVER_SPRITE = (2, 0, 0, 62, 36, 0)

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
LIFE_SPRITE = (0, 32, 112, 16, 16, 0)

SCORE_X = SCREEN_WIDTH - 20
SCORE_Y = 3
LIVES_X = SCREEN_WIDTH // 2 - 28
LIVES_Y = 1

CONVEYOR_Y_START = SCREEN_HEIGHT - 16
CONVEYOR_DISTANCE = 11      # Vertical distance between conveyor belts
CONVEYOR_SEGMENTS = 4       # Number of sprite segments making up a conveyor's length
CONVEYOR_SPRITE_W = CONVEYOR_SPRITE[3]
CONVEYOR_TOTAL_WIDTH_PX = CONVEYOR_SEGMENTS * CONVEYOR_SPRITE_W
CONVEYOR_X_START = SCREEN_WIDTH // 2 - (CONVEYOR_TOTAL_WIDTH_PX // 2)

CENTER_SCREEN = SCREEN_WIDTH // 2
STRUCT_WIDTH_PX = VERTICAL_STRUCTURE_SPRITE[3] * 2
STRUCT_X = CENTER_SCREEN - (STRUCT_WIDTH_PX // 2)

LUIGI_X = 45
MARIO_X = 194
MACHINE_X = SCREEN_WIDTH - 14
MACHINE_Y = SCREEN_HEIGHT - 24 
CONVEYOR_0_X = MACHINE_X - 32
TRUCK_X = 8

BOSS_Y = MACHINE_Y - 3
BOSS_MARIO = SCREEN_WIDTH - 16
BOSS_LUIGI = 0
PUNISH_MARIO_X = SCREEN_WIDTH - 30
PUNISH_LUIGI_X = 18

NUM_EASY_CRAZY = 5
NUM_MEDIUM = 7
NUM_EXTREME = 9

# Dynamically calculate the Y position for each conveyor floor
FLOORS_EASY_CRAZY = []
for i in range(NUM_EASY_CRAZY):
    FLOORS_EASY_CRAZY.append(CONVEYOR_Y_START - (i * CONVEYOR_DISTANCE))

FLOORS_MEDIUM = []
for i in range(NUM_MEDIUM):
    FLOORS_MEDIUM.append(CONVEYOR_Y_START - (i * CONVEYOR_DISTANCE))

FLOORS_EXTREME = []
for i in range(NUM_EXTREME):
    FLOORS_EXTREME.append(CONVEYOR_Y_START - (i * CONVEYOR_DISTANCE))

# This list is used by characters to know where their feet should be on each floor
FLOOR_Y_LEVELS = [GROUND_START_Y]
for y in FLOORS_EXTREME:
    FLOOR_Y_LEVELS.append(y + 2)

# Conveyor speeds
SLOW_SPEED = 1.0
MEDIUM_SPEED = 1.5
HIGH_SPEED = 2.0

# Game states
PLAYING = "playing"
TRUCK_SEQUENCE = "truck_sequence"
BOSS_SEQUENCE = "boss_sequence"
GAME_OVER = "game_over"
MAIN_MENU = "main_menu"
```

# Change Log

| File | Change | Reasoning |
| --- | --- | --- |
| `Game/package_manager.py` | Decoupled from `Board` class. | The class previously held a direct reference to the `Board`, allowing it to modify board state directly. This violated encapsulation. It now receives necessary data via its `update` method and returns a dictionary of results, making it a self-contained manager. |
| `Game/board.py` | Updated to work with the new `PackageManager` interface. | The `Board` now passes data to the `PackageManager` and processes the results, acting as a true orchestrator of game state. |
| `Game/characters.py` | Added a `reset()` method. | The logic for resetting a character's state was moved from the `Board` into the `Character` class itself, improving encapsulation. |
| `Game/board.py` | Refactored `reset_game()` to call `character.reset()`. | This simplifies the `Board`'s code and respects the `Character`'s ownership of its own state. |
| `Game/board.py` | Renamed `active_punishment` to `initiate_punishment`. | The new name more accurately reflects that the method starts the punishment sequence. |
| `Game/constants.py` | Renamed `CHAR_STATE` constants. | Names like `CHAR_STATE_PCK` were ambiguous. They have been renamed to more descriptive names like `CHAR_STATE_HAS_PACKAGE` for better readability. |
| `Game/characters.py` | Updated to use the new `CHAR_STATE` constant names. | Propagated the constant name changes throughout the file. |
| `Game/board.py` | Simplified `handle_truck_bonus()` and drawing logic. | Used a dictionary to clean up conditional logic for bonuses and created a `drawables` list to make the rendering order explicit and the draw loop cleaner. |
| `Game/characters.py` | Simplified `can_receive_package()` and `update()` methods. | Refactored complex conditional logic to be flatter and more readable. Used a dictionary to handle state-based updates. |
| All files | Cleaned up comments and docstrings. | Removed visual clutter and made comments more direct and functional. |

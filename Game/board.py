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
        for p in self.package_manager.packages:
            p.draw()
        
        for component in self.__drawables:
            if isinstance(component, list):
                for item in component:
                    if item: item.draw()
            elif component:
                component.draw()

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
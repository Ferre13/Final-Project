import pyxel
import constants
from factory import Factory
from game_info import GameInfo
from menu import Menu
from package_manager import PackageManager
from character import Character

class Game:
    """Manages the main game state, objects, and game loops."""
    def __init__(self):
        """Initializes the game window and core components."""
        pyxel.init(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, title="Super Package Bros.", fps = 30)
        pyxel.load(constants.SPRITES_FILE)
        
        self.game_info = GameInfo()
        self.menu = Menu()
        self.state = constants.MAIN_MENU
        self.difficulty = "EASY"

        # We initialize all attributes to None (or empty lists) for clarity. We group them to shorten the init method.
        self.factory = self.package_manager = None
        self.mario = self.luigi = self.boss = self.truck = None
        self.door_left = self.door_right = None
        self.machine = self.level_sign = self.exit_signal = self.vertical_structure = None
        self.punished_char = None
        self.windows = []
        self.platforms = []
        self.conveyors = []
        self.score = self.failures = self.deliveries_count = 0

        # State management dictionaries. Define here to avoid calculating them every frame
        self.__state_updaters = {constants.MAIN_MENU: self.__update_main_menu, constants.PLAYING: self.__update_playing,
                                 constants.TRUCK_SEQUENCE: self.__update_truck_sequence, constants.BOSS_SEQUENCE: self.__update_boss_sequence,
                                 constants.GAME_OVER: self.__update_game_over}
        self.__state_drawers = {constants.MAIN_MENU: self.menu.draw, constants.PLAYING: self.__draw_playing, constants.TRUCK_SEQUENCE: self.__draw_playing,
                                constants.BOSS_SEQUENCE: self.__draw_playing, constants.GAME_OVER: self.__draw_game_over}

    def start_game(self):
        """Creates all game objects and resets game state variables."""
        self.factory = Factory(self.difficulty)
        self.factory.create_all_objects()
        # Assign all game objects from the factory to local attributes for easier access
        self.mario = self.factory.mario
        self.luigi = self.factory.luigi
        self.boss = self.factory.boss
        self.door_left = self.factory.door_left
        self.door_right = self.factory.door_right
        self.truck = self.factory.truck
        self.windows = self.factory.windows
        self.platforms = self.factory.platforms
        self.conveyors = self.factory.conveyors
        self.machine = self.factory.machine
        self.level_sign = self.factory.level_sign
        self.exit_signal = self.factory.exit_signal
        self.vertical_structure = self.factory.vertical_structure
        # Create the package manager with the conveyors and difficulty
        self.package_manager = PackageManager(self.conveyors, self.difficulty)
        
        # Reset game state variables
        self.score = 0
        self.failures = 0
        self.punished_char = None
        self.deliveries_count = 0
        self.state = constants.PLAYING

    def handle_truck_bonus(self):
        """Removes a failure point if enough deliveries have been made."""
        self.deliveries_count += 1

        bonus_requirements = {"EASY": constants.BONUS_REQUIRED_EASY, "MEDIUM": constants.BONUS_REQUIRED_MED_EXTREME, "EXTREME": constants.BONUS_REQUIRED_MED_EXTREME}
        required = bonus_requirements.get(self.difficulty)
        # We check if required is not None (for CRAZY difficulty it is None)
        if required and (self.deliveries_count % required == 0) and self.failures > 0:
            self.failures -= 1

    def initiate_punishment(self, culprit: Character):
        """
        Starts the boss punishment sequence for a failed character.
        :param culprit: The character object that failed.
        """
        self.punished_char = culprit
        self.boss.appear_for_fail(culprit)
        self.punished_char.enter_punishment_mode()
        self.state = constants.BOSS_SEQUENCE

    def update(self):
        """The main update loop, called by Pyxel every frame."""
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        self.__state_updaters[self.state]()

    def __update_main_menu(self):
        """Handles user input on the main menu."""
        selected_difficulty = self.menu.update()
        if selected_difficulty:
            self.difficulty = selected_difficulty
            self.start_game()

    def __process_package_results(self, results: dict):
        """
        Processes the results from package updates, adjusting score, failures, and game state as needed.
        :param results: A dictionary containing score, failures, and state changes.
        """
        self.score += results["score_change"]
        self.failures += results["failures"]
        if results["new_state"]:
            self.state = results["new_state"]
            if self.state == constants.TRUCK_SEQUENCE:
                self.package_manager.clear_top_floor_packages()
            if results["truck_bonus"]:
                self.handle_truck_bonus()
        if self.failures >= constants.MAX_FAILURES:
            self.state = constants.GAME_OVER
        elif results["culprit"]:
            self.initiate_punishment(results["culprit"])

    def __update_playing(self):
        """Handles the main game logic when the game is active."""
        results = self.package_manager.update(self.score, self.mario, self.luigi, self.truck)
        self.__process_package_results(results)
        self.mario.update()
        self.luigi.update()
        self.door_left.update()
        self.door_right.update()

    def __update_truck_sequence(self):
        """Handles the truck delivery animation."""
        self.package_manager.update_falling_packages()
        self.truck.update()
        self.door_left.update()
        self.door_right.update()

        if self.mario.state not in [constants.CHAR_STATE_REST1, constants.CHAR_STATE_REST2]:
            self.mario.enter_rest_mode()
            self.luigi.enter_rest_mode()
        self.mario.update()
        self.luigi.update()

        if not self.truck.is_delivering:
            self.score += constants.POINTS_PER_TRUCK
            self.boss.appear_for_break()
            self.state = constants.BOSS_SEQUENCE

    def __update_boss_sequence(self):
        """Handles the boss appearance animation."""
        self.package_manager.update_falling_packages()
        self.boss.update()
        self.door_left.update()
        self.door_right.update()

        if not self.boss.is_active:
            # If there was a punished character, exit their punishment mode
            if self.punished_char:
                self.punished_char.exit_punishment_mode()
                self.punished_char = None
            # Exit rest mode for both characters
            self.mario.exit_rest_mode()
            self.luigi.exit_rest_mode()
            self.state = constants.PLAYING

    def __update_game_over(self):
        """Handles the game over screen."""
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.state = constants.MAIN_MENU

    def draw(self):
        """The main draw loop, called by Pyxel every frame."""
        pyxel.cls(0)
        self.__state_drawers[self.state]()

    def __draw_playing(self):
        """Draws all game elements in the correct order."""
        for w in self.windows: 
            w.draw()
        self.machine.draw()
        self.level_sign.draw()
        self.exit_signal.draw()
        self.door_left.draw()
        self.door_right.draw()
        self.package_manager.draw()
        for p in self.platforms: 
            p.draw()
        for c in self.conveyors: 
            c.draw()
        self.truck.draw()
        self.mario.draw()
        self.luigi.draw()
        self.boss.draw()
        self.vertical_structure.draw()
        self.game_info.draw_score(self.score)
        self.game_info.draw_lives(self.failures)

    def __draw_game_over(self):
        """Draws the game over screen."""
        sprite = constants.GAME_OVER_SPRITE
        img, u, v, w, h, colkey = sprite
        
        x_img = (constants.SCREEN_WIDTH - w) / 2
        y_img = (constants.SCREEN_HEIGHT - h) / 2 + constants.GAME_OVER_Y_OFFSET
        pyxel.blt(x_img, y_img, img, u, v, w, h, colkey)

        score_y = y_img + h + constants.GAME_OVER_SCORE_Y_OFFSET
        score_str = str(self.score)
        score_w = len(score_str) * 4
        score_x = (constants.SCREEN_WIDTH - score_w) / 2
        self.game_info.draw_score(self.score, score_x, score_y)

        restart_text = "PRESS SPACE TO RETURN TO MENU"
        text_w = len(restart_text) * 4
        text_x = (constants.SCREEN_WIDTH - text_w) / 2
        pyxel.text(text_x, score_y + constants.GAME_OVER_RESTART_Y_OFFSET, restart_text, constants.TEXT_COLOR)
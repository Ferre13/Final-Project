import pyxel
import constants

from factory import Factory
from game_info import GameInfo
from menu import Menu

# Import all individual game object classes
from character import Character
from boss import Boss
from door import Door
from truck import Truck
from package_manager import PackageManager
from game_platform import Platform
from conveyor import Conveyor
from exit_signal import ExitSignal
from machine import Machine
from window import Window
from level_sign import LevelSign
from vertical_structure import VerticalStructure


class Game:
    """
    The main game class that orchestrates all game objects, states,
    and the main update and draw loops. It integrates logic from the
    original Board, Menu, and GameInfo classes.
    """
    def __init__(self):
        pyxel.init(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, title="Super Package Bros.", fps=30)
        pyxel.load(constants.SPRITES_FILE)
        
        self.game_info = GameInfo()
        self.menu = Menu()
        self.state = constants.MAIN_MENU
        self.difficulty = "EASY" # Default difficulty

        self.factory = None
        self.mario = None
        self.luigi = None
        self.boss = None
        self.door_left = None
        self.door_right = None
        self.truck = None
        self.conveyors = []
        self.platforms = []
        self.windows = []
        self.machine = None
        self.level_sign = None
        self.exit_signal = None
        self.vertical_structure = None
        self.package_manager = None

        self.score = 0
        self.failures = 0
        self.punished_char = None
        self.deliveries_count = 0

    def reset_game(self):
        """
        Resets all game state to initial values and recreates game objects
        based on the current difficulty.
        """
        self.factory = Factory(self.difficulty)

        # Create background elements
        self.windows, self.machine, self.level_sign = self.factory.create_background_elements()
        
        # Create world elements
        self.truck, self.exit_signal, self.vertical_structure, \
        self.platforms, self.conveyors = self.factory.create_world_elements()
        
        # Create characters and boss
        self.mario, self.luigi, self.boss, \
        self.door_left, self.door_right = self.factory.create_characters_and_boss()

        self.package_manager = PackageManager(self.conveyors, self.difficulty)
        
        self.score = 0
        self.failures = 0
        self.punished_char = None
        self.deliveries_count = 0
        self.state = constants.PLAYING

    def handle_truck_bonus(self):
        """Checks if a bonus for successful deliveries should be awarded."""
        self.deliveries_count += 1

        if self.difficulty == "CRAZY":
            return

        bonus_requirements = {
            "EASY": constants.BONUS_REQUIRED_EASY,
            "MEDIUM": constants.BONUS_REQUIRED_MED_EXTREME,
            "EXTREME": constants.BONUS_REQUIRED_MED_EXTREME
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
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        state_updaters = {
            constants.MAIN_MENU: self.__update_main_menu,
            constants.PLAYING: self.__update_playing,
            constants.TRUCK_SEQUENCE: self.__update_truck_sequence,
            constants.BOSS_SEQUENCE: self.__update_boss_sequence,
            constants.GAME_OVER: self.__update_game_over
        }
        
        update_method = state_updaters.get(self.state)
        if update_method:
            update_method()
        
        # Update elements that might need to run regardless of game state transitions
        if self.door_left:
            self.door_left.update()
        if self.door_right:
            self.door_right.update()

    def __update_main_menu(self):
        """Handles logic when in the main menu state."""
        selected_difficulty = self.menu.update()
        if selected_difficulty:
            self.difficulty = selected_difficulty
            self.reset_game()

    def __update_playing(self):
        """Handles game logic when the game is in the 'PLAYING' state."""
        results = self.package_manager.update(self.score, self.mario, self.luigi, self.truck)
        
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

        self.mario.update()
        self.luigi.update()

    def __update_truck_sequence(self):
        """Handles the truck delivery animation sequence."""
        self.truck.update()
        # Keep characters in rest mode during truck sequence
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

        state_drawers = {
            constants.MAIN_MENU: self.__draw_main_menu,
            constants.PLAYING: self.__draw_playing,
            constants.TRUCK_SEQUENCE: self.__draw_playing, # Truck sequence draws similarly to playing state
            constants.BOSS_SEQUENCE: self.__draw_playing,  # Boss sequence draws similarly to playing state
            constants.GAME_OVER: self.__draw_game_over
        }
        
        draw_method = state_drawers.get(self.state)
        if draw_method:
            draw_method()

    def __draw_main_menu(self):
        """Draws the main menu."""
        self.menu.draw()

    def __draw_playing(self):
        """Draws all the elements for the main game screen."""
        # Draw packages first, so they are below everything else
        self.package_manager.draw()

        # Draw background elements
        for w in self.windows: w.draw()
        self.machine.draw()
        self.level_sign.draw()
        self.exit_signal.draw()
        self.door_left.draw()
        self.door_right.draw()
        
        # Draw platforms and conveyors
        for p in self.platforms: p.draw()
        for c in self.conveyors: c.draw()

        # Draw truck
        self.truck.draw()

        # Draw characters
        self.mario.draw()
        self.luigi.draw()

        # Draw boss (if active)
        self.boss.draw()

        # Draw the vertical structure last so it covers other elements
        self.vertical_structure.draw()
        
        # HUD is drawn on top of everything
        self.game_info.draw_score(self.score)
        self.game_info.draw_lives(self.failures)

    def __draw_game_over(self):
        """Draws the game over screen."""
        sprite = constants.GAME_OVER_SPRITE
        img, u, v, w, h, colkey = sprite # Unpack sprite tuple
        
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

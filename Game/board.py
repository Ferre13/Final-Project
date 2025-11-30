import pyxel
import constants
from game_info import GameInfo
from package_manager import PackageManager

class Board:
    """
    The main game board that manages all game objects, game states,
    and the main update and draw loops. It receives all game objects from
    a factory and is responsible for orchestrating the game's logic.
    """
    def __init__(self, difficulty: str, objects: dict):
        """
        Initializes the game board with all necessary game objects.
        
        :param difficulty: A string representing the chosen difficulty.
        :param objects: A dictionary containing all pre-created game objects.
        """
        self.difficulty = difficulty
        
        # Unpack objects from the dictionary provided by the factory
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
        self.init_configuration()
        self.package_manager = PackageManager(self)

    def init_configuration(self):
        """Sets up the initial configuration and state of the board."""
        self.score = 0
        self.failures = 0
        self.packages = []
        self.punished_char = None
        self.deliveries_count = 0
        self.game_info = GameInfo()
        self.state = constants.PLAYING

    def reset_game(self):
        """ Resets all game state to initial values without recreating objects. """
        self.score = 0
        self.failures = 0
        self.packages = []
        self.deliveries_count = 0
        self.punished_char = None
        self.state = constants.PLAYING
        
        self.truck.reset()
        
        # Reset characters to their initial states and positions
        self.mario.state = constants.CHAR_STATE_STATIC
        self.mario.floor = 0
        self.mario.x = self.mario.original_x
        self.mario.update()

        self.luigi.state = constants.CHAR_STATE_STATIC
        self.luigi.floor = 1
        self.luigi.x = self.luigi.original_x
        self.luigi.update()

    def handle_truck_bonus(self):
        """Checks if a bonus for successful deliveries should be awarded."""
        self.deliveries_count += 1
        bonus_awarded = False

        # Bonus logic is not applied in 'CRAZY' mode
        if self.difficulty == "EASY":
            if self.deliveries_count % constants.BONUS_REQUIRED_EASY == 0:
                bonus_awarded = True
        elif self.difficulty == "MEDIUM":
            if self.deliveries_count % constants.BONUS_REQUIRED_MEDIUM == 0:
                bonus_awarded = True
        elif self.difficulty == "EXTREME":
            if self.deliveries_count % constants.BONUS_REQUIRED_EXTREME == 0:
                bonus_awarded = True

        if bonus_awarded and self.failures > 0:
            self.failures -= 1

    def active_punishment(self, character_name: str):
        """Activates the boss sequence for a character's failure."""
        if character_name == "Mario":
            self.punished_char = self.mario
            self.boss.appear("MARIO_FAIL")
        else:
            self.punished_char = self.luigi
            self.boss.appear("LUIGI_FAIL")
        
        self.punished_char.enter_punishment_mode()
        self.state = constants.BOSS_SEQUENCE

    # --- Main Update Logic ---

    def update(self):
        """
        The main update loop, which dispatches to other update methods
        based on the current game state.
        """
        if self.state == constants.PLAYING:
            self.__update_playing()
        elif self.state == constants.TRUCK_SEQUENCE:
            self.__update_truck_sequence()
        elif self.state == constants.BOSS_SEQUENCE:
            self.__update_boss_sequence()
        elif self.state == constants.GAME_OVER:
            self.__update_game_over()
        
        # Global actions - can be moved inside states if needed
        self.door_left.update()
        self.door_right.update()
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def __update_playing(self):
        """Handles game logic when the game is in the 'PLAYING' state."""
        self.package_logic.update()
        self.mario.update()
        self.luigi.update()

    def __update_truck_sequence(self):
        """Handles the truck delivery animation sequence."""
        self.truck.update()
        # Characters enter rest mode during the truck sequence
        if self.mario.state != constants.CHAR_STATE_REST1 and self.mario.state != constants.CHAR_STATE_REST2:
            self.mario.enter_rest_mode()
            self.luigi.enter_rest_mode()
        self.mario.update()
        self.luigi.update()

        # Check if the truck sequence has finished
        if not self.truck.is_delivering:
            self.score += constants.POINTS_PER_TRUCK
            self.handle_truck_bonus()
            self.boss.appear("BREAK")  # Trigger the post-delivery boss appearance
            self.state = constants.BOSS_SEQUENCE

    def __update_boss_sequence(self):
        """Handles the boss appearance animation (for failures or breaks)."""
        self.boss.update()
        # Check if the boss sequence has finished
        if not self.boss.is_active:
            if self.punished_char:
                self.punished_char.exit_punishment_mode()
                self.punished_char = None
            # Always exit rest mode after any boss sequence
            self.mario.exit_rest_mode()
            self.luigi.exit_rest_mode()
            self.state = constants.PLAYING

    def __update_game_over(self):
        """Handles the game over screen and input for restarting."""
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
            self.reset_game()

    # --- Main Draw Logic ---

    def draw(self):
        """
        The main draw loop, which dispatches to other draw methods
        based on the current game state.
        """
        # Clear screen
        pyxel.cls(0)

        if self.state == constants.GAME_OVER:
            self.__draw_game_over()
        else:
            self.__draw_playing()

    def __draw_playing(self):
        """Draws all the elements for the main game screen."""
        for w in self.windows: w.draw()
        if self.machine: self.machine.draw()
        if self.exit_signal: self.exit_signal.draw()
        if self.door_left: self.door_left.draw()
        if self.door_right: self.door_right.draw()
        if self.boss: self.boss.draw()
        for p in self.packages: p.draw()
        for platform in self.platforms: platform.draw()
        for conv in self.conveyors: conv.draw()
        if self.vertical_structure: self.vertical_structure.draw()
        if self.level_sign: self.level_sign.draw()
        if self.mario: self.mario.draw()
        if self.luigi: self.luigi.draw()
        if self.truck: self.truck.draw()

        # HUD is drawn on top of everything
        self.game_info.draw_score(self.score)
        self.game_info.draw_lives(self.failures)

    def __draw_game_over(self):
        """Draws the game over screen."""
        pyxel.text(constants.CENTER_SCREEN - 30, constants.CENTER_SCREEN - 10, "GAME OVER", 8)
        pyxel.text(constants.CENTER_SCREEN - 40, constants.CENTER_SCREEN + 5, "PRESS SPACE TO RESTART", 7)
        
        # Show final score
        self.game_info.draw_score(self.score)
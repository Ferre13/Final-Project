import pyxel
import constants
from board import Board
from factory import Factory
from menu import Menu

class Game:
    """
    The main class that initializes the game, creates all objects using
    the Factory, and runs the main game loop. It manages the high-level
    state of the application, switching between the main menu and the game itself.
    """
    def __init__(self):
        """
        Initializes Pyxel and the main menu.
        """
        pyxel.init(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, title="Mario Bros Game")
        pyxel.load(constants.SPRITES_FILE)  # This loads the main resource file into image bank 0
        self.menu = Menu()
        self.board = None
        self.game_state = constants.MAIN_MENU
        
        pyxel.run(self.update, self.draw)

    def start_game(self, difficulty: str):
        """
        Creates all game objects and starts a new game with the given difficulty.
        """
        factory = Factory(difficulty)
        
        windows, machine, level_sign = factory.create_background()
        truck, exit_signal, vertical_structure, platforms, conveyors = factory.create_world()
        mario, luigi, boss, door_left, door_right = factory.create_characters()
        
        game_objects = {
            "mario": mario, "luigi": luigi, "boss": boss, "door_left": door_left,
            "door_right": door_right, "truck": truck, "conveyors": conveyors,
            "platforms": platforms, "windows": windows, "machine": machine,
            "level_sign": level_sign, "exit_signal": exit_signal,
            "vertical_structure": vertical_structure
        }
        
        self.board = Board(difficulty, game_objects)
        self.game_state = constants.PLAYING

    def update(self):
        """
        Main update loop. Delegates to the menu or the board based on the
        current game state.
        """
        if self.game_state == constants.MAIN_MENU:
            chosen_difficulty = self.menu.update()
            if chosen_difficulty:
                self.start_game(chosen_difficulty)
        
        elif self.game_state == constants.PLAYING:
            if self.board:
                self.board.update()
                # If the board signals it's time to go to the menu (from game over)
                if self.board.state == constants.MAIN_MENU:
                    self.game_state = constants.MAIN_MENU
                    self.board = None

    def draw(self):
        """
        Main draw loop. Delegates to the menu or the board based on the
        current game state.
        """
        pyxel.cls(0)
        if self.game_state == constants.MAIN_MENU:
            self.menu.draw()
        
        elif self.game_state == constants.PLAYING:
            if self.board:
                self.board.draw()

if __name__ == "__main__":
    Game()
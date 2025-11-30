import pyxel
import constants
import board
from factory import Factory

class Game:
    """
    The main class that initializes the game, creates all objects using
    the Factory, and runs the main game loop.
    """
    def __init__(self):
        """
        Initializes Pyxel, creates the factory, builds the world,
        and starts the game loop.
        """
        pyxel.init(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, title="Mario Bros Game")
        pyxel.load(constants.SPRITES_FILE)
        
        difficulty = "EXTREME"
        
        # Use the Factory to create all game objects
        factory = Factory(difficulty)
        
        # Create and bundle all objects into a dictionary
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
        
        self.board = board.Board(difficulty, game_objects)
        
        pyxel.run(self.update, self.draw)

    def update(self):
        """Main update loop, delegates to the board."""
        self.board.update()

    def draw(self):
        """Main draw loop, delegates to the board."""
        pyxel.cls(0)
        self.board.draw()

if __name__ == "__main__":
    Game()
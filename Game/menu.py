import pyxel
import constants

class Menu:
    """
    Manages the main menu of the game. It is responsible for drawing the
    difficulty options and detecting user input to select a level.
    """
    def __init__(self):
        """Initializes the menu."""
        # A dictionary mapping the key pressed to the difficulty string and sprite
        self.options = {
            pyxel.KEY_1: {"label": "EASY", "sprite": constants.LEVEL_EASY},
            pyxel.KEY_2: {"label": "MEDIUM", "sprite": constants.LEVEL_MEDIUM},
            pyxel.KEY_3: {"label": "EXTREME", "sprite": constants.LEVEL_EXTREME},
            pyxel.KEY_4: {"label": "CRAZY", "sprite": constants.LEVEL_CRAZY},
        }

    def update(self) -> str | None:
        """
        Checks for user input to select a difficulty.

        :return: The string of the chosen difficulty (e.g., "EASY") if a key is pressed,
                 otherwise returns None.
        """
        for key, option_data in self.options.items():
            if pyxel.btnp(key):
                return option_data["label"]
        return None

    def draw(self):
        """
        Draws the difficulty selection sprites on the screen.
        """
        y_pos = 40
        for key, option_data in self.options.items():
            sprite = option_data["sprite"]
            # Center the sprite horizontally
            x_pos = (constants.SCREEN_WIDTH - sprite[3]) / 2
            
            # Draw the sprite
            pyxel.blt(x_pos, y_pos, *sprite)
            
            # Move down for the next sprite
            y_pos += 15

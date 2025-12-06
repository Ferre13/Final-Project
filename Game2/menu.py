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
        # Starting y position for instructions
        y_inst_start = 15

        # Add explanatory text - moved to top
        instructions_text_1 = "PRESS 1-4 TO SELECT LEVEL"
        instructions_text_2 = "PRESS ESC TO EXIT"

        # Calculate x_pos to center the text
        text_x_1 = (constants.SCREEN_WIDTH - (len(instructions_text_1) * 4)) / 2
        text_x_2 = (constants.SCREEN_WIDTH - (len(instructions_text_2) * 4)) / 2
        
        # Use pyxel.text to draw the instructions
        pyxel.text(text_x_1, y_inst_start, instructions_text_1, constants.TEXT_COLOR)
        pyxel.text(text_x_2, y_inst_start + 10, instructions_text_2, constants.TEXT_COLOR) # 10 pixels lower for second line

        # Starting y position for difficulty options, after instructions
        y_pos_options_start = y_inst_start + 30 # A bit of spacing

        y_pos = y_pos_options_start
        for key, option_data in self.options.items():
            sprite = option_data["sprite"]
            # Center the sprite horizontally
            x_pos = (constants.SCREEN_WIDTH - sprite[3]) / 2
            
            # Draw the sprite
            pyxel.blt(x_pos, y_pos, *sprite)
            
            # Move down for the next sprite
            y_pos += 15

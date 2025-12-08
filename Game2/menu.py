import pyxel
import constants

class Menu:
    """Manages the main menu of the game. It draws the difficulty options and detects user input to select a level"""
    def __init__(self):
        # A dictionary that associates keys with the corresponding difficulty
        self.options = {
            # Each key has a label (difficulty name) and a sprite
            pyxel.KEY_1: {"label": "EASY", "sprite": constants.LEVEL_EASY}, 
            pyxel.KEY_2: {"label": "MEDIUM", "sprite": constants.LEVEL_MEDIUM},
            pyxel.KEY_3: {"label": "EXTREME", "sprite": constants.LEVEL_EXTREME},
            pyxel.KEY_4: {"label": "CRAZY", "sprite": constants.LEVEL_CRAZY},
        }

    def update(self):
        """Checks for user input to select a difficulty."""
        # Check each key to see if it was pressed and return the corresponding difficulty label
        for key, option_data in self.options.items():
            if pyxel.btnp(key):
                return option_data["label"]
        # If no key was pressed, return None and continue showing the menu
        return None

    def draw(self):
        """
        Draws the difficulty selection sprites on the screen.
        """
        # Starting y position for instructions
        y_inst_start = 15

        # Draw instructions at the top
        instructions_text_1 = "PRESS 1-4 TO SELECT LEVEL"
        instructions_text_2 = "PRESS ESC TO EXIT"

        # Calculate x_pos to center the text. Each character is 4 pixels wide.
        text_x_1 = (constants.SCREEN_WIDTH - (len(instructions_text_1) * 4)) / 2
        text_x_2 = (constants.SCREEN_WIDTH - (len(instructions_text_2) * 4)) / 2
        
        # Use pyxel.text to draw the instructions
        pyxel.text(text_x_1, y_inst_start, instructions_text_1, constants.TEXT_COLOR)
        pyxel.text(text_x_2, y_inst_start + 10, instructions_text_2, constants.TEXT_COLOR) # 10 pixels lower for second line

        # Starting y position for difficulty options, after instructions
        y_pos_options_start = y_inst_start + 30 # Add spacing

        y_pos = y_pos_options_start
        for key, option_data in self.options.items():
            sprite = option_data["sprite"]
            # Center the sprite horizontally
            x_pos = (constants.SCREEN_WIDTH - sprite[3]) / 2
            
            # Draw the sprite
            pyxel.blt(x_pos, y_pos, *sprite)
            
            # Move down for the next sprite
            y_pos += 15

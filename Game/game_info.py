import pyxel
import constants

class GameInfo:
    """
    Manages the display of game information, such as the player's score
    and remaining lives on the screen.
    """
    def __init__(self):
        """
        Initializes the HUD by loading necessary sprite lists from constants
        and storing them as private instance attributes.
        """
        self.__number_sprites = constants.NUMBER_SPRITES
        self.__life_sprite = constants.LIFE_SPRITE

    def draw_score(self, score: int):
        """
        Draws the player's current score in the top-right corner of the screen.

        :param score: The current score to be displayed.
        """
        # We have to convert the score to a string to access each digit individually
        score_str = str(score)
        x_offset = constants.SCORE_X
        

        # Draw each digit of the score using its sprite
        for char in score_str:
            digit = int(char)
            img, u, v, w, h, colkey = self.__number_sprites[digit]
            
            pyxel.blt(x_offset, constants.SCORE_Y, img, u, v, w, h, colkey)
            # Move the x_offset for the next digit, adding the width and 1 pixel for spacing
            x_offset += (w + 1)

    def draw_lives(self, failures: int):
        """
        Draws the remaining lives as Mario face icons in the top-center
        of the screen.

        :param failures: The number of times the player has failed.
        """        
        lives_left = constants.MAX_FAILURES - failures
        
        # Draw a Mario face icon for each life left
        for life in range(lives_left):
            img, u, v, w, h, colkey = self.__life_sprite
            # Calculate position for each life icon, adding 2 pixels for spacing
            pos_x = constants.LIVES_X + (life * (w + 2))
            pyxel.blt(pos_x, constants.LIVES_Y, img, u, v, w, h, colkey)
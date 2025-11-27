import pyxel
import constants

class HUD:
    """
    Manages the Heads-Up Display (HUD), which shows the player's score
    and remaining lives on the screen.
    """
    def __init__(self):
        """Initializes the HUD by loading necessary sprites from constants."""
        self.__number_sprites = constants.NUMBER_SPRITES
        self.__life_sprite = constants.LIFE_SPRITE

    def draw_score(self, score: int):
        """
        Draws the player's current score in the top-right corner of the screen.

        :param score: The current score to be displayed.
        """
        score_str = str(score)
        x_offset = constants.SCORE_X
        
        # Draw 'SCORE' text label
        pyxel.text(x_offset - 23, constants.SCORE_Y + 1, "SCORE", 7)

        # Draw each digit of the score using its sprite
        for char in score_str:
            digit = int(char)
            img, u, v, w, h, colkey = self.__number_sprites[digit]
            
            pyxel.blt(x_offset, constants.SCORE_Y, img, u, v, w, h, colkey)
            x_offset += (w + 1) # Move to the next position for the next digit

    def draw_lives(self, failures: int):
        """
        Draws the remaining lives as Mario face icons in the top-center
        of the screen.

        :param failures: The number of times the player has failed.
        """        
        lives_left = constants.MAX_FAILURES - failures
        
        # Draw a Mario face icon for each life the player has remaining
        for life in range(lives_left):
            img, u, v, w, h, colkey = self.__life_sprite
            # Calculate position for each life icon, adding 2 pixels for spacing
            pos_x = constants.LIVES_X + (life * (w + 2))
            pyxel.blt(pos_x, constants.LIVES_Y, img, u, v, w, h, colkey)
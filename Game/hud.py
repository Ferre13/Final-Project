import pyxel
import constants

class HUD:
    """
    Heads-Up Display manager. 
    Responsible for drawing the score and remaining lives (Misses).
    """
    def __init__(self):
        self.__number_sprites = constants.NUMBER_SPRITES
        self.__life_sprite = constants.LIFE_SPRITE

    def draw_score(self, score: int):
        """
        Draws the numeric score at the top right.
        """
        score_str = str(score)
        x_offset = constants.SCORE_X
        
        # Draw 'SCORE' text
        pyxel.text(x_offset - 23, constants.SCORE_Y + 1, "SCORE", 7)

        # Draw each digit of the score
        for char in score_str:
            digit = int(char)
            # Get each value from the sprite tuple
            img, u, v, w, h, colkey = self.__number_sprites[digit]
            
            pyxel.blt(x_offset, constants.SCORE_Y, img, u, v, w, h, colkey)
            # Calculate next x position
            x_offset += (w + 1)

    def draw_lives(self, failures: int):
        """
        Draws the lives left. 
        Logic: We draw specific icons to represent 'Lives Left'.
        """
        # Draw "LIVES" label
        pyxel.text(constants.LIVES_X, constants.LIVES_Y, "LIVES", 7)
        
        start_x = constants.LIVES_X + 15
        
        # Calculate lives left
        lives_left = constants.MAX_FAILURES - failures
        
        # Draw a Mario face for each life remaining
        for life in range(lives_left):
            img, u, v, w, h, colkey = self.__life_sprite
            # Calculate position for each life icon
            pos_x = start_x + (life * (w + 2))
            pyxel.blt(pos_x, constants.LIVES_Y, img, u, v, w, h, colkey)
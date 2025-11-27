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
        
        # Draw 'SCORE' label (optional, simple text for now or sprite if you have it)
        pyxel.text(x_offset - 23, constants.SCORE_Y + 1, "SCORE", 7)

        for char in score_str:
            digit = int(char)
            sprite = self.__number_sprites[digit]
            img, u, v, w, h, colkey = sprite
            
            pyxel.blt(x_offset, constants.SCORE_Y, img, u, v, w, h, colkey)
            x_offset += (w + 1) # Advance X for next digit

    def draw_lives(self, failures: int):
        """
        Draws the lives (Misses). 
        Logic: We draw specific icons to represent 'Lives Left' or 'Failures'.
        """
        # Draw "MISS" label
        pyxel.text(constants.LIVES_X, constants.LIVES_Y, "MISS", 7)
        
        start_x = constants.LIVES_X + 25
        
        # Calculate lives left (Max - Failures)
        lives_left = constants.MAX_FAILURES - failures
        
        # Draw a Mario face for each life remaining
        for i in range(lives_left):
            img, u, v, w, h, colkey = self.__life_sprite
            px = start_x + (i * (w + 2))
            pyxel.blt(px, constants.LIVES_Y, img, u, v, w, h, colkey)
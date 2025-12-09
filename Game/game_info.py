import pyxel
import constants

class GameInfo:
    """Manages drawing the score and lives."""
    def __init__(self):
        self.__number_sprites = constants.NUMBER_SPRITES
        self.__life_sprite = constants.LIFE_SPRITE

    def draw_score(self, score: int, x: int = constants.SCORE_X, y: int = constants.SCORE_Y):
        """
        Draws the score on the screen.
        :param score: The score value to draw.
        :param x: Optional x-coordinate to draw at.
        :param y: Optional y-coordinate to draw at.
        """
        # Draw the "SCORE" text if the position is the default (while playing the game)
        if x == constants.SCORE_X and y == constants.SCORE_Y:
            pyxel.text(x + constants.SCORE_LABEL_X_OFFSET, y + constants.SCORE_LABEL_Y_OFFSET, "SCORE", constants.TEXT_COLOR)

        # Draw the number sprites
        x_offset = x
        for char in str(score):
            digit = int(char)
            img, u, v, w, h, colkey = self.__number_sprites[digit]
            
            pyxel.blt(x_offset, y, img, u, v, w, h, colkey)
            x_offset += (w + constants.DIGIT_SPACING)

    def draw_lives(self, failures: int):
        """
        Draws the remaining lives on the screen.
        :param failures: The number of failures the player has.
        """        
        lives_left = constants.MAX_FAILURES - failures
        
        for life in range(lives_left):
            img, u, v, w, h, colkey = self.__life_sprite
            pos_x = constants.LIVES_X + (life * (w + constants.LIFE_ICON_SPACING))
            pyxel.blt(pos_x, constants.LIVES_Y, img, u, v, w, h, colkey)
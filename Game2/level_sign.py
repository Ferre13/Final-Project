import pyxel
import constants
from game_object import GameObject

class LevelSign(GameObject):
    """A sign in the bottom-left that displays the current difficulty."""
    def __init__(self, difficulty: str, x: int, y: int):
        super().__init__(x, y)
        self.difficulty = difficulty

    @property
    def __sprite(self):
        """Selects the correct sprite based on the difficulty string."""
        if self.difficulty == "EASY": return constants.LEVEL_EASY
        elif self.difficulty == "MEDIUM": return constants.LEVEL_MEDIUM
        elif self.difficulty == "EXTREME": return constants.LEVEL_EXTREME
        elif self.difficulty == "CRAZY": return constants.LEVEL_CRAZY
        return constants.LEVEL_EASY

    def draw(self):
        pyxel.blt(self.x, self.y, *self.__sprite)
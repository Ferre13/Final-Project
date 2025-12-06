import pyxel
import constants
from game_object import GameObject

class ExitSignal(GameObject):
    """A decorative 'EXIT' sign, usually placed near the truck."""
    def draw(self):
        pyxel.blt(self.x, self.y, *constants.EXIT_SIGNAL_SPRITE)
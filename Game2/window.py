import pyxel
import constants
from game_object import GameObject

class Window(GameObject):
    """A decorative window for the factory background."""
    def draw(self):
        pyxel.blt(self.x, self.y, *constants.WINDOW_SPRITE)
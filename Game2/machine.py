import pyxel
import constants
from game_object import GameObject

class Machine(GameObject):
    """The large machine on the right side of the screen where packages originate."""
    def draw(self):
        pyxel.blt(self.x, self.y, *constants.MACHINE_SPRITE)
import pyxel
from constants import CONVEYOR_SPRITE

class Conveyor:
    """
    Represents a conveyor belt in the factory.
    """

    def __init__(self, y: int, speed: float, length: int, direction: int, vertical_structure_x: int, vertical_structure_width: int):
        """
        Initializes a conveyor belt.
        :param y: The y-coordinate of the conveyor belt.
        :param speed: The speed at which packages move on the belt.
        :param length: The length of the conveyor belt.
        :param direction: The direction of the conveyor belt (-1 for left, 1 for right).
        :param vertical_structure_x: The x-coordinate of the vertical structure.
        :param vertical_structure_width: The width of the vertical structure in number of sprites.
        """
        self._y = y
        self._speed = speed
        self._length = length
        self._direction = direction
        self._vertical_structure_x = vertical_structure_x
        self._vertical_structure_width = vertical_structure_width

    @property
    def y(self) -> int:
        return self._y

    @property
    def speed(self) -> float:
        return self._speed

    @speed.setter
    def speed(self, value: float):
        self._speed = value
        
    @property
    def direction(self) -> int:
        return self._direction

    def draw(self):
        """
        Draws the conveyor belt using sprites, avoiding the vertical structure.
        """
        sprite_width = CONVEYOR_SPRITE[3]
        num_sprites = self._length // sprite_width
        for i in range(num_sprites):
            x = i * sprite_width
            if x < self._vertical_structure_x or x > self._vertical_structure_x + self._vertical_structure_width * 12:
                pyxel.blt(x, self.y, *CONVEYOR_SPRITE)

import constants
import pyxel

class Conveyor:
    """ 
    This class represents the conveyor belt in the game. 
    """
    def __init__(self, x: int, y: int, length: int, speed: float, direction: int, is_right_side: bool = False):
        self.x = x
        self.y = y
        self.length = length
        self.speed = speed
        self.direction = direction
        self.is_right_side = is_right_side

    @property
    def x(self) -> int:
        return self.__x
    @x.setter
    def x(self, x: int):
        if not isinstance(x, int):
            raise TypeError("x must be an integer")
        self.__x = x

    @property
    def y(self) -> int:
        return self.__y
    @y.setter
    def y(self, y: int):
        if not isinstance(y, int):
            raise TypeError("y must be an integer")
        self.__y = y

    @property
    def length(self) -> int:
        return self.__length
    @length.setter
    def length(self, length: int):
        if not isinstance(length, int):
            raise TypeError("length must be an integer")
        self.__length = length

    @property
    def speed(self) -> float:
        return self.__speed
    @speed.setter
    def speed(self, speed: float):
        if not isinstance(speed, (int, float)):
            raise TypeError("speed must be a number")
        self.__speed = speed

    @property
    def direction(self) -> int:
        return self.__direction
    @direction.setter
    def direction(self, value: int):
        if not isinstance(value, int) or value not in [-1, 1]:
            raise ValueError("Direction must be -1 or 1")
        self.__direction = value

    def draw(self):
        """
        Draws the conveyor belt.
        Left Side: Full Sprite -> Left Half Remainder
        Right Side: Right Half Remainder -> Full Sprite
        """
        sprite_width = constants.CONVEYOR_SPRITE[3]
        num_full_sprites = self.length // sprite_width
        remainder = self.length % sprite_width
        
        # Unpack sprite data
        img, u, v, w, h, colkey = constants.CONVEYOR_SPRITE

        current_x = self.x

        if self.is_right_side:
            # --- RIGHT SIDE DRAWING [Half -> Full] ---
            
            # 1. Draw Remainder FIRST (The "Right Half" of the sprite)
            if remainder > 0:
                # We start reading the texture from (u + width - remainder) to get the right side
                # e.g. if width 32, rem 16. Start at 16.
                start_u = u + (w - remainder)
                pyxel.blt(current_x, self.y, img, start_u, v, remainder, h, colkey)
                current_x += remainder
            
            # 2. Draw Full Sprites
            for i in range(num_full_sprites):
                pyxel.blt(current_x, self.y, *constants.CONVEYOR_SPRITE)
                current_x += sprite_width

        else:
            # --- LEFT SIDE DRAWING [Full -> Half] (Standard) ---
            
            # 1. Draw Full Sprites
            for i in range(num_full_sprites):
                pyxel.blt(current_x, self.y, *constants.CONVEYOR_SPRITE)
                current_x += sprite_width
            
            # 2. Draw Remainder LAST (The "Left Half" of the sprite)
            if remainder > 0:
                # Draw standard from u=0, but limited width
                pyxel.blt(current_x, self.y, img, u, v, remainder, h, colkey)
import constants
import pyxel

class Conveyor:
    """ 
    This class represents the conveyor belt in the game. 
    """
    def __init__(self, x: int, y: int, length: int, speed: float, 
                 direction: int, is_right_side: bool):
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

    @property
    def is_right_side(self) -> bool:
        return self.__is_right_side
    @is_right_side.setter
    def is_right_side(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("is_right_side must be a boolean")
        self.__is_right_side = value

    def draw(self):
        """
        Draws the conveyor belt.
        Left Side: Full Sprite + Left Half pixels left
        Right Side: Right Half pixels left + Full Sprite
        """
        sprite_width = constants.CONVEYOR_SPRITE[3]
        # How many full sprites for the length
        num_full_sprites = self.length // sprite_width
        # How many pixels are not covered by full sprites
        pixels_left = self.length % sprite_width
        
        # This is for drawing the remainder part correctly
        img, u, v, w, h, colkey = constants.CONVEYOR_SPRITE

        current_x = self.x

        if self.is_right_side:
            # Right (Half + Full)
            # Draw Remainder (The right half of the sprite)
            if pixels_left > 0:
                # We have to draw only the right part of the sprite
                # We go to the end of the sprite (u + w)
                # Then go back as many pixels as we want to see (pixels_left)
                starting_u = u + w - pixels_left

                pyxel.blt(current_x, self.y, img, starting_u, v, pixels_left, h, colkey)
                current_x += pixels_left
            
            # Draw Full Sprites
            for sprite in range(num_full_sprites):
                pyxel.blt(current_x, self.y, *constants.CONVEYOR_SPRITE)
                current_x += sprite_width

        else:
            # Left (Full + Half)
            # Draw Full Sprites
            for sprite in range(num_full_sprites):
                pyxel.blt(current_x, self.y, *constants.CONVEYOR_SPRITE)
                current_x += sprite_width
            
            # Draw Remainder (The left half of the sprite)
            if pixels_left > 0:
                # Width is limited to pixels_left
                pyxel.blt(current_x, self.y, img, u, v, pixels_left, h, colkey)
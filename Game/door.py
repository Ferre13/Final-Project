import constants
import pyxel

class Door:
    """ 
    Represents a door. Uses centralized constants for states.
    """
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.state = constants.DOOR_STATE_CLOSED
        self.sprites = constants.DOOR_SPRITES
        self.animation_timer = 0
        
    @property
    def x(self) -> int: return self.__x
    @x.setter
    def x(self, x: int):
        if not isinstance(x, int): raise TypeError("x must be int")
        self.__x = x
    
    @property
    def y(self) -> int: return self.__y
    @y.setter
    def y(self, y: int):    
        if not isinstance(y, int): raise TypeError("y must be int")
        self.__y = y
        
    def open(self):
        self.state = constants.DOOR_STATE_OPENING 
        self.animation_timer = constants.DOOR_ANIMATION_SPEED
    
    def close(self):
        self.state = constants.DOOR_STATE_CLOSING
        self.animation_timer = constants.DOOR_ANIMATION_SPEED

    def update(self):
        if self.state == constants.DOOR_STATE_OPENING:
            self.animation_timer -= 1
            if self.animation_timer <= 0:
                self.state = constants.DOOR_STATE_OPEN

        elif self.state == constants.DOOR_STATE_CLOSING:
            self.animation_timer -= 1
            if self.animation_timer <= 0:
                self.state = constants.DOOR_STATE_CLOSED
            
    def draw(self):
        pyxel.blt(self.x, self.y, *self.sprites[self.state])
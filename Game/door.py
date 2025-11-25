import constants
import pyxel

class Door:
    """ 
    This class represents a door for the boss to appear from in the game. 
    """
    def __init__(self, x: int, y: int):
        """This is the magic method that initializes the Door object.
        :param x: int - The x-coordinate of the door
        :param y: int - The y-coordinate of the door"""
        self.x = x
        self.y = y
        self.state = "closed"  # Possible states: "open", "opening", "closed"
        self.sprites = constants.DOOR_SPRITES
        self.animation_timer = 0
        
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
        
    # These are the methods for the door actions
    
    def open(self):
        """
        Initiates the door opening sequence.
        """
        self.state = "opening" 
        self.animation_timer = 30  # Duration of the opening animation in frames
    
    def close(self):
        """
        Initiates the door closing sequence.
        """
        self.state = "closing"
        self.animation_timer = 30  # Duration of the closing animation in frames
        
    def update(self):
        """
        Updates the door's state and animation.
        """
        if self.state == "opening":
            self.animation_timer -= 1
            if self.animation_timer > 15:
                self.state = "opening"
            else:
                self.state = "open"
            if self.animation_timer <= 0:
                self.state = "open"
        elif self.state == "closing":
            self.animation_timer -= 1
            if self.animation_timer > 15:
                self.state = "closing"
            else:
                self.state = "closed"
            if self.animation_timer <= 0:
                self.state = "closed"
            
        
    def draw(self):
        """
        Draws the door on the screen based on its current state.
        """
        
        pyxel.blt(self.x, self.y, *self.sprites[self.state])
        

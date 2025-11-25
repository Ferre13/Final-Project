import constants
import pyxel
from door import Door

class Boss:
    """ 
    This class represents the boss in the game. 
    """
    def __init__(self, name: str, sprites):
        """This is the magic method that initializes the Boss object.
        :param name: str - "Mario" or "Luigi"
        """
        self.name = name
        self.y = constants.BOSS_Y
        self,is_visible = False
        self.timer = 0
        self.door = Door(self.x, self.y)
        self.sprites = sprites
        
        # Character specific settings
        if self.name == "Mario":
            self.sprites = constants.BOSS_MARIO
            self.x = constants.BOSS_MARIO_X
        elif self.name == "Luigi":
            self.sprites = constants.BOSS_LUIGI
            self.x = constants.BOSS_LUIGI_X
        
    @property
    def name(self) -> str:
        #This is the getter for the name attribute
        return self.__name
    
    @name.setter
    def name(self, name: str):
        #This is the setter for the name attribute
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        self.__name = name
        
    
    # These are the methods for the boss actions
    
    def appear(self, duration: int):
        """
        Makes the boss appear by opening the door.
        :param duration: The number of frames the boss should be visible.
        """
        self.is_visible = True
        self.timer = duration
        self.door.open()
    
    def update(self):
        """
        Updates the boss's visibility timer and door state.
        """
        self.door.update()
        if self.is_visible:
            self.timer -= 1
            if self.timer <= 0:
                self.is_visible = False
                self.door.close()
    
    def draw(self):
        """
        Draws the boss and the door on the screen.
        """
        self.door.draw()
        if self.is_visible and self.door.state == "opened":
            pyxel.blt(self.x, self.y, *constants.BOSS_1)
    

    
    
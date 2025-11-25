import constants
import pyxel

class Boss:
    """ 
    This class represents the boss in the game. 
    """
    def __init__(self, name: str):
        """This is the magic method that initializes the Boss object.
        :param x: int - The x-coordinate of the boss
        :param y: int - The y-coordinate of the boss
        """
        self.name = name
        self.y = constants.BOSS_Y
        
        # Character specific settings
        if self.name == "Mario":
            self.sprite = constants.BOSS_MARIO
            self.x = constants.BOSS_MARIO_X
        elif self.name == "Luigi":
            self.sprite = constants.BOSS_LUIGI
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
        
    @property
    def y(self) -> int:
        return self.__y
    

    
    
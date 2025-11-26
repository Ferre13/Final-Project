import pyxel
import constants
from conveyor import Conveyor 

class Package:
    """
    Represents a package moving through the factory.
    """
    STATE_MOVING = "moving"
    STATE_FALLING = "falling"
    
    def __init__(self, difficulty: str, start_conveyor: Conveyor, floor_index: int):
        self.__difficulty = difficulty
        self.__width = 11
        self.__height = 6
        
        self.current_conveyor = start_conveyor
        self.floor_index = floor_index
        
        self.sprite_list = self.__get_sprite_list()
        
        # Position logic
        if self.current_conveyor.direction == 1:
             self.x = self.current_conveyor.x
        else:
             self.x = self.current_conveyor.end_x - 10 
             
        self.y = self.current_conveyor.y - self.height
        
        self.status = self.STATE_MOVING
        self.level_index = 0 

    @property
    def x(self) -> int: return self.__x
    @x.setter
    def x(self, value): 
        if not isinstance(value, (int, float)): raise TypeError("x must be a number")
        self.__x = value

    @property
    def y(self) -> int: return self.__y
    @y.setter
    def y(self, value): 
        if not isinstance(value, (int, float)): raise TypeError("y must be a number")
        self.__y = value

    @property
    def difficulty(self) -> str: return self.__difficulty
    @property
    def width(self) -> int: return self.__width
    @property
    def height(self) -> int: return self.__height
    
    # Methods for the package

    def __get_sprite_list(self) -> list:
        if self.difficulty == "EASY": return constants.PCK_EASY_SPRITES
        elif self.difficulty == "MEDIUM": return constants.PCK_MEDIUM_SPRITES
        elif self.difficulty == "EXTREME": return constants.PCK_EXTREME_SPRITES
        elif self.difficulty == "CRAZY": return constants.PCK_CRAZY_SPRITES
        return constants.PCK_EASY_SPRITES

    def advance_to_conveyor(self, next_conveyor: Conveyor):
        self.current_conveyor = next_conveyor
        self.floor_index += 1
        
        if self.current_conveyor.direction == 1: 
            self.x = self.current_conveyor.x
        else: 
            self.x = self.current_conveyor.end_x - 10

        self.y = self.current_conveyor.y - self.height
        self.status = self.STATE_MOVING

    def update(self):
        if self.status == self.STATE_MOVING:
            # --- UPDATED PHYSICS ---
            # Use the actual speed of the conveyor (supports floats and random values)
            speed = self.current_conveyor.speed
            direction = self.current_conveyor.direction
            
            prev_x = self.x
            self.x += speed * direction

            # Visuals (Level Up)
            trigger_x = constants.CENTER_SCREEN
            if (direction == -1 and prev_x > trigger_x and self.x <= trigger_x) or \
               (direction == 1 and prev_x < trigger_x and self.x >= trigger_x):
                self.level_index += 1

        elif self.status == self.STATE_FALLING:
            self.y += 2

    def draw(self):
        sprite_idx = self.level_index * 2
        if sprite_idx >= len(self.sprite_list): 
            sprite_idx = len(self.sprite_list) - 2
        
        if self.status == self.STATE_FALLING:
             sprite_idx += 1 
             
        sprite = self.sprite_list[sprite_idx]
        img, u, v, w, h, colkey = sprite
        pyxel.blt(int(self.x), int(self.y), img, u, v, w, h, colkey)
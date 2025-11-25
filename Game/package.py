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
        # Read-Only attributes
        self.__difficulty = difficulty
        self.__width = 11
        self.__height = 6
        
        self.current_conveyor = start_conveyor
        self.floor_index = floor_index
        
        # Use private methods (double underscore)
        self.sprite_list = self.__get_sprite_list()
        
        # Position logic
        if self.current_conveyor.direction == 1:
             self.x = self.current_conveyor.x
        else:
             self.x = self.current_conveyor.end_x - 10 
             
        # Use read-only height property
        self.y = self.current_conveyor.y - self.height
        
        self.status = self.STATE_MOVING
        self.base_speed = self.__get_speed_by_difficulty()
        
        # RESTORED: Visual level index
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

    def __get_speed_by_difficulty(self) -> float:
        """ Private auxiliary method to determine speed """
        if self.difficulty == "EASY": return constants.SLOW_SPEED
        elif self.difficulty == "MEDIUM": return constants.SLOW_SPEED 
        elif self.difficulty == "EXTREME": return constants.MEDIUM_SPEED
        elif self.difficulty == "CRAZY": return constants.RANDOM_SPEED
        return constants.SLOW_SPEED

    def __get_sprite_list(self) -> list:
        """ Private auxiliary method to determine sprites """
        if self.difficulty == "EASY": return constants.PCK_EASY_SPRITES
        elif self.difficulty == "MEDIUM": return constants.PCK_MEDIUM_SPRITES
        elif self.difficulty == "EXTREME": return constants.PCK_EXTREME_SPRITES
        elif self.difficulty == "CRAZY": return constants.PCK_CRAZY_SPRITES
        return constants.PCK_EASY_SPRITES

    def advance_to_conveyor(self, next_conveyor: Conveyor):
        """ Jumps the package to the next conveyor object. """
        self.current_conveyor = next_conveyor
        self.floor_index += 1
        
        if self.current_conveyor.direction == 1: # Right
            self.x = self.current_conveyor.x
        else: # Left
            self.x = self.current_conveyor.end_x - 10

        self.y = self.current_conveyor.y - self.height
        self.status = self.STATE_MOVING

    def update(self):
        """
        Updates package logic.
        """
        if self.status == self.STATE_MOVING:
            # 1. Movement
            speed = 1 if self.floor_index == 0 else self.base_speed
            direction = self.current_conveyor.direction
            
            # Store previous X to detect crossing
            prev_x = self.x
            self.x += speed * direction

            # 2. RESTORED: Visuals (Level Up)
            # We check against static constants, so no extra coupling is introduced.
            trigger_x = constants.CENTER_SCREEN
            
            # If we crossed the center line in either direction
            if (direction == -1 and prev_x > trigger_x and self.x <= trigger_x) or \
               (direction == 1 and prev_x < trigger_x and self.x >= trigger_x):
                self.level_index += 1

        elif self.status == self.STATE_FALLING:
            self.y += 2

    def draw(self):
        # RESTORED: Select sprite based on level_index
        # Each level has 2 sprites (normal, falling), so we multiply by 2
        sprite_idx = self.level_index * 2
        
        # Safety check: ensure we don't go out of bounds of the sprite list
        if sprite_idx >= len(self.sprite_list): 
            sprite_idx = len(self.sprite_list) - 2
        
        # Use falling sprite visual if falling (next sprite in list)
        if self.status == self.STATE_FALLING:
             sprite_idx += 1 
             
        sprite = self.sprite_list[sprite_idx]
        img, u, v, w, h, colkey = sprite
        
        # Cast to int for drawing
        pyxel.blt(int(self.x), int(self.y), img, u, v, w, h, colkey)
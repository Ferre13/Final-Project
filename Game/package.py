import pyxel
import constants
from conveyor import Conveyor 

class Package:
    """
    Represents a package. Uses centralized constants for states and logic.
    """
    def __init__(self, difficulty: str, start_conveyor: Conveyor, floor_index: int):
        self.__difficulty = difficulty
        self.__width = constants.PCK_LVL1[3]
        self.__height = constants.PCK_LVL1[4]
        
        self.current_conveyor = start_conveyor
        self.floor_index = floor_index
        
        self.__sprite_list = self.__get_sprite_list()
        
        # Position Logic
        if self.current_conveyor.direction == 1:
             self.x = self.current_conveyor.x
        else:
             self.x = self.current_conveyor.end_x - 10 
             
        self.y = self.current_conveyor.y - self.height
        
        self.state = constants.PKG_STATE_MOVING
        self.level_index = 0 

    # --- GETTERS AND SETTERS ---
    @property
    def x(self) -> float: return self.__x
    @x.setter
    def x(self, value: float): self.__x = float(value)

    @property
    def y(self) -> float: return self.__y
    @y.setter
    def y(self, value: float): self.__y = float(value)

    @property
    def width(self) -> int: return self.__width
    @property
    def height(self) -> int: return self.__height

    @property
    def floor_index(self) -> int: return self.__floor_index
    @floor_index.setter
    def floor_index(self, value: int):
        if not isinstance(value, int): raise TypeError("Floor index must be int")
        self.__floor_index = value

    @property
    def current_conveyor(self) -> Conveyor: return self.__current_conveyor
    @current_conveyor.setter
    def current_conveyor(self, value: Conveyor):
        if not isinstance(value, Conveyor): raise TypeError("Must be Conveyor")
        self.__current_conveyor = value

    # --- LOGIC ---

    def __get_sprite_list(self) -> list:
        if self.__difficulty == "EASY": return constants.PCK_EASY_SPRITES
        elif self.__difficulty == "MEDIUM": return constants.PCK_MEDIUM_SPRITES
        elif self.__difficulty == "EXTREME": return constants.PCK_EXTREME_SPRITES
        elif self.__difficulty == "CRAZY": return constants.PCK_CRAZY_SPRITES
        return constants.PCK_EASY_SPRITES

    def advance_to_conveyor(self, next_conveyor: Conveyor):
        self.current_conveyor = next_conveyor
        self.floor_index += 1
        
        if self.current_conveyor.direction == 1: 
            self.x = self.current_conveyor.x - constants.OVERHANG_LIMIT
        else: 
            self.x = self.current_conveyor.end_x + constants.OVERHANG_LIMIT - self.width

        self.y = self.current_conveyor.y - self.height
        self.state = constants.PKG_STATE_MOVING

    def fall(self):
        self.state = constants.PKG_STATE_FALLING

    def update(self) -> int:
        # CASE 1: FALLING
        if self.state == constants.PKG_STATE_FALLING:
            self.y += constants.PACKAGE_FALL_SPEED
            
            if self.y > constants.SCREEN_HEIGHT:
                # FIX: Blame based on FLOOR territory, not direction.
                # Even floors (0, 2, 4...) are Mario's responsibility.
                if self.floor_index % 2 == 0:
                    return constants.PKG_STATUS_FALLEN_MARIO
                else:
                    return constants.PKG_STATUS_FALLEN_LUIGI
            return constants.PKG_STATUS_MOVING

        # CASE 2: MOVING
        elif self.state == constants.PKG_STATE_MOVING:
            speed = self.current_conveyor.speed
            direction = self.current_conveyor.direction
            
            prev_x = self.x
            self.x += speed * direction

            # Level Up Visuals
            trigger_x = constants.CENTER_SCREEN
            if (direction == -1 and prev_x > trigger_x and self.x <= trigger_x) or \
               (direction == 1 and prev_x < trigger_x and self.x >= trigger_x):
                self.level_index += 1

            # Boundaries
            reached = False
            if direction == 1:
                limit = self.current_conveyor.end_x + constants.OVERHANG_LIMIT
                if self.x + self.width >= limit:
                    self.x = limit - self.width 
                    reached = True
            else:
                limit = self.current_conveyor.x - constants.OVERHANG_LIMIT
                if self.x <= limit:
                    self.x = limit 
                    reached = True
            
            if reached:
                return constants.PKG_STATUS_REACHED_END
            
            return constants.PKG_STATUS_MOVING

    def draw(self):
        sprite_idx = self.level_index * 2
        if sprite_idx >= len(self.__sprite_list): 
            sprite_idx = len(self.__sprite_list) - 2
        
        if self.state == constants.PKG_STATE_FALLING:
             sprite_idx += 1 
             
        sprite = self.__sprite_list[sprite_idx]
        img, u, v, w, h, colkey = sprite
        pyxel.blt(int(self.x), int(self.y), img, u, v, w, h, colkey)
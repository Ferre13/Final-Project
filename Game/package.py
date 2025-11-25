import pyxel
import constants
from conveyor import Conveyor 

class Package:
    """
    Represents a package moving through the factory.
    Uses State Machine (MOVING -> FALLING) and checks collisions internally.
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
        self.sprite_list = self._get_sprite_list()
        
        # Position logic
        if self.current_conveyor.direction == 1:
             self.x = self.current_conveyor.x
        else:
             self.x = self.current_conveyor.end_x - 10 
             
        # Use read-only height property
        self.y = self.current_conveyor.y - self.height
        
        self.status = self.STATE_MOVING
        self.base_speed = self._get_speed_by_difficulty()
        self.level_index = 0 

    @property
    def x(self) -> int: return self.__x
    @x.setter
    def x(self, value: int): self.__x = int(value)

    @property
    def y(self) -> int: return self.__y
    @y.setter
    def y(self, value: int): self.__y = int(value)

    @property
    def difficulty(self) -> str: return self.__difficulty
    @property
    def width(self) -> int: return self.__width
    @property
    def height(self) -> int: return self.__height

    def _get_speed_by_difficulty(self) -> float:
        if self.difficulty == "EASY": return constants.SLOW_SPEED
        elif self.difficulty == "MEDIUM": return constants.SLOW_SPEED 
        elif self.difficulty == "EXTREME": return constants.MEDIUM_SPEED
        elif self.difficulty == "CRAZY": return constants.RANDOM_SPEED
        return constants.SLOW_SPEED

    def _get_sprite_list(self) -> list:
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

    def update(self, mario, luigi, conveyors: list, truck):
        """
        Updates package logic using State Machine.
        """
        if self.status == self.STATE_MOVING:
            # 1. Movement
            speed = 1 if self.floor_index == 0 else self.base_speed
            direction = self.current_conveyor.direction
            prev_x = self.x
            self.x += speed * direction

            # 2. Visuals (Level Up)
            trigger_x = constants.CENTER_SCREEN
            if (direction == -1 and prev_x > trigger_x and self.x <= trigger_x) or \
               (direction == 1 and prev_x < trigger_x and self.x >= trigger_x):
                self.level_index += 1
            
            # 3. Check End of Conveyor
            reached_end = False
            if direction == 1 and self.x >= self.current_conveyor.end_x:
                self.x = self.current_conveyor.end_x
                reached_end = True
            elif direction == -1 and self.x <= self.current_conveyor.x:
                self.x = self.current_conveyor.x
                reached_end = True
            
            # 4. State Transition Logic
            if reached_end:
                # Check for Character Collision
                # Machine (Index 0) -> Mario (Floor 0)
                # Belt 1 (Index 1) -> Luigi (Floor 1)
                # Belt 2 (Index 2) -> Mario (Floor 2)
                required_floor = self.floor_index
                
                # Check if ANY character is on the required floor
                character_present = False
                if mario.floor == required_floor or luigi.floor == required_floor:
                    character_present = True
                
                if character_present:
                    # Move to next conveyor
                    next_idx = self.floor_index + 1
                    if next_idx < len(conveyors):
                        self.advance_to_conveyor(conveyors[next_idx])
                    else:
                        # Truck Delivery
                        truck.receive_package()
                        self.status = "delivered" 
                else:
                    # No character -> FALL
                    self.status = self.STATE_FALLING

        elif self.status == self.STATE_FALLING:
            self.y += 2
            if self.y > constants.SCREEN_HEIGHT:
                 self.status = "lost"

    def draw(self):
        sprite_idx = self.level_index * 2
        if sprite_idx >= len(self.sprite_list): 
            sprite_idx = len(self.sprite_list) - 2
        
        # Use falling sprite visual if falling
        if self.status == self.STATE_FALLING:
             sprite_idx += 1 
             
        sprite = self.sprite_list[sprite_idx]
        img, u, v, w, h, colkey = sprite
        pyxel.blt(self.x, self.y, img, u, v, w, h, colkey)
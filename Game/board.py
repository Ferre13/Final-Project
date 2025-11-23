import pyxel
import constants
from truck import Truck
from conveyor import Conveyor
from platforms import Platform
from background import VerticalStructure, Machine, ExitSignal

class Board:
    def __init__(self, difficulty: str):
        self.difficulty = difficulty
        self.floors = []
        self.conveyors = []
        self.platforms = []
        self.truck = Truck(constants.TRUCK_X, 0)
        
        self.vertical_structure = VerticalStructure(constants.STRUCT_X, 2)
        self.machine = Machine(constants.MACHINE_X, constants.MACHINE_Y)
        self.exit_signal = None 

        self.init_level()

    @property
    def conveyors(self) -> list:
        return self.__conveyors
    
    @conveyors.setter
    def conveyors(self, value: list):
        if not isinstance(value, list):
            raise TypeError("Conveyors must be a list")
        self.__conveyors = value

    @property
    def truck(self) -> Truck:
        return self.__truck

    @truck.setter
    def truck(self, value: Truck):
        if not isinstance(value, Truck):
            raise TypeError("Truck must be an instance of Truck class")
        self.__truck = value

    @property
    def platforms(self) -> list:
        return self.__platforms
    
    @platforms.setter
    def platforms(self, value: list):
        if not isinstance(value, list):
            raise TypeError("Platforms must be a list")
        self.__platforms = value

    def init_level(self):
        if self.difficulty == "EASY" or self.difficulty == "CRAZY":
            self.floors = constants.FLOORS_EASY
        elif self.difficulty == "MEDIUM":
            self.floors = constants.FLOORS_MEDIUM
        elif self.difficulty == "EXTREME":
            self.floors = constants.FLOORS_EXTREME
        else:
            self.floors = constants.FLOORS_EASY

        # Dynamic Truck Alignment
        top_floor_y = min(self.floors)
        
        # Aligned exactly with the top floor (Offset 0)
        self.truck.y = top_floor_y 
        
        # Signal moves with the truck
        self.exit_signal = ExitSignal(2, self.truck.y - 10)

        # 0. Create Platform 0 (Specific Bottom-Right Structure)
        start_y = constants.SCREEN_HEIGHT - 8
        sprite_h = constants.PLATFORM_0_SPRITE[4]
        
        num_segments = 8 // sprite_h
        
        for i in range(num_segments):
            y = start_y + (i * sprite_h)
            p = Platform(
                constants.MARIO_X, 
                y, 
                1, 
                is_flipped=False, 
                sprite=constants.PLATFORM_0_SPRITE
            )
            self.platforms.append(p)

        for i, y_pos in enumerate(self.floors):
            speed = constants.SLOW_SPEED
            direction = 1 if i % 2 != 0 else -1
            
            # 1. Left Conveyor
            left_conv = Conveyor(
                constants.CONVEYOR_X_LEFT, 
                y_pos, 
                constants.CONVEYOR_LENGTH, 
                speed, 
                direction,
                is_right_side=False 
            )
            self.conveyors.append(left_conv)

            # 2. Right Conveyor
            right_conv = Conveyor(
                constants.CONVEYOR_X_RIGHT, 
                y_pos, 
                constants.CONVEYOR_LENGTH, 
                speed, 
                direction,
                is_right_side=True 
            )
            self.conveyors.append(right_conv)

            # 3. EXTRA: Machine Connection (Only on Bottom Floor i=0)
            if i == 0:
                machine_conv = Conveyor(
                    constants.MACHINE_CONV_X,
                    y_pos,
                    constants.MACHINE_CONV_LENGTH, 
                    speed,
                    direction,
                    is_right_side=False 
                )
                self.conveyors.append(machine_conv)

            # 4. Platforms
            plat_y = y_pos - 4
            
            if i % 2 != 0:
                mario_plat = Platform(constants.MARIO_X, plat_y, 1, is_flipped=True)
                self.platforms.append(mario_plat)
            else:
                luigi_plat = Platform(constants.LUIGI_X, plat_y, 1, is_flipped=False)
                self.platforms.append(luigi_plat)

    def update(self):
        self.truck.update()

    def draw(self):
        self.vertical_structure.draw()
        self.machine.draw()
        if self.exit_signal:
            self.exit_signal.draw()

        for platform in self.platforms:
            platform.draw()

        for conv in self.conveyors:
            conv.draw()

        self.truck.draw()
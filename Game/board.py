import pyxel
import constants
from truck import Truck
from conveyor import Conveyor
from platforms import Platform
from background import VerticalStructure, Machine, ExitSignal, Window, LevelSign

class Board:
    def __init__(self, difficulty: str):
        self.difficulty = difficulty
        self.floors = []
        self.conveyors = []
        self.platforms = []
        self.truck = Truck(constants.TRUCK_X, 0)
        
        self.level_sign = LevelSign(self.difficulty, 4, constants.SCREEN_HEIGHT - 22)
        self.machine = Machine(constants.MACHINE_X, constants.MACHINE_Y)
        self.exit_signal = None 
        self.windows = [Window(20, 15), Window(215, 35), Window(210, 45)]
        self.door_x = 0
        self.door_y = 0

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
            self.floors = constants.FLOORS_EASY_CRAZY
        elif self.difficulty == "MEDIUM":
            self.floors = constants.FLOORS_MEDIUM
        elif self.difficulty == "EXTREME":
            self.floors = constants.FLOORS_EXTREME
        else:
            self.floors = constants.FLOORS_EASY_CRAZY

        # --- 1. CALCULATE COORDINATES ---
        top_floor_y = min(self.floors)
        self.truck.y = top_floor_y 
        self.exit_signal = ExitSignal(2, self.truck.y - 10)

        # Ground Params
        sprite_h = constants.PLATFORM_0_SPRITE[4] # 2px
        sprite_w = constants.PLATFORM_0_SPRITE[3] # 14px
        ground_height_px = 11
        ground_start_y = constants.SCREEN_HEIGHT - ground_height_px

        # --- 2. VERTICAL STRUCTURE ---
        self.vertical_structure = VerticalStructure(
            constants.STRUCT_X, 
            2, 
            top_floor_y, 
            base_y=ground_start_y
        )

        # --- 3. CONVEYORS & LADDERS ---
        # We create these BEFORE the ground so they are drawn BEHIND it.
        for i, y_pos in enumerate(self.floors):
            speed = constants.SLOW_SPEED
            direction = 1 if i % 2 != 0 else -1
            
            # Conveyors
            left_conv = Conveyor(
                constants.CONVEYOR_X_LEFT, y_pos, constants.CONVEYOR_LENGTH, 
                speed, direction, is_right_side=False 
            )
            self.conveyors.append(left_conv)

            right_conv = Conveyor(
                constants.CONVEYOR_X_RIGHT, y_pos, constants.CONVEYOR_LENGTH, 
                speed, direction, is_right_side=True 
            )
            self.conveyors.append(right_conv)

            # Machine Connection
            if i == 0:
                machine_conv = Conveyor(
                    constants.MACHINE_CONV_X, y_pos, constants.MACHINE_CONV_LENGTH, 
                    speed, direction, is_right_side=False 
                )
                self.conveyors.append(machine_conv)

            # Platforms (The Ladders)
            plat_y = y_pos - 3
            if i % 2 != 0:
                mario_plat = Platform(constants.MARIO_X, plat_y, 1, is_flipped=True)
                self.platforms.append(mario_plat)
            else:
                luigi_plat = Platform(constants.LUIGI_X, plat_y, 1, is_flipped=False)
                self.platforms.append(luigi_plat)

        # --- 4. TRUCK FLOOR ---
        truck_floor_y = self.truck.y + 16 
        truck_floor_segments = 2
        truck_floor_width = 3
        
        for i in range(truck_floor_segments):
            y = truck_floor_y + (i * sprite_h)
            p = Platform(0, y, truck_floor_width, is_flipped=False, sprite=constants.PLATFORM_0_SPRITE)
            self.platforms.append(p)

        # --- 5. BOSS & DOOR FLOORS ---
        boss_floor_y = constants.MACHINE_Y - 5
        boss_floor_width = 2
        
        boss_plat_left = Platform(
            0, boss_floor_y, boss_floor_width, 
            is_flipped=False, sprite=constants.PLATFORM_0_SPRITE
        )
        self.platforms.append(boss_plat_left)

        right_start_x = constants.SCREEN_WIDTH - (boss_floor_width * sprite_w)
        boss_plat_right = Platform(
            right_start_x, boss_floor_y, boss_floor_width, 
            is_flipped=False, sprite=constants.PLATFORM_0_SPRITE
        )
        self.platforms.append(boss_plat_right)


        # --- 6. GLOBAL GROUND ---
        # Appended LAST so it is drawn LAST (on top of the ladder bottoms)
        ground_rows = (ground_height_px + sprite_h - 1) // sprite_h
        sprites_per_row = (constants.SCREEN_WIDTH // sprite_w) + 1
        
        for r in range(ground_rows):
            y = ground_start_y + (r * sprite_h)
            ground_plat = Platform(
                0, y, sprites_per_row, 
                is_flipped=False, sprite=constants.PLATFORM_0_SPRITE
            )
            self.platforms.append(ground_plat)

    def update(self):
        self.truck.update()

    def draw(self):
        if self.vertical_structure:
            self.vertical_structure.draw()
        
        self.level_sign.draw()

        for w in self.windows:
            w.draw()

        self.machine.draw()
        
        if self.exit_signal:
            self.exit_signal.draw()

        for platform in self.platforms:
            platform.draw()

        for conv in self.conveyors:
            conv.draw()

        self.truck.draw()
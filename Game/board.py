import pyxel
import constants
from characters import Character
from truck import Truck
from conveyor import Conveyor
from platforms import Platform
from background import VerticalStructure, Machine, ExitSignal, Window, LevelSign

class Board:
    def __init__(self, difficulty: str):
        self.difficulty = difficulty
        self.truck = Truck(constants.TRUCK_X, 0)
        
        # These are static elements, they dont change when the game restarts
        self.machine = Machine(constants.MACHINE_X, constants.MACHINE_Y)
        self.windows = [Window(20, 15), Window(215, 35), Window(210, 45)]

        self.game_start()

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

    def game_start(self):
        # Reset for a new game
        self.conveyors = []
        self.platforms = []

        self.mario = Character("Mario", constants.MARIO_X + 3)
        self.luigi = Character("Luigi", constants.LUIGI_X + 4)

        # Create Level Sign
        self.level_sign = LevelSign(self.difficulty, 4, constants.SCREEN_HEIGHT - 22)

        # Set floors based on difficulty
        if self.difficulty == "EASY" or self.difficulty == "CRAZY":
            self.floors = constants.FLOORS_EASY_CRAZY
        elif self.difficulty == "MEDIUM":
            self.floors = constants.FLOORS_MEDIUM
        elif self.difficulty == "EXTREME":
            self.floors = constants.FLOORS_EXTREME
        else:
            self.floors = constants.FLOORS_EASY_CRAZY

        # Calculate truck.y based on top floor and limit for vertical structure
        # truck.y is used for the exit signal position as well
        top_floor_y = self.floors[-1]
        self.truck.y = top_floor_y 
        self.truck.reset()

        # Ground calculations
        ground_height_px = 6
        ground_start_y = constants.SCREEN_HEIGHT - ground_height_px

        # Create Exit Signal
        self.exit_signal = ExitSignal(2, self.truck.y - 10)
        # Vertical Structure
        self.vertical_structure = VerticalStructure(constants.STRUCT_X, 2, top_floor_y, ground_start_y)

        # Create Conveyors and Platforms
        # Enumerate returns index and value (0, FLOOR_Y_POSITIONS[0])
        for index, y_pos in enumerate(self.floors):
            # Change based on difficulty
            speed = constants.SLOW_SPEED

            if index % 2 != 0:
                plat_x = constants.MARIO_X
            else:
                plat_x = constants.LUIGI_X

            self.platforms.append(Platform(plat_x, y_pos + 2, 1))

            if index % 2 == 0:
                direction = -1
            else:
                direction = 1
            
            # Conveyors
            self.conveyors.append(Conveyor(constants.CONVEYOR_X_LEFT, y_pos, constants.CONVEYOR_LENGTH, speed, direction, False))
            self.conveyors.append(Conveyor(constants.CONVEYOR_X_RIGHT, y_pos, constants.CONVEYOR_LENGTH, speed, direction, True))

            # Machine Connection
            if index == 0:
                self.conveyors.append(Conveyor(constants.CONVEYOR_0_X, y_pos, constants.CONVEYOR_0_LENGTH, speed, direction, False))
        
        # Ground Calculations
        sprite_h = constants.FLOOR_SPRITE[4]
        sprite_w = constants.FLOOR_SPRITE[3]

        # Truck Platform
        # Floor is 16px lower than the truck, accordint to truck height
        truck_floor_y = self.truck.y + 16
        truck_floor_height = 2
        truck_floor_width = 3
        
        for height in range(truck_floor_height):
            y = truck_floor_y + (height * sprite_h)
            floor = Platform(0, y, truck_floor_width, constants.FLOOR_SPRITE)
            self.platforms.append(floor)

        # Boss Platforms
        # Floor is 2px below the boss y position
        boss_floor_y = constants.BOSS_Y + 2
        boss_floor_width = 2
        
        boss_plat_left = Platform(0, boss_floor_y, boss_floor_width, constants.FLOOR_SPRITE)
        self.platforms.append(boss_plat_left)

        right_start_x = constants.SCREEN_WIDTH - (boss_floor_width * sprite_w)
        boss_plat_right = Platform(right_start_x, boss_floor_y, boss_floor_width, constants.FLOOR_SPRITE)
        self.platforms.append(boss_plat_right)


        # Ground
        ground_rows = (ground_height_px + sprite_h - 1) // sprite_h
        sprites_per_row = (constants.SCREEN_WIDTH // sprite_w) + 1
        
        for each in range(ground_rows):
            y = ground_start_y + (each * sprite_h)
            ground_plat = Platform(0, y, sprites_per_row, constants.FLOOR_SPRITE)
            self.platforms.append(ground_plat)

    def update(self):
        self.mario.update(self.floors)
        self.luigi.update(self.floors)
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.truck.update()

    # Draw all elements
    def draw(self):

        self.vertical_structure.draw()
        self.level_sign.draw()
        for w in self.windows:
            w.draw()
        self.machine.draw()
        self.exit_signal.draw()
        for platform in self.platforms:
            platform.draw()
        for conv in self.conveyors:
            conv.draw()
        self.mario.draw()
        self.luigi.draw()
        self.truck.draw()
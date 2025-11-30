import constants
from characters import Character
from truck import Truck
from conveyor import Conveyor
from platforms import Platform
from background import VerticalStructure, Machine, ExitSignal, Window, LevelSign
from boss import Boss
from door import Door

class Factory:
    """
    A factory class responsible for creating all the game objects.
    This helps to keep the Board class clean and focused on game logic,
    not on object creation.
    """
    def __init__(self, difficulty: str):
        """
        Initializes the factory with a given difficulty.
        
        :param difficulty: The game difficulty, which affects object creation.
        """
        self.difficulty = difficulty
        if self.difficulty in ["EASY", "CRAZY"]: 
            self.floor_y_positions = constants.FLOORS_EASY_CRAZY
        elif self.difficulty == "MEDIUM":
            self.floor_y_positions = constants.FLOORS_MEDIUM
        elif self.difficulty == "EXTREME":
            self.floor_y_positions = constants.FLOORS_EXTREME
        else:
            self.floor_y_positions = constants.FLOORS_EASY_CRAZY
        
        self.num_floors = len(self.floor_y_positions)
        self.platforms = []
        self.conveyors = []

    def create_background(self):
        """Creates the static background elements."""
        windows = [Window(20, 15), Window(215, 35), Window(215, 45)]
        machine = Machine(constants.MACHINE_X, constants.MACHINE_Y)
        level_sign = LevelSign(self.difficulty, 4, constants.SCREEN_HEIGHT - 18)
        return windows, machine, level_sign

    def create_world(self):
        """Creates the dynamic elements of the game world like conveyors and platforms."""
        top_floor_y = self.floor_y_positions[-1]
        truck = Truck(constants.TRUCK_X, top_floor_y - 5)
        truck.reset()

        ground_y = constants.SCREEN_HEIGHT - 6
        exit_signal = ExitSignal(2, truck.y - 10)
        vertical_structure = VerticalStructure(constants.STRUCT_X, 2, top_floor_y, ground_y)

        self.conveyors.append(Conveyor(
            constants.CONVEYOR_0_X, self.floor_y_positions[0], 1, -1, self.difficulty, 0
        ))
        
        for i, y_pos in enumerate(self.floor_y_positions):
            level_idx = i + 1
            if i % 2 == 0: direction = -1
            else: direction = 1
            
            if i % 2 != 0: plat_x = constants.MARIO_X
            else: plat_x = constants.LUIGI_X
            
            self.platforms.append(Platform(plat_x, y_pos + 2, 1))
            self.conveyors.append(Conveyor(
                constants.CONVEYOR_X_START, y_pos, constants.CONVEYOR_SEGMENTS, 
                direction, self.difficulty, level_idx
            ))

        self.__create_extra_platforms(ground_y, truck)
        
        return truck, exit_signal, vertical_structure, self.platforms, self.conveyors

    def __create_extra_platforms(self, ground_start_y: int, truck: Truck):
        """Creates decorative platforms for the ground and boss area."""
        sprite_h = constants.FLOOR_SPRITE[4]
        truck_floor_y = truck.y + truck.height 
        for h in range(2):
            self.platforms.append(Platform(0, truck_floor_y + (h * sprite_h), 5, constants.FLOOR_SPRITE))

        self.platforms.append(Platform(0, constants.BOSS_Y, 4, constants.FLOOR_SPRITE))
        right_x = constants.SCREEN_WIDTH - (4 * constants.FLOOR_SPRITE[3])
        self.platforms.append(Platform(right_x, constants.BOSS_Y, 4, constants.FLOOR_SPRITE))

        ground_rows = (6 + sprite_h - 1) // sprite_h
        sprites_per_row = (constants.SCREEN_WIDTH // constants.FLOOR_SPRITE[3]) + 1
        for row in range(ground_rows):
            self.platforms.append(Platform(0, ground_start_y + (row * sprite_h), sprites_per_row, constants.FLOOR_SPRITE))

    def create_characters(self):
        """Creates the player characters and the boss."""
        mario = Character("Mario", constants.MARIO_X + 2, self.difficulty, self.num_floors)
        luigi = Character("Luigi", constants.LUIGI_X + 3, self.difficulty, self.num_floors)
        
        door_y = constants.BOSS_Y - constants.DOOR_OPEN[4]
        door_left = Door(constants.BOSS_LUIGI, door_y)
        door_right = Door(constants.BOSS_MARIO, door_y)
        boss = Boss(door_left, door_right)
        
        return mario, luigi, boss, door_left, door_right

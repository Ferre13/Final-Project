import constants
from character import Mario, Luigi
from truck import Truck
from conveyor import Conveyor
from game_platform import Platform
from vertical_structure import VerticalStructure
from machine import Machine
from exit_signal import ExitSignal
from window import Window
from level_sign import LevelSign
from boss import Boss
from door import Door

class Factory:
    """Creates and configures all game objects based on difficulty."""
    def __init__(self, difficulty: str):
        """
        Initializes the factory.
        :param difficulty: The game difficulty, which affects how objects are created.
        """
        self.difficulty = difficulty
        # Map difficulty to floor configurations
        floor_configurations = {"EASY": constants.FLOORS_EASY_CRAZY, "CRAZY": constants.FLOORS_EASY_CRAZY, 
                                "MEDIUM": constants.FLOORS_MEDIUM, "EXTREME": constants.FLOORS_EXTREME}
        # Calculate floor positions based on difficulty
        self.floor_y_positions = floor_configurations[self.difficulty]
        self.num_floors = len(self.floor_y_positions)
        self.platforms = []
        self.conveyors = []
        self.windows = []
        # We initialize these later, but define here for clarity
        self.machine = None
        self.level_sign = None
        self.truck = None
        self.exit_signal = None
        self.vertical_structure = None
        self.mario = None
        self.luigi = None
        self.boss = None
        self.door_left = None
        self.door_right = None

    def create_all_objects(self):
        """Runs all creation methods to build the game world."""
        self.create_background_elements()
        self.create_world_elements()
        self.create_characters_and_boss()

    def create_background_elements(self):
        """Creates static background scenery."""
        self.windows = [Window(20, 15), Window(215, 35), Window(215, 45)]
        self.machine = Machine(constants.MACHINE_X, constants.MACHINE_Y)
        self.level_sign = LevelSign(self.difficulty, constants.LEVEL_SIGN_X, constants.SCREEN_HEIGHT - constants.LEVEL_SIGN_Y_OFFSET)

    def create_world_elements(self):
        """Creates interactive world elements like conveyors and platforms."""
        top_floor_y = self.floor_y_positions[-1]
        self.truck = Truck(constants.TRUCK_X, top_floor_y + constants.TRUCK_Y_OFFSET)
        self.truck.reset()

        ground_y = constants.SCREEN_HEIGHT - 6
        self.exit_signal = ExitSignal(constants.EXIT_SIGNAL_X, self.truck.y + constants.EXIT_SIGNAL_Y_OFFSET)
        self.vertical_structure = VerticalStructure(constants.STRUCT_X, constants.VERTICAL_STRUCTURE_WIDTH, top_floor_y, ground_y)

        self.conveyors.append(Conveyor(
            constants.CONVEYOR_0_X, self.floor_y_positions[0], 1, -1, self.difficulty, 0
        ))
        for i, y_pos in enumerate(self.floor_y_positions):
            level_idx = i + 1
            is_even_floor = (i % 2 == 0)
            if is_even_floor:
                direction = -1
                plat_x = constants.LUIGI_X
            else:
                direction = 1
                plat_x = constants.MARIO_X
            self.platforms.append(Platform(plat_x, y_pos + 2, 1))
            self.conveyors.append(Conveyor(
                constants.CONVEYOR_X_START, y_pos, constants.CONVEYOR_SEGMENTS, 
                direction, self.difficulty, level_idx
            ))
        self.__create_extra_platforms(ground_y, self.truck)

    def __create_extra_platforms(self, ground_start_y: int, truck: Truck):
        """
        Creates platforms for the ground, boss and truck area.
        :param ground_start_y: The y-coordinate of the ground.
        :param truck: The truck object, used for positioning.
        """
        sprite_h = constants.FLOOR_SPRITE[4]
        # Truck platform
        truck_floor_y = truck.y + truck.height 
        for h in range(constants.TRUCK_PLATFORM_ROWS):
            self.platforms.append(Platform(0, truck_floor_y + (h * sprite_h), 5, constants.FLOOR_SPRITE))

        # Boss platforms
        self.platforms.append(Platform(0, constants.BOSS_Y, 4, constants.FLOOR_SPRITE))
        right_x = constants.SCREEN_WIDTH - (4 * constants.FLOOR_SPRITE[3])
        self.platforms.append(Platform(right_x, constants.BOSS_Y, 4, constants.FLOOR_SPRITE))

        # Ground
        ground_rows = (6 + sprite_h - 1) // sprite_h
        sprites_per_row = (constants.SCREEN_WIDTH // constants.FLOOR_SPRITE[3]) + 1
        for row in range(ground_rows):
            self.platforms.append(Platform(0, ground_start_y + (row * sprite_h), sprites_per_row, constants.FLOOR_SPRITE))

    def create_characters_and_boss(self):
        """Creates the Mario, Luigi, and Boss objects (including doors)."""
        self.mario = Mario(constants.MARIO_X + 2, self.difficulty, self.num_floors)
        self.luigi = Luigi(constants.LUIGI_X + 3, self.difficulty, self.num_floors)
        
        door_y = constants.BOSS_Y - constants.DOOR_OPEN[4]
        self.door_left = Door(constants.BOSS_LUIGI, door_y)
        self.door_right = Door(constants.BOSS_MARIO, door_y)
        self.boss = Boss(self.door_left, self.door_right)
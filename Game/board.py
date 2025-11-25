import pyxel
import random
import constants
from characters import Character
from truck import Truck
from conveyor import Conveyor
from platforms import Platform
from background import VerticalStructure, Machine, ExitSignal, Window, LevelSign
from boss import Boss
from door import Door
from package import Package

class Board:
    def __init__(self, difficulty: str):
        self.init_configuration(difficulty)
        self.create_background()
        self.create_world()
        self.create_actors()

    # --- INITIALIZATION METHODS ---

    def init_configuration(self, difficulty: str):
        self.difficulty = difficulty
        self.score = 0
        self.failures = 0
        self.spawn_timer = 0
        self.packages = []
        
        self.is_punishing = False
        self.punishment_timer = 0
        self.punished_char = None
        self.active_door = None
        
        self.floor_max_index = 0

    def create_background(self):
        self.windows = [Window(20, 15), Window(215, 35), Window(215, 45)]
        self.machine = Machine(constants.MACHINE_X, constants.MACHINE_Y)
        self.level_sign = LevelSign(self.difficulty, 4, constants.SCREEN_HEIGHT - 18)

    def create_world(self):
        # 1. Determine Floors
        floor_y_positions = []
        if self.difficulty == "EASY" or self.difficulty == "CRAZY": 
            floor_y_positions = constants.FLOORS_EASY_CRAZY
        elif self.difficulty == "MEDIUM": 
            floor_y_positions = constants.FLOORS_MEDIUM
        elif self.difficulty == "EXTREME": 
            floor_y_positions = constants.FLOORS_EXTREME
        else: 
            floor_y_positions = constants.FLOORS_EASY_CRAZY
            
        self.floor_max_index = len(floor_y_positions)

        # 2. Setup Truck position
        self.truck = Truck(constants.TRUCK_X, 0)
        top_floor_y = floor_y_positions[-1]
        self.truck.y = top_floor_y - 5 
        self.truck.reset()

        # 3. Create Structures
        ground_height_px = 6
        ground_start_y = constants.SCREEN_HEIGHT - ground_height_px
        self.exit_signal = ExitSignal(2, self.truck.y - 10)
        self.vertical_structure = VerticalStructure(constants.STRUCT_X, 2, top_floor_y, ground_start_y)

        # 4. Create Conveyors & Platforms
        self.conveyors = []
        self.platforms = []

        # Machine Conveyor (Always 1x Speed)
        self.conveyors.append(Conveyor(constants.CONVEYOR_0_X, floor_y_positions[0], 1, 1.0, -1))
        
        # Main Loops for Conveyors
        for index, y_pos in enumerate(floor_y_positions):
            # Direction Logic
            if index % 2 == 0: direction = -1 # Odd (1st, 3rd...) -> Goes Left
            else: direction = 1 # Even (2nd, 4th...) -> Goes Right
            
            # Platform Logic
            plat_x = constants.MARIO_X if index % 2 != 0 else constants.LUIGI_X
            self.platforms.append(Platform(plat_x, y_pos + 2, 1))
            
            # --- CORRECT SPEED CALCULATION ---
            # Index 0 is the first belt in the loop (Conveyor 1, Odd)
            is_odd_belt = (index % 2 == 0)
            
            speed = 1.0 # Default (EASY)
            
            if self.difficulty == "MEDIUM":
                if is_odd_belt: speed = 1.5
                else: speed = 1.0
            elif self.difficulty == "EXTREME":
                if is_odd_belt: speed = 2.0
                else: speed = 1.5
            elif self.difficulty == "CRAZY":
                # Random float between 1.0 and 2.0 for EACH belt
                speed = random.uniform(1.0, 2.0)
            
            self.conveyors.append(Conveyor(constants.CONVEYOR_X_START, y_pos, constants.CONVEYOR_SEGMENTS, speed, direction))

        # 5. Create Extra Platforms
        self.create_extra_platforms(ground_start_y)

    def create_extra_platforms(self, ground_start_y: int):
        sprite_h = constants.FLOOR_SPRITE[4]
        sprite_w = constants.FLOOR_SPRITE[3]
        
        # Truck Platform
        truck_floor_y = self.truck.y + self.truck.height 
        for height in range(2):
            y = truck_floor_y + (height * sprite_h)
            self.platforms.append(Platform(0, y, 5, constants.FLOOR_SPRITE))

        # Boss Platforms
        boss_floor_y = constants.BOSS_Y
        self.platforms.append(Platform(0, boss_floor_y, 4, constants.FLOOR_SPRITE))
        right_start_x = constants.SCREEN_WIDTH - (4 * sprite_w)
        self.platforms.append(Platform(right_start_x, boss_floor_y, 4, constants.FLOOR_SPRITE))

        # Ground Floor
        ground_rows = (6 + sprite_h - 1) // sprite_h
        sprites_per_row = (constants.SCREEN_WIDTH // sprite_w) + 1
        for each in range(ground_rows):
            y = ground_start_y + (each * sprite_h)
            self.platforms.append(Platform(0, y, sprites_per_row, constants.FLOOR_SPRITE))

    def create_actors(self):
        self.mario = Character("Mario", constants.MARIO_X + 2)
        self.luigi = Character("Luigi", constants.LUIGI_X + 3)
        
        self.mario.max_floor_index = self.floor_max_index
        self.luigi.max_floor_index = self.floor_max_index
        
        self.boss = Boss()
        
        door_h = 16 
        door_y = constants.BOSS_Y - door_h
        self.door_left = Door(constants.BOSS_LUIGI, door_y)
        self.door_right = Door(constants.BOSS_MARIO, door_y)

    # --- PROPERTIES ---
    @property
    def conveyors(self) -> list: return self.__conveyors
    @conveyors.setter
    def conveyors(self, value: list):
        if not isinstance(value, list): raise TypeError("Conveyors must be a list")
        for item in value:
            if not isinstance(item, Conveyor): raise TypeError("All items in conveyors must be of type Conveyor")
        self.__conveyors = value
    
    @property
    def truck(self) -> Truck: return self.__truck
    @truck.setter
    def truck(self, value: Truck):
        if not isinstance(value, Truck): raise TypeError("Truck must be an instance of Truck class")
        self.__truck = value
    
    @property
    def platforms(self) -> list: return self.__platforms
    @platforms.setter
    def platforms(self, value: list):
        if not isinstance(value, list): raise TypeError("Platforms must be a list")
        for item in value:
            if not isinstance(item, Platform): raise TypeError("All items in platforms must be of type Platform")
        self.__platforms = value

    # --- GAME UPDATE LOGIC ---
    def spawn_package(self):
        if len(self.packages) == 0: self.spawn_timer = 999
        self.spawn_timer += 1
        if self.spawn_timer > 180:
            new_pck = Package(self.difficulty, self.conveyors[0], 0)
            self.packages.append(new_pck)
            self.spawn_timer = 0

    def update_packages(self):
        for p in self.packages[:]:
            p.update()

            if p.y > constants.SCREEN_HEIGHT:
                self.packages.remove(p)
                self.failures += 1
                culprit = "Mario" if p.x > constants.CENTER_SCREEN else "Luigi"
                self.trigger_failure(culprit)
                continue

            if p.status == Package.STATE_MOVING:
                conv = p.current_conveyor
                reached_end = False

                if conv.direction == 1 and p.x >= conv.end_x:
                    p.x = conv.end_x 
                    reached_end = True
                elif conv.direction == -1 and p.x <= conv.x:
                    p.x = conv.x 
                    reached_end = True

                if reached_end:
                    character_present = False
                    if self.mario.floor == p.floor_index: character_present = True
                    if self.luigi.floor == p.floor_index: character_present = True

                    if character_present:
                        next_idx = p.floor_index + 1
                        
                        if next_idx < len(self.conveyors):
                            p.advance_to_conveyor(self.conveyors[next_idx])
                            self.score += 1 
                        else:
                            self.truck.receive_package()
                            self.score += 1 
                            if self.truck.packages_count == 8:
                                self.score += 10 
                            self.packages.remove(p)
                    else:
                        p.status = Package.STATE_FALLING

    def trigger_failure(self, character_name: str):
        self.is_punishing = True
        if character_name == "Mario":
            self.active_door = self.door_right
            self.punished_char = self.mario
        else:
            self.active_door = self.door_left
            self.punished_char = self.luigi
        self.active_door.open()

    def update(self):
        self.door_left.update()
        self.door_right.update()

        if self.is_punishing:
            if self.active_door.state == "open" and not self.boss.active:
                self.boss.appear(self.punished_char.name)
                self.punished_char.enter_punishment_mode()
                self.punishment_timer = 60 
            if self.boss.active:
                self.boss.update()
                self.punishment_timer -= 1
                if self.punishment_timer <= 0:
                    self.is_punishing = False
                    self.boss.disappear()
                    self.active_door.close()
                    self.punished_char.exit_punishment_mode()
                    self.punished_char = None
                    self.active_door = None
        else:
            self.spawn_package()
            self.update_packages() 
            self.mario.update()
            self.luigi.update()
            self.truck.update()

        if pyxel.btnp(pyxel.KEY_Q): pyxel.quit()

    def draw(self):
        for w in self.windows: w.draw()
        self.machine.draw()
        self.exit_signal.draw()
        self.door_left.draw()
        self.door_right.draw()
        self.boss.draw()
        for platform in self.platforms: platform.draw()
        for conv in self.conveyors: conv.draw()
        for p in self.packages: p.draw()
        self.vertical_structure.draw()
        self.level_sign.draw()
        self.mario.draw()
        self.luigi.draw()
        self.truck.draw()
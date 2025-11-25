import pyxel
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
        self.difficulty = difficulty
        self.truck = Truck(constants.TRUCK_X, 0) # Y reset in game_start
        
        self.machine = Machine(constants.MACHINE_X, constants.MACHINE_Y)
        self.windows = [Window(20, 15), Window(215, 35), Window(215, 45)]
        self.boss = Boss()
        
        # Ideally Door would have a height property, assuming 16 based on sprite constant
        door_h = 16
        door_y = constants.BOSS_Y - door_h
        self.door_left = Door(constants.BOSS_LUIGI, door_y)
        self.door_right = Door(constants.BOSS_MARIO, door_y)

        self.is_punishing = False
        self.punishment_timer = 0
        self.punished_char = None
        self.active_door = None
        self.score = 0
        self.failures = 0

        self.game_start()

    @property
    def conveyors(self) -> list: return self.__conveyors
    @conveyors.setter
    def conveyors(self, value: list): self.__conveyors = value
    @property
    def truck(self) -> Truck: return self.__truck
    @truck.setter
    def truck(self, value: Truck): self.__truck = value
    @property
    def platforms(self) -> list: return self.__platforms
    @platforms.setter
    def platforms(self, value: list): self.__platforms = value

    def game_start(self):
        self.conveyors = []
        self.platforms = []
        self.packages = []
        
        self.mario = Character("Mario", constants.MARIO_X + 2)
        self.luigi = Character("Luigi", constants.LUIGI_X + 3)
        self.level_sign = LevelSign(self.difficulty, 4, constants.SCREEN_HEIGHT - 18)
        self.spawn_timer = 0

        floor_y_positions = []
        if self.difficulty == "EASY" or self.difficulty == "CRAZY": floor_y_positions = constants.FLOORS_EASY_CRAZY
        elif self.difficulty == "MEDIUM": floor_y_positions = constants.FLOORS_MEDIUM
        elif self.difficulty == "EXTREME": floor_y_positions = constants.FLOORS_EXTREME
        else: floor_y_positions = constants.FLOORS_EASY_CRAZY

        # --- Magic Number Fix: Truck Y ---
        top_floor_y = floor_y_positions[-1]
        # Position truck so its bottom aligns with the platform
        # Using truck.height property
        self.truck.y = top_floor_y - 5 
        self.truck.reset()

        ground_height_px = 6
        ground_start_y = constants.SCREEN_HEIGHT - ground_height_px
        self.exit_signal = ExitSignal(2, self.truck.y - 10)
        self.vertical_structure = VerticalStructure(constants.STRUCT_X, 2, top_floor_y, ground_start_y)

        # Conveyor 0 (Machine)
        self.conveyors.append(Conveyor(constants.CONVEYOR_0_X, floor_y_positions[0], 1, constants.SLOW_SPEED, -1))
        
        # Main Conveyors
        for index, y_pos in enumerate(floor_y_positions):
            if index % 2 == 0: direction = -1
            else: direction = 1
            
            plat_x = constants.MARIO_X if index % 2 != 0 else constants.LUIGI_X
            self.platforms.append(Platform(plat_x, y_pos + 2, 1))

            self.conveyors.append(Conveyor(constants.CONVEYOR_X_START, y_pos, constants.CONVEYOR_SEGMENTS, constants.SLOW_SPEED, direction))

        # Platforms
        sprite_h = constants.FLOOR_SPRITE[4]
        sprite_w = constants.FLOOR_SPRITE[3]
        
        # Truck Platform - dynamic Y based on truck height
        truck_floor_y = self.truck.y + self.truck.height 
        for height in range(2):
            y = truck_floor_y + (height * sprite_h)
            self.platforms.append(Platform(0, y, 5, constants.FLOOR_SPRITE))

        boss_floor_y = constants.BOSS_Y
        self.platforms.append(Platform(0, boss_floor_y, 4, constants.FLOOR_SPRITE))
        right_start_x = constants.SCREEN_WIDTH - (4 * sprite_w)
        self.platforms.append(Platform(right_start_x, boss_floor_y, 4, constants.FLOOR_SPRITE))

        ground_rows = (ground_height_px + sprite_h - 1) // sprite_h
        sprites_per_row = (constants.SCREEN_WIDTH // sprite_w) + 1
        for each in range(ground_rows):
            y = ground_start_y + (each * sprite_h)
            self.platforms.append(Platform(0, y, sprites_per_row, constants.FLOOR_SPRITE))

    def spawn_package(self):
        if len(self.packages) == 0: self.spawn_timer = 999
        self.spawn_timer += 1
        if self.spawn_timer > 180:
            new_pck = Package(self.difficulty, self.conveyors[0], 0)
            self.packages.append(new_pck)
            self.spawn_timer = 0

    def update_packages(self):
        for p in self.packages[:]:
            # --- NEW UPDATE CALL ---
            p.update(self.mario, self.luigi, self.conveyors, self.truck)
            
            # --- HANDLE STATUS ---
            if p.status == "delivered":
                self.packages.remove(p)
                self.score += 1
            elif p.status == "lost":
                self.packages.remove(p)
                self.failures += 1
                # Trigger failure logic (defaulting to Mario for simplicity or add logic to find who missed it)
                self.trigger_failure("Mario") 

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
        if pyxel.btnp(pyxel.KEY_B): self.trigger_failure("Mario")
        if pyxel.btnp(pyxel.KEY_N): self.trigger_failure("Luigi")

        self.door_left.update()
        self.door_right.update()

        if self.is_punishing:
            if self.active_door.state == "open" and not self.boss.active:
                self.boss.appear(self.punished_char.name)
                self.punished_char.enter_punishment_mode()
                self.punishment_timer = 150 
            if self.boss.active:
                self.boss.update()
                self.punishment_timer -= 1
                if self.punishment_timer <= 0:
                    self.is_punishing = False
                    self.boss.disappear()
                    self.active_door.close()
                    self.punished_char.exit_punishment_mode(self.conveyors)
                    self.punished_char = None
                    self.active_door = None
        else:
            self.spawn_package()
            self.update_packages()
            self.mario.update(self.conveyors)
            self.luigi.update(self.conveyors)
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
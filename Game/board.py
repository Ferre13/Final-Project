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
        self.truck = Truck(constants.TRUCK_X, 0)
        
        # These are static elements, they dont change when the game restarts
        self.machine = Machine(constants.MACHINE_X, constants.MACHINE_Y)
        self.windows = [Window(20, 15), Window(215, 35), Window(215, 45)]
        self.boss = Boss()
        
        door_y = (constants.BOSS_Y) - 16
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
        self.packages = []
        self.route_segments = []

        self.mario = Character("Mario", constants.MARIO_X + 2)
        self.luigi = Character("Luigi", constants.LUIGI_X + 3)

        # Create Level Sign
        self.level_sign = LevelSign(self.difficulty, 4, constants.SCREEN_HEIGHT - 18)

        self.spawn_timer = 0

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
        self.truck.y = top_floor_y - 5
        self.truck.reset()

        # Ground calculations
        ground_height_px = 6
        ground_start_y = constants.SCREEN_HEIGHT - ground_height_px

        # Create Exit Signal
        self.exit_signal = ExitSignal(2, self.truck.y - 10)
        # Vertical Structure
        self.vertical_structure = VerticalStructure(constants.STRUCT_X, 2, top_floor_y, ground_start_y)

        self.route_segments.append({
            'type': 'interact', # Mario must pick it up here (Horizontal)
            'start_x': constants.CONVEYOR_0_X + 20,
            'start_y': self.floors[0],
            'end_x': constants.CONVEYOR_0_X, # End of machine belt
            'direction': -1,
            'floor_index': 0, # Handled by Mario
            'handler': "Mario"
        })

        # Create Conveyors and Platforms
        # Enumerate returns index and value (0, FLOOR_Y_POSITIONS[0])
        for index, y_pos in enumerate(self.floors):
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
            self.conveyors.append(
                Conveyor(constants.CONVEYOR_X_START, y_pos, constants.CONVEYOR_SEGMENTS, speed, direction)
            )
            # Machine Connection
            if index == 0:
                self.conveyors.append(Conveyor(constants.CONVEYOR_0_X, y_pos, 1, speed, direction))

            if direction == -1: # Left (Luigi receives)
                start_x = constants.CONVEYOR_X_START + constants.CONVEYOR_TOTAL_WIDTH_PX
                end_x = constants.CONVEYOR_X_START
                handler_name = "Luigi"
            else: # Right (Mario receives)
                start_x = constants.CONVEYOR_X_START
                end_x = constants.CONVEYOR_X_START + constants.CONVEYOR_TOTAL_WIDTH_PX
                handler_name = "Mario"
            
            self.route_segments.append({
                'type': 'interact',
                'start_x': start_x,
                'start_y': y_pos,
                'end_x': end_x,
                'direction': direction,
                'floor_index': index, # Matches character floor index
                'handler': handler_name
            })
        
        # Ground Calculations
        sprite_h = constants.FLOOR_SPRITE[4]
        sprite_w = constants.FLOOR_SPRITE[3]

        # Truck Platform
        # Floor is 16px lower than the truck, accordint to truck height
        truck_floor_y = self.truck.y + 16
        truck_floor_height = 2
        truck_floor_width = 5
        
        for height in range(truck_floor_height):
            y = truck_floor_y + (height * sprite_h)
            floor = Platform(0, y, truck_floor_width, constants.FLOOR_SPRITE)
            self.platforms.append(floor)

        # Boss Platforms
        # Floor is 2px below the boss y position
        boss_floor_y = constants.BOSS_Y
        boss_floor_width = 4
        
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

    def spawn_package(self):
        if len(self.packages) == 0: 
            self.spawn_timer = 999
        self.spawn_timer += 1
        if self.spawn_timer > 180:
            new_pck = Package(self.difficulty, self.route_segments)
            self.packages.append(new_pck)
            self.spawn_timer = 0

    def update_packages(self):
        for p in self.packages[:]: 
            p.update()
            
            # AUTO-ADVANCE (Tracing Route)
            # No Boss logic here, just movement.
            if p.status == p.STATE_WAITING:
                p.advance()

            # TRUCK DELIVERY
            if p.current_segment_index >= len(self.route_segments):
                self.truck.add_package()
                self.packages.remove(p)

    def trigger_failure(self, character_name: str):
        """ Begins the Boss Punishment Sequence """
        self.is_punishing = True
                
        # 1. Determine which door and character are involved
        if character_name == "Mario":
            self.active_door = self.door_right
            self.punished_char = self.mario
        else:
            self.active_door = self.door_left
            self.punished_char = self.luigi
            
        # 2. Start opening the door
        self.active_door.open()

    def update(self):
        # Test Keys
        if pyxel.btnp(pyxel.KEY_B): self.trigger_failure("Mario")
        if pyxel.btnp(pyxel.KEY_N): self.trigger_failure("Luigi")

        self.door_left.update()
        self.door_right.update()

        if self.is_punishing:
            # Check if the door is fully open and Boss hasn't appeared yet
            if self.active_door.state == "open" and not self.boss.active:
                # Step 2: Door is open, Boss appears, Character moves
                self.boss.appear(self.punished_char.name)
                self.punished_char.enter_punishment_mode()
                self.punishment_timer = 150 # Start countdown now

            # If Boss is active, run the punishment timer
            if self.boss.active:
                self.boss.update()
                self.punishment_timer -= 1
                
                # Step 3: End Punishment
                if self.punishment_timer <= 0:
                    self.is_punishing = False
                    self.boss.disappear()
                    self.active_door.close()
                    self.punished_char.exit_punishment_mode(self.floors)
                    self.punished_char = None
                    self.active_door = None
        else:
            # Normal Game Loop
            self.spawn_package()
            self.update_packages()
            self.mario.update(self.floors)
            self.luigi.update(self.floors)
            self.truck.update()

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    # Draw all elements
    def draw(self):

        for w in self.windows:
            w.draw()
        self.machine.draw()
        self.exit_signal.draw()
        self.door_left.draw()
        self.door_right.draw()
        self.boss.draw()

        for platform in self.platforms:
            platform.draw()
        for conv in self.conveyors:
            conv.draw()

        for p in self.packages:
            p.draw()
        self.vertical_structure.draw()
        self.level_sign.draw()

        self.mario.draw()
        self.luigi.draw()
        self.truck.draw()
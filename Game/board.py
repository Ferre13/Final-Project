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
from hud import HUD

class Board:
    def __init__(self, difficulty: str):
        self.init_configuration(difficulty)
        self.create_background()
        self.create_world()
        self.create_characters()

    def init_configuration(self, difficulty: str):
        self.difficulty = difficulty
        self.score = 0
        self.failures = 0
        self.spawn_timer = 0
        self.packages = []
        self.punished_char = None
        self.deliveries_count = 0 
        self.hud = HUD()

    def create_background(self):
        self.windows = [Window(20, 15), Window(215, 35), Window(215, 45)]
        self.machine = Machine(constants.MACHINE_X, constants.MACHINE_Y)
        self.level_sign = LevelSign(self.difficulty, 4, constants.SCREEN_HEIGHT - 18)

    def create_world(self):
        if self.difficulty in ["EASY", "CRAZY"]: 
            floor_y_positions = constants.FLOORS_EASY_CRAZY
        elif self.difficulty == "MEDIUM": 
            floor_y_positions = constants.FLOORS_MEDIUM
        elif self.difficulty == "EXTREME": 
            floor_y_positions = constants.FLOORS_EXTREME
        else:
            floor_y_positions = constants.FLOORS_EASY_CRAZY

        top_floor_y = floor_y_positions[-1]
        self.truck = Truck(constants.TRUCK_X, top_floor_y - 5)
        self.truck.reset()

        ground_y = constants.SCREEN_HEIGHT - 6
        self.exit_signal = ExitSignal(2, self.truck.y - 10)
        self.vertical_structure = VerticalStructure(constants.STRUCT_X, 2, top_floor_y, ground_y)

        self.conveyors = []
        self.platforms = []

        self.conveyors.append(Conveyor(
            constants.CONVEYOR_0_X, floor_y_positions[0], 1, -1, self.difficulty, 0
        ))
        
        for i, y_pos in enumerate(floor_y_positions):
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

        self.create_extra_platforms(ground_y)

    def create_extra_platforms(self, ground_start_y: int):
        sprite_h = constants.FLOOR_SPRITE[4]
        truck_floor_y = self.truck.y + self.truck.height 
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
        self.mario = Character("Mario", constants.MARIO_X + 2, self.difficulty)
        self.luigi = Character("Luigi", constants.LUIGI_X + 3, self.difficulty)
        
        door_y = constants.BOSS_Y - constants.DOOR_OPEN[4]
        self.door_left = Door(constants.BOSS_LUIGI, door_y)
        self.door_right = Door(constants.BOSS_MARIO, door_y)
        self.boss = Boss(self.door_left, self.door_right)

    def reset_game(self):
        """ Resets all game state to initial values. """
        self.score = 0
        self.failures = 0
        self.spawn_timer = 0
        self.packages = []
        self.deliveries_count = 0
        self.punished_char = None
        
        self.truck.reset()
        # Re-create characters to reset positions
        self.create_characters()

    def calculate_max_packages(self) -> int:
        limit = constants.INITIAL_PACKAGE_LIMIT
        
        if self.difficulty == "EASY":
            limit += (self.score // constants.SPAWN_SCORE_THRESHOLD_EASY)
        elif self.difficulty == "MEDIUM":
            limit += (self.score // constants.SPAWN_SCORE_THRESHOLD_MEDIUM)
        elif self.difficulty == "EXTREME":
            limit += (self.score // constants.SPAWN_SCORE_THRESHOLD_EXTREME)
        elif self.difficulty == "CRAZY":
            limit += (self.score // constants.SPAWN_SCORE_THRESHOLD_CRAZY)
            
        return limit

    def spawn_package(self):
        self.spawn_timer += 1
        max_packages = self.calculate_max_packages()
        
        if len(self.packages) < max_packages:
            if not self.packages or self.spawn_timer > constants.SPAWN_TIMER_GAP:
                new_pck = Package(self.difficulty, self.conveyors[0], 0)
                self.packages.append(new_pck)
                self.spawn_timer = 0

    def handle_truck_bonus(self):
        self.deliveries_count += 1
        bonus_awarded = False

        if self.difficulty == "EASY":
            if self.deliveries_count % constants.BONUS_REQUIRED_EASY == 0:
                bonus_awarded = True
        elif self.difficulty == "MEDIUM":
            if self.deliveries_count % constants.BONUS_REQUIRED_MEDIUM == 0:
                bonus_awarded = True
        elif self.difficulty == "EXTREME":
            if self.deliveries_count % constants.BONUS_REQUIRED_EXTREME == 0:
                bonus_awarded = True

        if bonus_awarded and self.failures > 0:
            self.failures -= 1

    def active_punishment(self, character_name: str):
        if character_name == "Mario":
            self.punished_char = self.mario
            self.boss.appear("MARIO_FAIL")
        else:
            self.punished_char = self.luigi
            self.boss.appear("LUIGI_FAIL")
        
        self.punished_char.enter_punishment_mode()

    def update_packages(self):
        for p in self.packages[:]:
            status = p.update() 

            if status == constants.PKG_STATUS_FALLEN_MARIO:
                self.handle_failure(p, "Mario")
            elif status == constants.PKG_STATUS_FALLEN_LUIGI:
                self.handle_failure(p, "Luigi")
            elif status == constants.PKG_STATUS_REACHED_END:
                self.handle_package_transfer(p)

    def handle_failure(self, p: Package, culprit: str):
        self.packages.remove(p)
        self.failures += 1
        
        if self.failures < constants.MAX_FAILURES:
            self.active_punishment(culprit)

    def handle_package_transfer(self, p: Package):
        if self.mario.can_receive_package(p.floor_index) or \
           self.luigi.can_receive_package(p.floor_index):
            
            next_idx = p.floor_index + 1
            
            if next_idx < len(self.conveyors):
                p.advance_to_conveyor(self.conveyors[next_idx])
                self.score += constants.POINTS_PER_PACKAGE 
            else:
                self.truck.receive_package()
                self.packages.remove(p)
                self.score += constants.POINTS_PER_PACKAGE
        else:
            p.fall()

    def update(self):
        # 1. Game Over Check
        if self.failures >= constants.MAX_FAILURES:
            # Restart Logic
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_ENTER):
                self.reset_game()
            return

        self.door_left.update()
        self.door_right.update()

        if self.truck.is_delivering:
            self.truck.update()
            if self.mario.state != constants.CHAR_STATE_REST1 and self.mario.state != constants.CHAR_STATE_REST2:
                self.mario.enter_rest_mode()
                self.luigi.enter_rest_mode()
            self.mario.update()
            self.luigi.update()

            if not self.truck.is_delivering:
                self.score += constants.POINTS_PER_TRUCK
                self.handle_truck_bonus()
                self.boss.appear("BREAK")
            return

        if self.boss.is_active:
            self.boss.update()
            if not self.boss.is_active:
                if self.punished_char:
                    self.punished_char.exit_punishment_mode()
                    self.punished_char = None
                self.mario.exit_rest_mode()
                self.luigi.exit_rest_mode()
            return

        self.spawn_package()
        self.update_packages()
        self.mario.update()
        self.luigi.update()

        if pyxel.btnp(pyxel.KEY_Q): pyxel.quit()

    def draw(self):
        # Game Over Screen
        if self.failures >= constants.MAX_FAILURES:
            pyxel.text(constants.CENTER_SCREEN - 30, constants.CENTER_SCREEN - 10, "GAME OVER", 8)
            pyxel.text(constants.CENTER_SCREEN - 40, constants.CENTER_SCREEN + 5, "PRESS SPACE TO RESTART", 7)
            
            # Show final score
            self.hud.draw_score(self.score)
            return

        for w in self.windows: w.draw()
        self.machine.draw()
        self.exit_signal.draw()
        self.door_left.draw()
        self.door_right.draw()
        self.boss.draw()
        for p in self.packages: p.draw()
        for platform in self.platforms: platform.draw()
        for conv in self.conveyors: conv.draw()
        self.vertical_structure.draw()
        self.level_sign.draw()
        self.mario.draw()
        self.luigi.draw()
        self.truck.draw()

        self.hud.draw_score(self.score)
        self.hud.draw_lives(self.failures)
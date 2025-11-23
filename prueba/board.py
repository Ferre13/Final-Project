import pyxel
from constants import (
    GAME_PLAYING, GAME_PAUSE, GAME_OVER, GAME_TRUCK,
    NUM_CONVEYORS_EASY, NUM_CONVEYORS_MEDIUM, NUM_CONVEYORS_EXTREME, NUM_CONVEYORS_CRAZY,
    FLOOR_Y_POSITIONS, SLOW_SPEED, MEDIUM_SPEED, FAST_SPEED, RANDOM_SPEED, CONVEYOR_LENGTH,
    CONVEYOR_X_RIGHT, CONVEYOR_X_LEFT,
    MARIO_X, LUIGI_X,
    BOSS_LUIGI, BOSS_Y, TRUCK_X, TRUCK_Y,
    BOSS_SCENE, MAX_FAILURES,
    POINTS_PER_PACKAGE, PLATFORM_SPRITE, EXIT_SIGNAL_SPRITE
)
from character import Mario, Luigi
from conveyor import Conveyor
from truck import Truck
from boss import Boss
from package import Package
from game_platform import Platform
from exit_signal import ExitSignal
from score import Score
from vertical_structure import VerticalStructure
from machine import Machine
from window import Window
from typing import List
import random

class Board:
    """
    The main game board, responsible for managing all game elements and logic.
    """

    def __init__(self, width: int, height: int, difficulty: str = "easy"):
        """
        Initializes the game board.
        :param width: The width of the game screen.
        :param height: The height of the game screen.
        :param difficulty: The chosen difficulty level.
        """
        self.width = width
        self.height = height
        self.difficulty = difficulty
        
        self.score = 0
        self.failures = 0
        self.game_state = GAME_PLAYING

        # Create game elements
        self.mario = Mario()
        self.luigi = Luigi()
        self.boss = Boss(x=BOSS_LUIGI, y=BOSS_Y)
        self.truck = Truck(x=TRUCK_X, y=TRUCK_Y)
        self.exit_signal = ExitSignal(x=TRUCK_X + 48, y=TRUCK_Y)
        self.score_display = Score(x=5, y=5)
        self.vertical_structure = VerticalStructure(x=self.width/2 - 18, height=self.height // 16, width=3)
        self.machine = Machine(x=CONVEYOR_X_RIGHT, y=FLOOR_Y_POSITIONS[1] - 16)
        self.window = Window(x=self.width/2 - 16, y=32)
        
        if self.difficulty == "easy":
            self.num_conveyors = NUM_CONVEYORS_EASY
            self.conveyor_speed = SLOW_SPEED
        elif self.difficulty == "medium":
            self.num_conveyors = NUM_CONVEYORS_MEDIUM
            self.conveyor_speed = MEDIUM_SPEED
        elif self.difficulty == "extreme":
            self.num_conveyors = NUM_CONVEYORS_EXTREME
            self.conveyor_speed = FAST_SPEED
        elif self.difficulty == "crazy":
            self.num_conveyors = NUM_CONVEYORS_CRAZY
            self.conveyor_speed = RANDOM_SPEED
        
        self.conveyors: List[Conveyor] = self._create_conveyors()
        self.packages: List[Package] = []
        self.platforms: List[Platform] = self._create_platforms()
        
        self.package_spawn_timer = 0

    def _create_platforms(self) -> List[Platform]:
        """
        Creates the platforms for the characters to stand on.
        """
        platforms = []
        for i in range(self.num_conveyors + 1):
            y_position = FLOOR_Y_POSITIONS[i] + 16
            if i % 2 == 0:
                platforms.append(Platform(x=MARIO_X - 8, y=y_position, width=3))
            if i % 2 != 0:
                platforms.append(Platform(x=LUIGI_X - 8, y=y_position, width=3))
        return platforms

    def _create_conveyors(self) -> List[Conveyor]:
        """
        Creates the conveyor belts based on the selected difficulty.
        """
        conveyors = []
        for i in range(self.num_conveyors):
            y_position = FLOOR_Y_POSITIONS[i+1] - 8
            direction = -1 if i % 2 == 0 else 1 # Even conveyors move left, odd move right
            
            speed = self.conveyor_speed
            if self.difficulty == "crazy" and i > 0:
                speed = random.uniform(1, 2)

            conveyors.append(Conveyor(y=y_position, speed=speed, length=CONVEYOR_LENGTH, direction=direction, vertical_structure_x=self.vertical_structure._x, vertical_structure_width=self.vertical_structure._width))
        return conveyors

    def update(self):
        """
        Updates the state of all game elements.
        """
        if pyxel.btnp(pyxel.KEY_P):
            if self.game_state == GAME_PLAYING:
                self.game_state = GAME_PAUSE
            elif self.game_state == GAME_PAUSE:
                self.game_state = GAME_PLAYING

        if self.game_state == GAME_PAUSE:
            return

        if self.game_state == GAME_OVER:
            return
            
        if self.game_state == GAME_TRUCK:
            self.truck.update()
            self.mario.rest()
            self.luigi.rest()
            if not self.truck.is_away:
                self.game_state = GAME_PLAYING
            return

        self.mario.update()
        self.luigi.update()
        self.boss.update()
        self.truck.update()
        
        self._handle_package_spawning()
        self._update_packages()

    def _handle_package_spawning(self):
        """
        Handles the spawning of new packages.
        """
        self.package_spawn_timer -= 1
        if self.package_spawn_timer <= 0:
            self.spawn_package()
            self.package_spawn_timer = random.randint(120, 240)

    def spawn_package(self):
        """
        Spawns a new package on the first conveyor.
        """
        # Conveyor 0 sends packages to Mario on floor 1
        package_y = FLOOR_Y_POSITIONS[1]
        new_package = Package(x=CONVEYOR_X_RIGHT, y=package_y, direction=-1)
        self.packages.append(new_package)

    def _update_packages(self):
        """
        Updates the position of all packages and handles interactions.
        """
        for pkg in self.packages[:]:
            pkg.update()
            
            # Find which conveyor the package is on
            current_conveyor_index = -1
            for i, conveyor in enumerate(self.conveyors):
                if abs(pkg.y - (conveyor.y + 8)) < 5:
                    current_conveyor_index = i
                    break
            
            # Package has fallen off a conveyor
            if pkg.x < CONVEYOR_X_LEFT or pkg.x > CONVEYOR_X_RIGHT:
                self.handle_package_fall(pkg, current_conveyor_index)

    def handle_package_fall(self, pkg: Package, conveyor_index: int):
        """
        Handles the logic when a package falls off a conveyor.
        """
        # Luigi's side (even conveyors)
        if conveyor_index % 2 == 0:
            if self.luigi.floor == conveyor_index + 1:
                if conveyor_index == self.num_conveyors - 1:
                    self.packages.remove(pkg)
                    if self.truck.add_package():
                        self.game_state = GAME_TRUCK
                        self.truck.is_away = True
                    self.score += POINTS_PER_PACKAGE
                else:
                    self.transfer_package(pkg, conveyor_index + 1)
            else:
                self.record_failure(pkg)
        # Mario's side (odd conveyors)
        else:
            if self.mario.floor == conveyor_index + 1:
                # Last conveyor goes to truck
                if conveyor_index == self.num_conveyors - 1:
                    self.packages.remove(pkg)
                    if self.truck.add_package():
                        self.game_state = GAME_TRUCK
                        self.truck.is_away = True
                    self.score += POINTS_PER_PACKAGE
                else:
                    self.transfer_package(pkg, conveyor_index + 1)
            else:
                self.record_failure(pkg)

    def transfer_package(self, pkg: Package, next_conveyor_index: int):
        """
        Transfers a package to the next conveyor.
        """
        next_conveyor = self.conveyors[next_conveyor_index]
        pkg.y = next_conveyor.y + 8
        pkg.direction = next_conveyor.direction
        pkg.x = CONVEYOR_X_LEFT if pkg.direction == 1 else CONVEYOR_X_RIGHT
        self.score += POINTS_PER_PACKAGE

    def record_failure(self, pkg: Package):
        """
        Records a failure and removes the package.
        """
        self.packages.remove(pkg)
        self.failures += 1
        self.boss.appear(BOSS_SCENE)
        if self.failures >= MAX_FAILURES:
            self.game_state = GAME_OVER

    def draw(self):
        """
        Draws all game elements on the screen.
        """
        pyxel.cls(0)  # 7, 13, 15
        
        # Draw window
        self.window.draw()
        
        # Draw vertical structure
        self.vertical_structure.draw()
        
        # Draw machine
        self.machine.draw()
        
        # Draw conveyors
        for conveyor in self.conveyors:
            conveyor.draw()
            
        # Draw platforms
        for platform in self.platforms:
            platform.draw()
            
        # Draw characters
        self.mario.draw()
        self.luigi.draw()
        self.boss.draw()
        self.truck.draw()

        if self.truck.is_full:
            self.exit_signal.is_visible = True
        else:
            self.exit_signal.is_visible = False
        self.exit_signal.draw()

        # Draw packages
        for pkg in self.packages:
            pkg.draw()

        # Draw UI
        self.score_display.draw(self.score)
        failures_text = f"Failures: {self.failures}"
        difficulty_text = f"Difficulty: {self.difficulty.capitalize()}"
        
        pyxel.text(self.width/2 - len(difficulty_text)*2, 5, difficulty_text, 7)
        pyxel.text(self.width - len(failures_text)*4, 5, failures_text, 7)

        if self.game_state == GAME_OVER:
            pyxel.text(self.width // 2 - 30, self.height // 2, "GAME OVER", pyxel.frame_count % 16)
        
        if self.game_state == GAME_PAUSE:
            pyxel.text(self.width // 2 - 20, self.height // 2, "PAUSED", 7)
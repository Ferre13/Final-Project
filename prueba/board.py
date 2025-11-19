import pyxel
from constants import *
from character import Mario, Luigi
from conveyor import Conveyor
from truck import Truck
from boss import Boss
from package import Package
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
        
        self.score = 0
        self.failures = 0
        self.game_state = STATE_PLAYING

        # Create game elements
        self.mario = Mario()
        self.luigi = Luigi()
        self.boss = Boss(x=BOSS_X, y=BOSS_Y)
        self.truck = Truck(x=TRUCK_X, y=TRUCK_Y)
        
        self.conveyors: List[Conveyor] = self._create_conveyors()
        self.packages: List[Package] = []
        
        self.package_spawn_timer = 0

    def _create_conveyors(self) -> List[Conveyor]:
        """
        Creates the conveyor belts.
        """
        conveyors = []
        for i in range(NUM_CONVEYORS):
            y_position = FLOOR_Y_POSITIONS[i+1] - 8
            direction = -1 if i % 2 == 0 else 1 # Even conveyors move left, odd move right
            conveyors.append(Conveyor(y=y_position, speed=PACKAGE_SPEED, length=CONVEYOR_LENGTH, direction=direction))
        return conveyors

    def update(self):
        """
        Updates the state of all game elements.
        """
        if self.game_state == STATE_GAME_OVER:
            return
            
        if self.game_state == STATE_TRUCK_AWAY:
            self.truck.update()
            if not self.truck.is_away:
                self.game_state = STATE_PLAYING
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
        new_package = Package(x=CONVEYOR_X_START_RIGHT, y=package_y, direction=-1)
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
            if pkg.x < CONVEYOR_X_END_LEFT or pkg.x > CONVEYOR_X_START_RIGHT:
                self.handle_package_fall(pkg, current_conveyor_index)

    def handle_package_fall(self, pkg: Package, conveyor_index: int):
        """
        Handles the logic when a package falls off a conveyor.
        """
        # Mario's side (even conveyors)
        if conveyor_index % 2 == 0:
            if self.mario.floor == conveyor_index + 1:
                self.transfer_package(pkg, conveyor_index + 1)
            else:
                self.record_failure(pkg)
        # Luigi's side (odd conveyors)
        else:
            if self.luigi.floor == conveyor_index + 1:
                # Last conveyor goes to truck
                if conveyor_index == NUM_CONVEYORS - 1:
                    self.packages.remove(pkg)
                    if self.truck.add_package():
                        self.game_state = STATE_TRUCK_AWAY
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
        pkg.x = CONVEYOR_X_END_LEFT if pkg.direction == 1 else CONVEYOR_X_START_RIGHT
        self.score += POINTS_PER_PACKAGE

    def record_failure(self, pkg: Package):
        """
        Records a failure and removes the package.
        """
        self.packages.remove(pkg)
        self.failures += 1
        self.boss.appear(BOSS_APPEAR_DURATION)
        if self.failures >= MAX_FAILURES:
            self.game_state = STATE_GAME_OVER

    def draw(self):
        """
        Draws all game elements on the screen.
        """
        pyxel.cls(0)
        
        # Draw conveyors
        for conveyor in self.conveyors:
            conveyor.draw()
            
        # Draw characters
        self.mario.draw()
        self.luigi.draw()
        self.boss.draw()
        self.truck.draw()

        # Draw packages
        for pkg in self.packages:
            pkg.draw()

        # Draw UI
        pyxel.text(5, 5, f"Score: {self.score}", 7)
        pyxel.text(self.width - 60, 5, f"Failures: {self.failures}", 7)

        if self.game_state == STATE_GAME_OVER:
            pyxel.text(self.width // 2 - 30, self.height // 2, "GAME OVER", pyxel.frame_count % 16)
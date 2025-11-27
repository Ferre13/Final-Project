import constants
from package import Package
import states

class PackageLogic:
    """
    Manages all logic related to packages, including spawning, updating,
    and handling transfers and failures. This class isolates package-specific
    logic from the main board.
    """
    def __init__(self, board):
        """
        Initializes the package logic handler.
        
        :param board: A reference to the main board object to access and modify
                      shared game state like score, failures, and lists of objects.
        """
        self.board = board
        self.spawn_timer = 0

    def update(self):
        """The main update method for all package-related logic."""
        self._spawn_package()
        self._update_packages()

    def _calculate_max_packages(self) -> int:
        """Calculates the maximum number of packages allowed on screen based on score."""
        limit = constants.INITIAL_PACKAGE_LIMIT
        difficulty = self.board.difficulty
        score = self.board.score

        if difficulty == "EASY":
            limit += (score // constants.SPAWN_SCORE_THRESHOLD_EASY)
        elif difficulty == "MEDIUM":
            limit += (score // constants.SPAWN_SCORE_THRESHOLD_MEDIUM)
        elif difficulty == "EXTREME":
            limit += (score // constants.SPAWN_SCORE_THRESHOLD_EXTREME)
        elif difficulty == "CRAZY":
            limit += (score // constants.SPAWN_SCORE_THRESHOLD_CRAZY)
            
        return limit

    def _spawn_package(self):
        """Handles the logic for spawning new packages onto the first conveyor."""
        self.spawn_timer += 1
        max_packages = self._calculate_max_packages()
        
        if self.board.conveyors and len(self.board.packages) < max_packages:
            if not self.board.packages or self.spawn_timer > constants.SPAWN_TIMER_GAP:
                new_pck = Package(self.board.difficulty, self.board.conveyors[0], 0)
                self.board.packages.append(new_pck)
                self.spawn_timer = 0

    def _update_packages(self):
        """Updates all packages and handles their status changes."""
        for p in self.board.packages[:]:
            status = p.update() 

            if status == constants.PKG_STATUS_FALLEN_MARIO:
                self._handle_failure(p, "Mario")
            elif status == constants.PKG_STATUS_FALLEN_LUIGI:
                self._handle_failure(p, "Luigi")
            elif status == constants.PKG_STATUS_REACHED_END:
                self._handle_package_transfer(p)

    def _handle_failure(self, p: Package, culprit: str):
        """Handles the consequences of a package falling."""
        self.board.packages.remove(p)
        self.board.failures += 1
        
        if self.board.failures >= constants.MAX_FAILURES:
            self.board.state = states.GAME_OVER
        else:
            self.board.active_punishment(culprit)

    def _handle_package_transfer(self, p: Package):
        """Handles the logic for transferring a package between conveyors or to the truck."""
        mario = self.board.mario
        luigi = self.board.luigi
        
        if mario.can_receive_package(p.floor_index) or luigi.can_receive_package(p.floor_index):
            next_idx = p.floor_index + 1
            
            if next_idx < len(self.board.conveyors):
                p.advance_to_conveyor(self.board.conveyors[next_idx])
                self.board.score += constants.POINTS_PER_PACKAGE 
            else:
                # Package reaches the final conveyor and is delivered to the truck
                if self.board.truck.receive_package():
                    self.board.state = states.TRUCK_SEQUENCE
                self.board.packages.remove(p)
                self.board.score += constants.POINTS_PER_PACKAGE
        else:
            # If no character is in position, the package falls
            p.fall()

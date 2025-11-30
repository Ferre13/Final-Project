import constants
from package import Package

class PackageManager:
    """
    Manages all logic related to packages, including spawning, updating,
    and handling transfers and failures. This class encapsulates package-specific
    logic and acts as a manager for the main board.
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
        self.__spawn_package()
        self.__update_packages()

    def __calculate_max_packages(self) -> int:
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

    def __spawn_package(self):
        """Handles the logic for spawning new packages onto the first conveyor."""
        self.spawn_timer += 1
        max_packages = self.__calculate_max_packages()
        
        if self.board.conveyors and len(self.board.packages) < max_packages:
            if not self.board.packages or self.spawn_timer > constants.SPAWN_TIMER_GAP:
                new_pck = Package(self.board.difficulty, self.board.conveyors[0], 0)
                self.board.packages.append(new_pck)
                self.spawn_timer = 0

    def __update_packages(self):
        """
        Updates all packages, checks their status, and tells the characters
        when to start their transfer animations.
        """
        for p in self.board.packages[:]:
            # First, check for animation triggers
            char_to_animate = None
            if self.board.mario.can_receive_package(p.floor_index):
                char_to_animate = self.board.mario
            elif self.board.luigi.can_receive_package(p.floor_index):
                char_to_animate = self.board.luigi
            
            if char_to_animate:
                distance_to_end = 0
                direction = p.current_conveyor.direction
                speed = p.current_conveyor.speed
                if direction == 1:
                    distance_to_end = p.current_conveyor.end_x - (p.x + p.width)
                else:
                    distance_to_end = p.x - p.current_conveyor.x
                
                if speed > 0 and (distance_to_end / speed) <= constants.TRANSFER_ANIMATION_TIME:
                    char_to_animate.start_transfer_animation()

            # Now, update the package and handle its status
            status = p.update()
            
            if status == constants.PKG_STATUS_REACHED_END:
                self.__handle_package_transfer(p)
            elif status == constants.PKG_STATUS_FALLEN_MARIO:
                self.__handle_failure(p, "Mario")
            elif status == constants.PKG_STATUS_FALLEN_LUIGI:
                self.__handle_failure(p, "Luigi")

    def __handle_failure(self, p: Package, culprit: str):
        """Handles the consequences of a package falling."""
        self.board.packages.remove(p)
        self.board.failures += 1
        
        if self.board.failures >= constants.MAX_FAILURES:
            self.board.state = constants.GAME_OVER
        else:
            self.board.active_punishment(culprit)

    def __handle_package_transfer(self, p: Package):
        """
        Handles the logic for transferring a package between conveyors or to the truck.
        """
        mario = self.board.mario
        luigi = self.board.luigi
        
        # This check is now simplified because the animation state is handled
        # by the character itself. We just check if they are on the right floor.
        can_transfer = False
        if mario.floor == p.floor_index and (p.floor_index % 2 == 0):
            can_transfer = True
        elif luigi.floor == p.floor_index and (p.floor_index % 2 != 0):
            can_transfer = True

        if can_transfer:
            next_idx = p.floor_index + 1
            
            if next_idx < len(self.board.conveyors):
                p.advance_to_conveyor(self.board.conveyors[next_idx])
                self.board.score += constants.POINTS_PER_PACKAGE 
            else:
                if self.board.truck.receive_package():
                    self.board.state = constants.TRUCK_SEQUENCE
                self.board.packages.remove(p)
                self.board.score += constants.POINTS_PER_PACKAGE
        else:
            # If no character is in position, the package falls
            p.fall()
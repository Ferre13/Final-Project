import constants
from package import Package
import pyxel

class PackageManager:
    """
    Manages all logic related to packages, including spawning, updating,
    and handling transfers and failures.
    """
    def __init__(self, conveyors: list, difficulty: str):
        """
        Initializes the package manager.
        
        :param conveyors: A list of the conveyor belt objects.
        :param difficulty: The game difficulty setting.
        """
        self.conveyors = conveyors
        self.difficulty = difficulty
        self.packages = []
        self.last_spawn_frame = 0

    def update(self, score: int, mario, luigi, truck) -> dict:
        """
        The main update method for all package-related logic.
        
        :param score: The current game score.
        :param mario: The Mario character object.
        :param luigi: The Luigi character object.
        :param truck: The Truck object.
        :return: A dictionary with the results of the update cycle.
        """
        self.__spawn_package(score)
        
        results = {
            "failures": 0,
            "score_change": 0,
            "new_state": None,
            "culprit": None,
            "truck_bonus": False
        }
        
        self.__update_packages(mario, luigi, truck, results)
        
        return results

    def __calculate_max_packages(self, score: int) -> int:
        """Calculates the maximum number of packages allowed on screen based on score."""
        limit = constants.INITIAL_PACKAGE_LIMIT
        
        thresholds = {
            "EASY": constants.SPAWN_SCORE_THRESHOLD_EASY,
            "MEDIUM": constants.SPAWN_SCORE_THRESHOLD_MED_EXTREME,
            "EXTREME": constants.SPAWN_SCORE_THRESHOLD_MED_EXTREME,
            "CRAZY": constants.SPAWN_SCORE_THRESHOLD_CRAZY
        }
        
        threshold = thresholds.get(self.difficulty, 1) # Default to 1 to avoid division by zero
        if threshold > 0:
            limit += (score // threshold)
            
        return limit

    def __spawn_package(self, score: int):
        """Handles the logic for spawning new packages onto the first conveyor."""
        max_packages = self.__calculate_max_packages(score)
        
        can_spawn = len(self.packages) < max_packages
        time_since_last_spawn = pyxel.frame_count - self.last_spawn_frame
        
        if can_spawn and time_since_last_spawn > constants.SPAWN_TIMER_GAP:
            new_pck = Package(self.difficulty, self.conveyors[0], 0)
            self.packages.append(new_pck)
            self.last_spawn_frame = pyxel.frame_count

    def __update_packages(self, mario, luigi, truck, results: dict):
        """
        Updates all packages and checks their status.
        """
        for p in self.packages[:]:
            status = p.update()
            
            if status == constants.PKG_STATUS_REACHED_END:
                self.__handle_package_transfer(p, mario, luigi, truck, results)
            elif status == constants.PKG_STATUS_FALLEN_MARIO:
                self.__handle_failure(p, "Mario", results)
            elif status == constants.PKG_STATUS_FALLEN_LUIGI:
                self.__handle_failure(p, "Luigi", results)

    def __handle_failure(self, p: Package, culprit: str, results: dict):
        """Handles the consequences of a package falling."""
        self.packages.remove(p)
        results["failures"] += 1
        results["culprit"] = culprit

    def __handle_package_transfer(self, p: Package, mario, luigi, truck, results: dict):
        """
        Handles the logic for transferring a package between conveyors or to the truck.
        """
        is_mario_turn = mario.floor == p.floor_index and p.floor_index % 2 == 0
        is_luigi_turn = luigi.floor == p.floor_index and p.floor_index % 2 != 0
        can_transfer = is_mario_turn or is_luigi_turn

        if can_transfer:
            # Tell the character to show the transfer pose for one frame
            if is_mario_turn:
                mario.show_transfer_pose()
            else:
                luigi.show_transfer_pose()

            next_idx = p.floor_index + 1
            
            if next_idx < len(self.conveyors):
                p.advance_to_conveyor(self.conveyors[next_idx])
                results["score_change"] += constants.POINTS_PER_PACKAGE
            else:
                if truck.receive_package():
                    results["new_state"] = constants.TRUCK_SEQUENCE
                    results["truck_bonus"] = True
                self.packages.remove(p)
                results["score_change"] += constants.POINTS_PER_PACKAGE
        else:
            p.fall()
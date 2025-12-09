import pyxel
import constants
from package import Package
from character import Character

class PackageManager:
    """Manages the spawning, movement, and logic for all packages."""
    def __init__(self, conveyors: list, difficulty: str):
        """
        Initializes the package manager.
        :param conveyors: A list of the game's conveyor belt objects.
        :param difficulty: The current game difficulty.
        """
        self.conveyors = conveyors
        self.difficulty = difficulty
        self.packages = []
        self.last_spawn_frame = 0

        # Define thresholds once to avoid recreating the dictionary every frame
        self.spawn_score_thresholds = {"EASY": constants.SPAWN_SCORE_THRESHOLD_EASY, "MEDIUM": constants.SPAWN_SCORE_THRESHOLD_MED_EXTREME,
            "EXTREME": constants.SPAWN_SCORE_THRESHOLD_MED_EXTREME, "CRAZY": constants.SPAWN_SCORE_THRESHOLD_CRAZY}

    def update(self, score: int, mario: Character, luigi: Character, truck, run_game_logic: bool = True) -> dict:
        """
        Updates all package logic for one frame.
        :param score: The current game score.
        :param mario: The Mario character object.
        :param luigi: The Luigi character object.
        :param truck: The Truck object.
        :param run_game_logic: If False, only moves packages without checking for new events.
        :return: A dictionary with the results of the update cycle.
        """
        if run_game_logic:
            self.__update_package_spawning(score)
        results = {"failures": 0, "score_change": 0, "new_state": None, "culprit": None, "truck_bonus": False}
        self.__update_packages(mario, luigi, truck, results, run_game_logic)
        return results

    def update_falling_packages(self):
        """Only updates packages that are currently in the FALLING state."""
        for p in self.packages[:]:
            if p.state == constants.PKG_STATE_FALLING:
                status = p.update()
                if status == constants.PKG_STATUS_DELETE_ME:
                    self.packages.remove(p)

    def __calculate_min_packages(self, score: int) -> int:
        """
        Calculates the min number of packages allowed based on score.
        :param score: The current game score.
        """
        limit = constants.INITIAL_PACKAGE_LIMIT
        threshold = self.spawn_score_thresholds.get(self.difficulty)
        limit += (score // threshold)
            
        return limit

    def __update_package_spawning(self, score: int):
        """
        Handles the logic for spawning new packages.
        :param score: The current game score, used to determine min packages.
        """
        time_since_last_spawn = pyxel.frame_count - self.last_spawn_frame
        
        is_below_minimum = len(self.packages) < self.__calculate_min_packages(score)
        periodic_timer_elapsed = time_since_last_spawn > constants.PERIODIC_SPAWN_TIME
        fill_in_timer_elapsed = time_since_last_spawn > constants.SPAWN_TIMER_GAP
        if fill_in_timer_elapsed:
            if periodic_timer_elapsed or is_below_minimum:
                new_pck = Package(self.difficulty, self.conveyors[0])
                self.packages.append(new_pck)
                self.last_spawn_frame = pyxel.frame_count

    def clear_top_floor_packages(self):
        """Removes all packages from the top conveyor."""
        top_floor_index = len(self.conveyors) - 1
        packages_to_keep = []
        for p in self.packages:
            if p.floor_index != top_floor_index:
                packages_to_keep.append(p)
        self.packages = packages_to_keep

    def __update_packages(self, mario: Character, luigi: Character, truck, results: dict, run_game_logic: bool):
        """
        Updates each package and checks for state changes like transfers or falls.
        :param mario: The Mario object.
        :param luigi: The Luigi object.
        :param truck: The Truck object.
        :param results: The dictionary to populate with update results.
        :param run_game_logic: If False, only moves packages without checking for new events.
        """
        # Iterate over a copy of the list to allow removing items during the loop.
        for p in self.packages[:]:
            # Always update the package's internal physics
            status = p.update()
            # Only check for new game logic events if the flag is true
            if run_game_logic and status == constants.PKG_STATUS_REACHED_END:
                self.__handle_package_transfer(p, mario, luigi, truck, results)
            # Always check if a package has fallen completely off-screen
            elif status == constants.PKG_STATUS_DELETE_ME:
                self.packages.remove(p)

    def __handle_package_transfer(self, p: Package, mario: Character, luigi: Character, truck, results: dict):
        """
        Handles moving a package between conveyors or to the truck.
        :param p: The package to be transferred.
        :param mario: The Mario object.
        :param luigi: The Luigi object.
        :param truck: The Truck object.
        :param results: The dictionary to populate with update results.
        """
        can_mario_receive = mario.can_receive_package(p.floor_index)
        can_luigi_receive = luigi.can_receive_package(p.floor_index)
        can_transfer = can_mario_receive or can_luigi_receive

        if can_transfer:
            if can_mario_receive:
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
            # The package was missed, so register the failure immediately.
            if p.floor_index % 2 == 0:
                culprit = mario
            else:
                culprit = luigi
            results["failures"] += 1
            results["culprit"] = culprit
            # Start the visual falling animation for the package.
            p.fall()

    def draw(self):
        """Draws all packages."""
        for p in self.packages:
            p.draw()
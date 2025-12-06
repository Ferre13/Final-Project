class Soldier:
    """
    Soldier with validated attributes and fight mechanics.
    - attack is one third of life points
    - equality/ordering based on attack
    """

    def __init__(self, name: str, kingdom: str, life_points: float):
        self.name = name
        self.kingdom = kingdom
        self._battles = 0
        self._life_points = self._validate_life(life_points)

    # -----------------------------
    # Properties
    # -----------------------------
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if len(value.strip()) < 1:
            raise ValueError("Name must contain at least 1 character")
        self._name = value

    @property
    def kingdom(self) -> str:
        return self._kingdom

    @kingdom.setter
    def kingdom(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Kingdom must be a string")
        if len(value.strip()) < 1:
            raise ValueError("Kingdom must contain at least 1 character")
        self._kingdom = value

    @property
    def attack(self) -> float:
        return self._life_points / 3

    @property
    def battles(self) -> int:
        return self._battles

    @property
    def alive(self) -> bool:
        return self._life_points > 0

    # -----------------------------
    # Dunder methods
    # -----------------------------
    def __eq__(self, other) -> bool:
        if not isinstance(other, Soldier):
            return False
        return self.attack == other.attack

    def __gt__(self, other) -> bool:
        if not isinstance(other, Soldier):
            raise TypeError("Can only compare with another Soldier")
        return self.attack > other.attack

    def __str__(self) -> str:
        status = "Alive" if self.alive else "Dead"
        return (
            "Soldier information:\n"
            f"Name: {self.name}\n"
            f"Kingdom: {self.kingdom}\n"
            f"Battles: {self.battles}\n"
            f"Status: {status}\n"
            f"Life: {self._life_points:.2f} pts\n"
        )

    # -----------------------------
    # Validators
    # -----------------------------
    def _validate_life(self, value: float) -> float:
        if not isinstance(value, (int, float)):
            raise TypeError("Life points must be a number")
        if value < 0:
            raise ValueError("Life points must be positive")
        return float(value)

    def _validate_battles(self, value: int) -> int:
        if not isinstance(value, int):
            raise TypeError("Battles must be an integer")
        if value < 0:
            raise ValueError("Battles must be a positive integer")
        return value

    # -----------------------------
    # Private helpers
    # -----------------------------
    def _win_battle(self, battle_damage: float):
        self._battles += 1
        # Reduce life by opponent attack, clamp to 0
        self._life_points = max(0.0, self._life_points - self._validate_life(battle_damage))

    def _lose_battle(self):
        self._battles += 1
        self._life_points = 0.0

    # -----------------------------
    # Public API
    # -----------------------------
    def fight(self, other: "Soldier"):
        if not isinstance(other, Soldier):
            raise TypeError("Can only fight another Soldier")
        if not self.alive or not other.alive:
            raise ValueError("Both soldiers must be alive to fight")
        if self.kingdom == other.kingdom:
            raise ValueError("Soldiers must belong to different kingdoms to fight")

        if self == other:
            self._lose_battle()
            other._lose_battle()
        elif self > other:
            self._win_battle(other.attack)
            other._lose_battle()
        else:
            other._win_battle(self.attack)
            self._lose_battle()

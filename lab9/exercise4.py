import random

class Soldier:
    def __init__(self, name: str, kingdom: str, life_points: float):
        self.name = name
        self.kingdom = kingdom
        self.life_points = life_points
        self.battles = 0

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__validate_string(value, "Name")
        self.__name = value

    @property
    def kingdom(self):
        return self.__kingdom

    @kingdom.setter
    def kingdom(self, value):
        self.__validate_string(value, "Kingdom")
        self.__kingdom = value

    @property
    def life_points(self):
        return self.__life_points

    @life_points.setter
    def life_points(self, value):
        self.__life_points = self.__validate_life_points(value)

    @property
    def attack(self):
        return self.life_points / 3

    @property
    def battles(self):
        return self.__battles

    @battles.setter
    def battles(self, value):
        self.__battles = self.__validate_battles(value)
    
    @property                                                                                                                                                         
    def alive(self):                                                                                                                                                  
           return self.__life_points > 0 

    def __validate_life_points(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Life points must be a number.")
        if value < 0:
            raise ValueError("Life points must be positive.")
        return float(value)

    def __validate_battles(self, value):
        if not isinstance(value, int):
            raise TypeError("Battles must be a number.")
        if value < 0:
            raise ValueError("Battles must be positive.")
        return value

    def __validate_string(self, value, attribute_name):
        if not isinstance(value, str):
            raise TypeError(f"{attribute_name} must be a string.")
        if len(value.strip()) == 0:
            raise ValueError(f"{attribute_name} must have at least 1 character.")

    def __eq__(self, other):
        if not isinstance(other, Soldier):
            return NotImplemented
        return self.attack == other.attack

    def __gt__(self, other):
        if not isinstance(other, Soldier):
            return NotImplemented
        return self.attack > other.attack

    def __str__(self):
        if self.alive:
            status = "Alive"
        else:
            status = "Dead"
        return (
            f"\nSoldier information:\n"
            f"Name: {self.name}\n"
            f"Kingdom: {self.kingdom}\n"
            f"Battles: {self.battles}\n"
            f"Status: {status}\n"
            f"Life: {self.life_points:.2f} pts"
        )
    
    def __win_battle(self, battle_damage):
        self.battles += 1
        self.life_points -= battle_damage

    def __lose_battle(self):
        self.battles += 1
        self.life_points = 0

    def fight(self, soldier):
        if not self.alive or not soldier.alive:
            print("\nOne soldier is already dead.")
            return
        if self.kingdom == soldier.kingdom:
            print(f"\nBoth soldiers are from the same kingdom ({self.kingdom}).")
            return

        if self > soldier:
            self.__win_battle(soldier.attack)
            soldier.__lose_battle()
        elif soldier > self:
            soldier.__win_battle(self.attack)
            self.__lose_battle()
        else:
            self.__lose_battle()
            soldier.__lose_battle()

print(f"\nEnter data for Soldier 1")
name1 = input("Name: ")
kingdom1 = input("Kingdom: ")
min_life1 = float(input("Enter minimum life points: "))
max_life1 = float(input("Enter maximum life points: "))
while min_life1 < 0 or max_life1 < min_life1:
    print("Invalid range. Min life must be positive and not greater than max life.")
    min_life1 = float(input("Enter minimum life points: "))
    max_life1 = float(input("Enter maximum life points: "))

life_points1 = random.uniform(min_life1, max_life1)
soldier1 = Soldier(name1, kingdom1, life_points1)

print(f"\nEnter data for Soldier 2")
name2 = input("Name: ")
kingdom2 = input("Kingdom: ")
min_life2 = float(input("Enter minimum life points: "))
max_life2 = float(input("Enter maximum life points: "))
while min_life2 < 0 or max_life2 < min_life2:
    print("Invalid range. Min life must be positive and not greater than max life.")
    min_life2 = float(input("Enter minimum life points: "))
    max_life2 = float(input("Enter maximum life points: "))


life_points2 = random.uniform(min_life2, max_life2)
soldier2 = Soldier(name2, kingdom2, life_points2)

print("\nInitial Soldier Status")
print(soldier1)
print(soldier2)

soldier1.fight(soldier2)

print("\nFinal Soldier Status")
print(soldier1)
print(soldier2)
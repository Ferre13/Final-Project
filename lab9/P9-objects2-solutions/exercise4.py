import random
from soldier import Soldier

first_kingdom = input("Enter the name of the first kingdom: ")
first_soldier_name = input("Enter the name of the first soldier: ")

first_min_life = int(input("Min life of the first soldier: "))
while first_min_life < 1:
    first_min_life = int(input("Min life of the first soldier (>=1): "))

first_max_life = int(input("Max life of the first soldier: "))
while first_max_life < first_min_life:
    first_max_life = int(input("Max life must be >= min life. Enter again: "))

first_lp = random.randint(first_min_life, first_max_life)
soldier1 = Soldier(first_soldier_name, first_kingdom, first_lp)

second_kingdom = input("Enter the name of the second kingdom: ")
second_soldier_name = input("Enter the name of the second soldier: ")

second_min_life = int(input("Min life of the second soldier: "))
while second_min_life < 1:
    second_min_life = int(input("Min life of the second soldier (>=1): "))

second_max_life = int(input("Max life of the second soldier: "))
while second_max_life < second_min_life:
    second_max_life = int(input("Max life must be >= min life. Enter again: "))

second_lp = random.randint(second_min_life, second_max_life)
soldier2 = Soldier(second_soldier_name, second_kingdom, second_lp)

print("Before the fight:")
print(soldier1)
print(soldier2)

soldier1.fight(soldier2)

print("After the fight:")
print(soldier1)
print(soldier2)

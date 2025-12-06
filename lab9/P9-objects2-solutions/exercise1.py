from person import Person

person1 = Person("Pepe", 28, 10564349, "male", 80.0, 190.0)

name2 = input("Enter a name: ")
age2 = int(input("Enter an age: "))
dni2 = int(input("Enter an ID number (DNI): "))
gender2 = input("Enter gender (male/female/non-binary): ")
weight2 = float(input("Enter weight (kg): "))
height2 = float(input("Enter height (cm): "))

person2 = Person(name2, age2, dni2, gender2, weight2, height2)

name3 = input("Enter a name: ")
age3 = int(input("Enter an age: "))
dni3 = int(input("Enter an ID number (DNI): "))

# Default values for the third person: weight=90, height=185, sex='non-binary'
person3 = Person(name3, age3, dni3, "non-binary", 90, 185)

# First tuple using auxiliary variables
tpl1 = (person1, person2, person3)
for p in tpl1:
    print(p)

# Second tuple creating objects inline
tpl2 = (
    Person("Pepe", 28, 10564349, "male", 80.0, 190.0),
    Person(name2, age2, dni2, gender2, weight2, height2),
    Person(name3, age3, dni3, "non-binary", 90, 185),
)
for p in tpl2:
    print(p)

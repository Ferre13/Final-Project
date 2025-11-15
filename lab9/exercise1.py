"""
Create a Person class that contains the following attributes: name, age, DNI (spanish ID card
number), DNI_letter, sex (male, female, other), weight and height. Create an init method giving
the appropriate value to each attribute. The DNIletter field must be calculated automatically
(you should look for information on the Internet on how to calculate this field knowing the ID
number). Create properties/setters for all the attributes:
"""

class Person:
    def __init__(self, name: str, age: int, DNI: int, sex: str, weight: float, height: float):
        self.name = name
        self.age = age
        self.DNI = DNI
        self.sex = sex
        self.weight = weight
        self.height = height

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name: str):
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        if len(name) == 0:
            raise ValueError("Name must have at least one letter.")
        self.__name = name

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, age: int):
        if not isinstance(age, int):
            raise TypeError("Age must be an integer.")
        if age <= 0:
            raise ValueError("Age must be bigger than 0.")
        self.__age = age

    @property
    def sex(self):
        return self.__sex

    @sex.setter
    def sex(self, sex: str):
        SEXES = ("male", "female", "non-binary")
        if not isinstance(sex, str):
            raise TypeError("Sex must be a string.")
        if sex.lower() not in SEXES:
            raise ValueError("Sex must be male, female or non-binary." )
        self.__sex = sex.lower()

    @property
    def DNI(self):
        return self.__DNI

    @DNI.setter
    def DNI(self, DNI: int):
        if not isinstance(DNI, int):
            raise TypeError("DNI must be an integer.")
        if len(str(DNI)) > 8 or DNI <= 0:
            raise ValueError("DNI must be a positive number of a maximum of 8 digits.")
        
        DNI_letter = self._DniLetterCalculator(DNI)
        self.__DNI = str(DNI) + DNI_letter
    
    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, weight: float):
        if not isinstance(weight, (int, float)):
            raise TypeError("Weight must be a number (float or int).")
        if weight <= 0:
            raise ValueError("It must be bigger than 0.")
        self.__weight = float(weight)

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, height: float):
        if not isinstance(height, (int, float)):
            raise TypeError("Height must be a number (float or int).")
        if height <= 0:
            raise ValueError("It must be bigger than 0.")
        self.__height = float(height)


    def _DniLetterCalculator(self, DNI: int):
        DNI_LETTERS = "TRWAGMYFPDXBNJZSQVHLCKE"
        pos = DNI % 23
        return DNI_LETTERS[pos]
    
    def __str__(self):
        return (
            "\n\nPersonal information:\n"
            f"Name: {self.name}\n"
            f"Gender: {self.sex}\n"
            f"Age: {self.age} years old\n"
            f"DNI: {self.DNI}\n"
            f"Weight: {self.weight:.1f} kg\n"
            f"Height: {self.height:.1f} cm"
        )
    
person1 = Person("Rodrigo", 18, 87654321, "male", 65, 172)

print("\nEnter details for person 2.")
name_2 = input("Name: ")
age_2 = int(input("Age: "))
dni_2 = int(input("DNI (8 digits, no letter): "))
sex_2 = input("Sex (male/female/non-binary): ")
weight_2 = float(input("Weight (kg): "))
height_2 = float(input("Height (cm): "))
person2 = Person(name_2, age_2, dni_2, sex_2, weight_2, height_2)

print("\nEnter details for person 3.")
name_3 = input("Name: ")
age_3 = int(input("Age: "))
dni_3 = int(input("DNI (8 digists, no letter): "))
person3 = Person(name_3, age_3, dni_3, "Male", 90, 185)

print(person1, person2, person3)

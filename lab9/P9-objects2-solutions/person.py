class Person:
    """
    Person class with validated properties and automatic DNI letter calculation.
    """

    def __init__(self, name: str, age: int, dni: int, sex: str, weight: float, height: float):
        self.name = name
        self.age = age
        self.dni = dni  # triggers letter calculation
        self.sex = sex
        self.weight = weight
        self.height = height

    # -----------------------------
    # Internal helpers
    # -----------------------------
    def _dni_letter_calculator(self) -> str:
        """Calculates the Spanish DNI letter based on the dni number."""
        letters = "TRWAGMYFPDXBNJZSQVHLCKE"
        return letters[self._dni % 23]

    # -----------------------------
    # Properties
    # -----------------------------
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Name must be a non-empty string")
        self._name = value

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Age must be an integer")
        if value <= 0:
            raise ValueError("Age must be greater than 0")
        self._age = value

    @property
    def sex(self) -> str:
        return self._sex

    @sex.setter
    def sex(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Sex must be a string")
        normalized = value.strip().lower()
        valid = {"male", "female", "non-binary"}
        if normalized not in valid:
            raise ValueError("Sex must be one of: male, female, non-binary")
        self._sex = normalized

    @property
    def dni(self) -> int:
        return self._dni

    @dni.setter
    def dni(self, value: int):
        if not isinstance(value, int):
            raise TypeError("DNI must be an integer")
        if not (1 <= value <= 99999999):
            raise ValueError("DNI must be a positive integer up to 8 digits")
        self._dni = value
        # Recalculate letter whenever DNI changes
        self._dni_letter = self._dni_letter_calculator()

    @property
    def dni_letter(self) -> str:
        return self._dni_letter

    @property
    def weight(self) -> float:
        return self._weight

    @weight.setter
    def weight(self, value: float):
        if not isinstance(value, (int, float)):
            raise TypeError("Weight must be a number")
        if value <= 0:
            raise ValueError("Weight must be greater than 0")
        self._weight = float(value)

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, value: float):
        if not isinstance(value, (int, float)):
            raise TypeError("Height must be a number")
        if value <= 0:
            raise ValueError("Height must be greater than 0")
        self._height = float(value)

    # -----------------------------
    # String representation
    # -----------------------------
    def __str__(self) -> str:
        # Capitalize sex for display
        display_sex = {
            "male": "Male",
            "female": "Female",
            "non-binary": "Non-binary"
        }.get(self.sex, self.sex.capitalize())

        return (
            "Personal information:\n"
            f"Name: {self.name}\n"
            f"Gender: {display_sex}\n"
            f"Age: {self.age} years old\n"
            f"DNI: {self.dni}-{self.dni_letter}\n"
            f"Weight: {self.weight:.1f} kg\n"
            f"Height: {self.height:.1f} cm\n"
        )

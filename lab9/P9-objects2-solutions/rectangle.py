class Rectangle:
    """
    Rectangle class with validated properties.
    - If only base is provided, a square is created (height = base).
    - Relational operators compare by the longest side.
    """

    def __init__(self, base, height=None):
        self.base = base
        # If height is not provided, make it a square
        self.height = base if height is None else height

    # -----------------------------
    # Validators
    # -----------------------------
    def _validate_number(self, value, name: str) -> float:
        if not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be a number")
        if value <= 0:
            raise ValueError(f"{name} must be greater than 0")
        return float(value)

    # -----------------------------
    # Properties
    # -----------------------------
    @property
    def base(self) -> float:
        return self._base

    @base.setter
    def base(self, value):
        self._base = self._validate_number(value, "Base")

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, value):
        self._height = self._validate_number(value, "Height")

    @property
    def square(self) -> bool:
        return self.base == self.height

    # -----------------------------
    # String and equality
    # -----------------------------
    def __str__(self) -> str:
        kind = "square" if self.square else "rectangle"
        return f"a {kind} with base {self.base} and height {self.height}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Rectangle):
            raise TypeError("Can only compare with another Rectangle")
        return ((self.base == other.base and self.height == other.height) or
                (self.base == other.height and self.height == other.base))

    # -----------------------------
    # Geometry
    # -----------------------------
    def perimeter(self) -> float:
        return 2 * (self.base + self.height)

    def area(self) -> float:
        return self.base * self.height

    def longest_side(self) -> float:
        return self.base if self.base >= self.height else self.height

    def make_square(self) -> bool:
        """
        Converts the rectangle into a square by setting the shorter side
        to the value of the longer side.
        Returns:
          True  -> base was changed
          False -> height was changed
        """
        m = self.longest_side()
        if m == self.base:
            # Change height to match base
            self.height = m
            return False
        else:
            # Change base to match height
            self.base = m
            return True

    # -----------------------------
    # Relational operators (by longest side)
    # -----------------------------
    def __lt__(self, other) -> bool:
        if not isinstance(other, Rectangle):
            raise TypeError("Can only compare with another Rectangle")
        return self.longest_side() < other.longest_side()

    def __le__(self, other) -> bool:
        if not isinstance(other, Rectangle):
            raise TypeError("Can only compare with another Rectangle")
        return self.longest_side() <= other.longest_side()

    def __gt__(self, other) -> bool:
        if not isinstance(other, Rectangle):
            raise TypeError("Can only compare with another Rectangle")
        return self.longest_side() > other.longest_side()

    def __ge__(self, other) -> bool:
        if not isinstance(other, Rectangle):
            raise TypeError("Can only compare with another Rectangle")
        return self.longest_side() >= other.longest_side()

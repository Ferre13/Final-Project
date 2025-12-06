class GameObject:
    """
    A parent class for all static, non-interactive game objects.
    It provides base `x` and `y` properties.
    """
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    @property
    def x(self) -> float: return self.__x
    @x.setter
    def x(self, value: float):
        if not isinstance(value, (int, float)): raise TypeError("x must be a number")
        self.__x = float(value)

    @property
    def y(self) -> float: return self.__y
    @y.setter
    def y(self, value: float):
        if not isinstance(value, (int, float)): raise TypeError("y must be a number")
        self.__y = float(value)
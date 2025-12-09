class GameObject:
    """
    This class serves as a base for all game objects, since they all have x and y coordinates.
    It provides basic properties and type checking for these coordinates.
    """
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    # We use floats to track movement with decimals. It keeps the animation smooth and prevents rounding errors. We convert to int only when drawing
    @property
    def x(self) -> float: 
        return self.__x
    @x.setter
    def x(self, value: float):
        if not isinstance(value, (int, float)): 
            raise TypeError("x must be a number")
        self.__x = float(value)

    @property
    def y(self) -> float: 
        return self.__y
    @y.setter
    def y(self, value: float):
        if not isinstance(value, (int, float)): 
            raise TypeError("y must be a number")
        self.__y = float(value)
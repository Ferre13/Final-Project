import constants

class Conveyor:
    """ This class represents the conveyor belt in the game. """
    def __init__(self, image: str, speed: int, x_pos: int, y_pos: int):
        """ This is the magic method we must use to declare the attributes of our objects.
        :param image: str - The image of the conveyor belt
        :param speed: int - The speed of the conveyor belt
        """
        # Attributes must always start by self.
        self.image = image
        self.speed = speed
        self.x_pos = x_pos
        self.y_pos = y_pos

    @property
    def image(self):
        """ This is the getter method for the image attribute """
        return self.__image
    
    @image.setter
    def image(self, image: str):
        """ This is the setter method for the image attribute """
        if not isinstance(image, str):
            raise TypeError("The image must be a string")
        self.__image = image

    @property
    def speed(self):
        """ This is the getter method for the speed attribute """
        return self.__speed
    
    @speed.setter
    def speed(self, speed: int):
        """ This is the setter method for the speed attribute """
        if not isinstance(speed, int):
            raise TypeError("The speed must be an integer")
        self.__speed = speed

    @property
    def x_pos(self):
        """ This is the getter method for the x_pos attribute """
        return self.__x_pos
    
    @x_pos.setter
    def x_pos(self, x_pos: int):
        """ This is the setter method for the x_pos attribute """
        if not isinstance(x_pos, int):
            raise TypeError("The x position must be an integer")
        self.__x_pos = x_pos

    @property
    def y_pos(self):
        """ This is the getter method for the y_pos attribute """
        return self.__y_pos
    
    @y_pos.setter
    def y_pos(self, y_pos: int):
        """ This is the setter method for the y_pos attribute """
        if not isinstance(y_pos, int):
            raise TypeError("The y position must be an integer")
        self.__y_pos = y_pos
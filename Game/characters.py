import constants

class Character:
    """ This class represents the characters in the game (Mario and Luigi). """
    def __init__(self, image: str, side: str, x_pos: int):
        """ This is the magic method we must use to declare the attributes of our objects.
        :param image: str - The image of the character
        :param side: str - The side where the character is located
        """
        # Attributes must always start by self.
        self.image = image
        self.side = side
        # I assume character will always start on the lower part of the screen so
        # I don't need a parameter for this attribute
        self.vertical_pos = 0
        sprite = (0, 0, 0, 16, 24, 0) # img, x_ins, y_ins, w, h, colkey
        self.sprite = sprite
        self.x_pos = x_pos

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
    def side(self):
        """ This is the getter method for the side attribute """
        return self.__side
    
    @side.setter
    def side(self, side: str):
        """ This is the setter method for the side attribute """
        if side not in ["left", "right"]:
            raise ValueError("The side must be 'left' or 'right'")
        self.__side = side

    @property
    def vertical_pos(self):
        """ This is the getter method for the vertical_pos attribute """
        return self.__vertical_pos
    
    @vertical_pos.setter
    def vertical_pos(self, vertical_pos: int):
        """ This is the setter method for the vertical_pos attribute """
        if not isinstance(vertical_pos, int):
            raise TypeError("The vertical position must be an integer")
        self.__vertical_pos = vertical_pos

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
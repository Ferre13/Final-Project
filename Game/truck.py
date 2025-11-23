import pyxel
import constants

class Truck:
    """This class respresents the truck in the game"""
    def __init__(self, image: str, x_pos:int, y_pos:int, capacity: int = 8, ):
        """This is the magic method we must use to declare the attributes of our objects.
        :param image: str - The image of the truck.
        :param capacity: int - The number of packages the truck can hold.
        """
        # Attributes must always start by self.
        self.image = image
        class Truck:
            """This class respresents the truck in the game"""
            def __init__(self, image: str, x_pos:int, y_pos:int, capacity: int = 8, ):
                """This is the magic method we must use to declare the attributes of our objects.
                :param image: str - The image of the truck.
                :param capacity: int - The number of packages the truck can hold.
                """
                # Attributes must always start by self.
                self.image = image
                self.x_pos = x_pos
                self.y_pos = y_pos
                self.capacity = capacity
                self.packages_loaded = 0
                self.is_away = False
                self.is_moving_away = False
                self.is_animating = False
                self.animation_timer = 0
                self._sprites = [
                    constants.TRUCK_EMPTY, constants.TRUCK_1, constants.TRUCK_2, constants.TRUCK_3, constants.TRUCK_4,
                    constants.TRUCK_5, constants.TRUCK_6, constants.TRUCK_7, constants.TRUCK_8, constants.TRUCK_FULL
                ]
                
            @property
            def image(self):
                """ This is the getter method for the image attribute """
                return self.__image
            
            @image.setter
            def image(self, image:str):
                """ This is the setter method for the image attribute """
                if not isinstance(image, str):
                    raise TypeError("The image must be a string")
                self.__image = image

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
            
            
            @property
            def packages_loaded(self):
                """ This is the getter method for the packages_loaded attribute """
                return self.__packages_loaded
            
            @packages_loaded.setter
            def packages_loaded(self, packages_loaded: int):
                """ This is the setter method for the packages_loaded attribute """
                if not isinstance(packages_loaded, int):
                    raise TypeError("The packages loaded must be an integer")
                self.__packages_loaded = packages_loaded
                
            @property
            def capacity(self):
                """ This is the getter method for the capacity attribute """
                return self.__capacity
            
            @capacity.setter
            def capacity(self, capacity: int):
                """ This is the setter method for the capacity attribute """
                if not isinstance(capacity, int):
                    raise TypeError("The capacity must be an integer")
                self.__capacity = capacity
            
            @property
            def is_animating(self):
                return self.__is_animating
            
            @is_animating.setter
            def is_animating(self, is_animating):
                self.__is_animating = is_animating
            
            @property
            def animation_timer(self):
                return self.__animation_timer
            
            @property
            def is_moving_away(self):
                return self.__is_moving_away
            
            @is_moving_away.setter
            def is_moving_away(self, is_moving_away):
                self.__is_moving_away = is_moving_away
            
            @animation_timer.setter
            def animation_timer(self, animation_timer):
                self.__animation_timer = animation_timer    
            
            @property
            def is_full(self):
                return self.__packages_loaded >= self.__capacity
            
            @property
            def is_away(self):
                return self.__is_away
            @is_away.setter
            def is_away(self, is_away):
                self.__is_away = is_away
                
            
            """ These are the methods of the Truck class """
            
            def draw(self):
                """
                Draws the truck on the screen.
                """
                if not self.is_away or self.__is_moving_away:
                    sprite = self._sprites[self.__packages_loaded]
                    if self.is_animating:
                        if (self.__animation_timer // 30) % 2 == 0:
                            sprite = constants.TRUCK_FULL
                        else:
                            sprite = self._sprites[8]
                    
                    pyxel.blt(self.x_pos, self.y_pos, *sprite)
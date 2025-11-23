import pyxel
from constants import (
    GAME_PLAYING, GAME_PAUSE, GAME_OVER, GAME_TRUCK,
    NUM_CONVEYORS_EASY, NUM_CONVEYORS_MEDIUM, NUM_CONVEYORS_EXTREME, NUM_CONVEYORS_CRAZY,
    SLOW_SPEED, MEDIUM_SPEED, FAST_SPEED, RANDOM_SPEED, CONVEYOR_LENGTH,
    CONVEYOR_X_RIGHT, CONVEYOR_X_LEFT,
    MARIO_X, LUIGI_X,
    BOSS_LUIGI, BOSS_Y, TRUCK_X, TRUCK_Y,
    BOSS_SCENE, MAX_FAILURES,
    POINTS_PER_PACKAGE, PLATFORM_SPRITE, EXIT_SIGNAL_SPRITE
)
from conveyor import Conveyor
from truck import Truck
from platforms import Platform
from background import Background

class Board:
    """ This class represents the game board. """
    def __init__(self, width: int, height: int, difficulty: str = "easy"):
        """ This is the magic method we must use to declare the attributes of our objects.
        :param image: str - The image of the board
        :param width: The width of the game screen.
        :param height: The height of the game screen.
        :param difficulty: The chosen difficulty level.
        """
        # Attributes must always start by self.
        self.width = width
        self.height = height
        self.difficulty = difficulty
        
        self.score = 0
        self.failures = 0
        self.game_state = GAME_PLAYING
        
        # Game elements
        self.truck = Truck(image="truck_image", x_pos=TRUCK_X, y_pos=TRUCK_Y)
        
        if self.difficulty == "easy":
            self.num_conveyors = NUM_CONVEYORS_EASY
            self.conveyor_speed = SLOW_SPEED
        elif self.difficulty == "medium":
            self.num_conveyors = NUM_CONVEYORS_MEDIUM
            self.conveyor_speed = MEDIUM_SPEED
        elif self.difficulty == "extreme":
            self.num_conveyors = NUM_CONVEYORS_EXTREME
            self.conveyor_speed = FAST_SPEED
        elif self.difficulty == "crazy":
            self.num_conveyors = NUM_CONVEYORS_CRAZY
            self.conveyor_speed = RANDOM_SPEED
        
    """
        self.conveyors: List[Conveyor] = self.__create_conveyors()
        self.platforms: List[Platform] = self.__create_platforms()
        self.background = Background(image="background_image", width=width, height=height)
        self.packages: List[Package] = []
    """       

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
    def width(self):
        """ This is the getter method for the width attribute """
        return self.__width
    @width.setter
    def width(self, width: int):
        """ This is the setter method for the width attribute """
        if not isinstance(width, int):
            raise TypeError("The width must be an integer")
        self.__width = width
        
    @property
    def height(self):
        """ This is the getter method for the height attribute """
        return self.__height
    @height.setter
    def height(self, height: int):
        """ This is the setter method for the height attribute """
        if not isinstance(height, int):
            raise TypeError("The height must be an integer")
        self.__height = height
        
    @property
    def difficulty(self):
        """ This is the getter method for the difficulty attribute """
        return self.__difficulty
    @difficulty.setter
    def difficulty(self, difficulty: str):
        """ This is the setter method for the difficulty attribute """
        if difficulty not in ["easy", "medium", "extreme", "crazy"]:
            raise ValueError("The difficulty must be 'easy', 'medium', 'extreme', or 'crazy'")
        self.__difficulty = difficulty
        
    @property
    def score(self):
        """ This is the getter method for the score attribute """
        return self.__score
    @score.setter
    def score(self, score: int):
        """ This is the setter method for the score attribute """
        if not isinstance(score, int):
            raise TypeError("The score must be an integer")
        self.__score = score
        
    @property
    def failures(self):
        """ This is the getter method for the failures attribute """
        return self.__failures
    @failures.setter
    def failures(self, failures: int):
        """ This is the setter method for the failures attribute """
        if not isinstance(failures, int):
            raise TypeError("The failures must be an integer")
        self.__failures = failures
        
    @property
    def game_state(self):
        """ This is the getter method for the game_state attribute """
        return self.__game_state
    @game_state.setter
    def game_state(self, game_state: str):
        """ This is the setter method for the game_state attribute """
        if game_state not in [GAME_PLAYING, GAME_PAUSE, GAME_OVER, GAME_TRUCK]:
            raise ValueError("The game state must be a valid state")
        self.__game_state = game_state
    
    @property
    def truck(self):
        """ This is the getter method for the truck attribute """
        return self.__truck
    @truck.setter
    def truck(self, truck: Truck):
        """ This is the setter method for the truck attribute """
        if not isinstance(truck, Truck):
            raise TypeError("The truck must be a Truck object")
        self.__truck = truck
    
    def draw(self):
        """
        Draws the board and its elements on the screen.
        """
        # Draws the background
        self.background.draw()
        
        # Draws the platforms, conveyors and packages
        for platform in self.platforms:
            platform.draw()
        for conveyor in self.conveyors:
            conveyor.draw()
        for package in self.packages:
            package.draw()
            
        # Draws the truck
        self.truck.draw()
        
        # Draws the characters
        
        # Draws Packages
        
        # Draws Score and Failures
        pyxel.text(5, 5, f"Score: {self.score}", pyxel.frame_count % 16)
        pyxel.text(5, 15, f"Failures: {self.failures}", pyxel.frame_count % 16)
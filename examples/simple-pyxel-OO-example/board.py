from character import Character
import pyxel


class Board:
    """This class contains a simple board"""

    def __init__(self, width: int, height: int):
        """ Method that creates the board.
        :param width: The width of the board
        :param height: The height of the board
        """
        # Setting the attributes
        self.width = width
        self.height = height
        # The board will contain a Character in the middle of it
        self.character = Character(self.width//2, self.height//2)

        # In this init we also initialize pyxel
        # This instruction is used to initialize pyxel, see API for more parameters
        pyxel.init(self.width, self.height, title="Pyxel game demo")
        # Loading the pyxres file with the images
        pyxel.load("assets/example.pyxres")
        # Running the game
        pyxel.run(self.update, self.draw)

    # Properties and setters
    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @width.setter
    def width(self, width: int):
        if not isinstance(width, int):
            raise TypeError("The width must be an integer " + str(type(width)) + "is provided")
        elif width < 1 or width > 256:
            raise ValueError("The width must be in the range 1 to 256")
        else:
            self.__width = width

    @height.setter
    def height(self, height: int):
        if not isinstance(height, int):
            raise TypeError("The height must be an integer " + str(type(height)) + "is provided")
        elif height < 1 or height > 256:
            raise ValueError("The height must be in the range 1 to 256")
        else:
            self.__height = height

    def update(self):
        """ This is a pyxel method that gets executed in every iteration of the game (every
        frame). You need to put here all the code that has to be executed in every frame. Now
        it contains only the logic to move the character if a key is pressed."""
        # To exit the game
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        # horizontal movement
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.character.move('right', self.width)
        elif pyxel.btn(pyxel.KEY_LEFT):
            self.character.move('left', self.width)

    def draw(self):
        """This is a pyxel method that gets executed in every iteration of the game (every
        frame). You need to put here all the code to draw the sprites of the game.
        """
        # Erasing the previous screen
        pyxel.cls(0)
        # Drawing the character, parameters of pyxel.blt are (x, y, sprite tuple)
        pyxel.blt(self.character.x, self.character.y, *self.character.sprite)

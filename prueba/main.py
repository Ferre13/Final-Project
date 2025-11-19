import pyxel
from board import Board
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Game:
    """
    The main game class that ties everything together.
    """

    def __init__(self):
        """
        Initializes the game.
        """
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Mario Bros. Factory")
        
        # TODO: You need to create a 'my_resource.pyxres' file using the 
        # Pyxel editor and place it in the same directory as main.py.
        # For now, the game will run with placeholder graphics.
        # try:
        pyxel.load("assets/my_resource.pyxres")
        # except Exception:
        #     print("Could not load resource file. Please create 'my_resource.pyxres'.")


        self.board = Board(SCREEN_WIDTH, SCREEN_HEIGHT, difficulty="easy")
        
        pyxel.run(self.update, self.draw)

    def update(self):
        """
        The main update loop of the game.
        """
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.board.update()

    def draw(self):
        """
        The main draw loop of the game.
        """
        self.board.draw()

if __name__ == "__main__":
    Game()

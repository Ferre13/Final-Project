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
        
        pyxel.load("assets/my_resource.pyxres")

        self.difficulty = "easy"
        self.board = Board(SCREEN_WIDTH, SCREEN_HEIGHT, difficulty=self.difficulty)
        
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

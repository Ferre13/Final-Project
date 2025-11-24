import pyxel
import constants
import board

class Game:
    def __init__(self):
        pyxel.init(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, title="Mario Bros Game")
        pyxel.load(constants.SPRITES_FILE)
        
        self.board = board.Board("EXTREME")
        
        pyxel.run(self.update, self.draw)

    def update(self):            
        self.board.update()

    def draw(self):
        pyxel.cls(0)
        self.board.draw()

if __name__ == "__main__":
    Game()
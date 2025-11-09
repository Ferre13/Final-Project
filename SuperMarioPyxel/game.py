import pyxel
from player import Player
from level import Level

class Game:
    """Main class for the game."""

    def __init__(self):
        """Initializes the game."""
        # Initialize Pyxel
        pyxel.init(256, 256, title="Super Mario Pyxel")

        # Load assets
        pyxel.load("assets/mario.pyxres")

        # Create game objects
        self.player = Player(50, 50)
        self.level = Level()

        # Start the game loop
        pyxel.run(self.update, self.draw)

    def update(self):
        """Updates the game state."""
        self.player.update()
        self.level.update()

    def draw(self):
        """Draws the game objects."""
        pyxel.cls(0)
        self.level.draw()
        self.player.draw()

if __name__ == "__main__":
    Game()

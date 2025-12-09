import pyxel
from game import Game

# Create an instance of the main Game class
game_instance = Game()

# Run the Pyxel application, passing the update and draw methods
pyxel.run(game_instance.update, game_instance.draw)
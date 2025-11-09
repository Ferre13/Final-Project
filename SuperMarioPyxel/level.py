import pyxel
from enemy import Enemy

class Level:
    """The game level."""

    def __init__(self):
        """Initializes the level."""
        self.platforms = []
        self.enemies = []
        # Add platforms and enemies
        self.platforms.append((0, 240, 256, 16)) # Ground
        self.enemies.append(Enemy(100, 224))

    def update(self):
        """Updates the level's state."""
        for enemy in self.enemies:
            enemy.update()

    def draw(self):
        """Draws the level."""
        for x, y, w, h in self.platforms:
            pyxel.rect(x, y, w, h, 7)
        for enemy in self.enemies:
            enemy.draw()

import pyxel


    """An enemy character (Goomba)."""

    def __init__(self, x, y):
        """Initializes the enemy."""
        self.x = x
        self.y = y
        self.dx = -1

    def update(self):
        """Updates the enemy's state."""
        self.x += self.dx

    def draw(self):
        """Draws the enemy."""
        pyxel.blt(self.x, self.y, 0, 16, 0, 16, 16, 0)

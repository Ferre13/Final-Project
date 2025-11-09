import pyxel

class Player:
    """The player character (Mario)."""

    def __init__(self, x, y):
        """Initializes the player."""
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.is_jumping = False
        self.direction = 1  # 1 for right, -1 for left

    def update(self):
        """Updates the player's state."""
        # Handle input
        if pyxel.btn(pyxel.KEY_LEFT):
            self.dx = -2
            self.direction = -1
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.dx = 2
            self.direction = 1

        # Apply gravity
        self.dy += 0.5

        # Update position
        self.x += self.dx
        self.y += self.dy

        # Reset horizontal movement
        self.dx = 0

    def draw(self):
        """Draws the player."""
        # The width of the sprite is multiplied by the direction
        w = 16 * self.direction
        pyxel.blt(self.x, self.y, 0, 0, 0, w, 16, 0)

    def jump(self):
        """Makes the player jump."""
        if not self.is_jumping:
            self.dy = -5
            self.is_jumping = True

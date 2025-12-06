import constants
import pyxel
from game_object import GameObject

class Door(GameObject):
    """ 
    Represents a door for the boss's appearance. It's a simple state machine
    that handles its own opening and closing animations.
    """
    def __init__(self, x: int, y: int):
        """
        Initializes a door at a specific location.

        :param x: The x-coordinate.
        :param y: The y-coordinate.
        """
        super().__init__(x, y)
        self.state = constants.DOOR_STATE_CLOSED
        self.sprites = constants.DOOR_SPRITES
        self.animation_start_frame = 0
            
    def open(self):
        """Starts the sequence to open the door."""
        if self.state == constants.DOOR_STATE_CLOSED:
            self.state = constants.DOOR_STATE_OPENING 
            self.animation_start_frame = pyxel.frame_count
    
    def close(self):
        """Starts the sequence to close the door."""
        if self.state == constants.DOOR_STATE_OPEN:
            self.state = constants.DOOR_STATE_CLOSING
            self.animation_start_frame = pyxel.frame_count

    def update(self):
        """Updates the door's state based on its animation timing."""
        if self.state == constants.DOOR_STATE_OPENING:
            if pyxel.frame_count >= self.animation_start_frame + constants.DOOR_ANIMATION_SPEED:
                self.state = constants.DOOR_STATE_OPEN

        elif self.state == constants.DOOR_STATE_CLOSING:
            if pyxel.frame_count >= self.animation_start_frame + constants.DOOR_ANIMATION_SPEED:
                self.state = constants.DOOR_STATE_CLOSED
            
    def draw(self):
        """Draws the door sprite that corresponds to its current state."""
        # The sprite is selected from the dictionary using the state string as the key.
        pyxel.blt(self.x, self.y, *self.sprites[self.state])
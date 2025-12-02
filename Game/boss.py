import constants
import pyxel

class Boss:
    """ 
    Manages the state and animation for the boss character. The boss appears
    when a player fails or after a successful truck delivery. This class acts
    as a state machine that coordinates with the Door objects.
    """
    def __init__(self, door_left, door_right):
        """
        Initializes the Boss.

        :param door_left: The Door object on the left side of the screen.
        :param door_right: The Door object on the right side of the screen.
        """
        self.door_left = door_left
        self.door_right = door_right
        
        self.state = constants.BOSS_STATE_IDLE
        self.target = None # Determines which side the boss appears on ('Mario', 'Luigi', or 'BOTH')
        self.yell_start_frame = 0
        self.active_doors = []

    @property
    def state(self) -> int: return self.__state
    @state.setter
    def state(self, value: int):
        if not isinstance(value, int): raise TypeError("State must be an integer")
        self.__state = value

    @property
    def is_active(self) -> bool:
        """Returns True if the boss is currently in any state other than IDLE."""
        return self.state != constants.BOSS_STATE_IDLE

    def appear(self, reason: str):
        """
        Starts the boss appearance sequence.

        :param reason: A string that determines why the boss is appearing.
                       - "MARIO_FAIL": Boss appears on the right for Mario.
                       - "LUIGI_FAIL": Boss appears on the left for Luigi.
                       - "BREAK": Boss appears on both sides for a work break.
        """
        if self.is_active: # Prevent starting a new sequence while one is running
            return

        self.state = constants.BOSS_STATE_OPENING
        self.active_doors = []
        
        if reason == "MARIO_FAIL":
            self.target = "Mario"
            self.active_doors.append(self.door_right)
        elif reason == "LUIGI_FAIL":
            self.target = "Luigi"
            self.active_doors.append(self.door_left)
        elif reason == "BREAK":
            self.target = "BOTH"
            self.active_doors = [self.door_left, self.door_right]
            
        for d in self.active_doors:
            d.open()

    def update(self):
        """Updates the boss's state machine."""
        if self.state == constants.BOSS_STATE_IDLE: 
            return

        # State 1: Wait for the active doors to be fully open.
        if self.state == constants.BOSS_STATE_OPENING:
            if all(d.state == constants.DOOR_STATE_OPEN for d in self.active_doors):
                self.state = constants.BOSS_STATE_YELLING
                self.yell_start_frame = pyxel.frame_count

        # State 2: Stay in the "yelling" state for a set duration.
        elif self.state == constants.BOSS_STATE_YELLING:
            if pyxel.frame_count >= self.yell_start_frame + constants.BOSS_YELL_DURATION:
                self.state = constants.BOSS_STATE_CLOSING
                for d in self.active_doors: 
                    d.close()

        # State 3: Wait for the active doors to be fully closed, then return to idle.
        elif self.state == constants.BOSS_STATE_CLOSING:
            if all(d.state == constants.DOOR_STATE_CLOSED for d in self.active_doors):
                self.state = constants.BOSS_STATE_IDLE
                self.active_doors = []

    def draw(self):
        """Draws the boss character if he is currently yelling."""
        if self.state == constants.BOSS_STATE_YELLING:
            # Alternate between two sprites to create a simple animation.
            if (pyxel.frame_count // constants.BOSS_ANIMATION_SPEED) % 2 == 0:
                sprite = constants.BOSS_1
            else:
                sprite = constants.BOSS_2

            img, u, v, w, h, colkey = sprite
            
            # Adjust y-position to align the sprite correctly with the floor.
            draw_y = constants.BOSS_Y + constants.BOSS_DRAW_Y_OFFSET
            
            # Draw on the right side if the target is Mario or both.
            if self.target == "BOTH" or self.target == "Mario":
                pyxel.blt(constants.BOSS_MARIO, draw_y, img, u, v, abs(w), h, colkey)
            
            # Draw on the left side (flipped) if the target is Luigi or both.
            if self.target == "BOTH" or self.target == "Luigi":
                pyxel.blt(constants.BOSS_LUIGI, draw_y, img, u, v, -abs(w), h, colkey)
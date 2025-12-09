import constants
import pyxel
from door import Door
from character import Character

class Boss:
    """Manages the boss character's appearance and animations."""
    def __init__(self, door_left: Door, door_right: Door):
        """
        :param door_left: The Door object for the left side.
        :param door_right: The Door object for the right side.
        """
        self.door_left = door_left
        self.door_right = door_right
        
        self.state = constants.BOSS_STATE_IDLE
        self.yell_start_frame = 0
        self.active_doors = []

    @property
    def state(self) -> int:
        """The current state of the boss"""
        return self.__state
    @state.setter
    def state(self, value: int):
        if not isinstance(value, int): raise TypeError("State must be an integer")
        self.__state = value

    @property
    def is_active(self) -> bool:
        """Returns True if the boss is not idle. To check if the boss is currently appearing."""
        return self.state != constants.BOSS_STATE_IDLE

    def __start_appearance(self):
        """A private helper to begin the door-opening sequence."""
        self.state = constants.BOSS_STATE_OPENING
        for door in self.active_doors:
            door.open()

    def appear_for_break(self):
        """Starts the boss sequence for a work break."""
        if self.is_active:
            return # Don't start if already active
        self.active_doors = [self.door_left, self.door_right]
        self.__start_appearance()

    def appear_for_fail(self, character: Character):
        """
        Starts the boss sequence for a character's failure.
        :param character: The character that failed.
        """
        if self.is_active: 
            return # Don't start if already active
        self.active_doors = []
        # To know if its Mario or Luigi who failed (based on x position)
        if character.x > constants.CENTER_SCREEN:
            self.active_doors.append(self.door_right)
        else:
            self.active_doors.append(self.door_left)
        self.__start_appearance()

    def update(self):
        """Updates the boss's animation state machine."""
        if self.state == constants.BOSS_STATE_IDLE: 
            return
        if self.state == constants.BOSS_STATE_OPENING:
            # We define as true first and then check for false. If none are false, then all are open.
            all_doors_are_open = True
            for door in self.active_doors:
                if door.state != constants.DOOR_STATE_OPEN:
                    all_doors_are_open = False
            if all_doors_are_open:
                self.state = constants.BOSS_STATE_YELLING
                self.yell_start_frame = pyxel.frame_count
        elif self.state == constants.BOSS_STATE_YELLING:
            if pyxel.frame_count >= self.yell_start_frame + constants.BOSS_YELL_DURATION:
                self.state = constants.BOSS_STATE_CLOSING
                for door in self.active_doors: 
                    door.close()
        elif self.state == constants.BOSS_STATE_CLOSING:
            # We define as true first and then check for false. If none are false, then all are closed. Same as above.
            all_doors_are_closed = True
            for door in self.active_doors:
                if door.state != constants.DOOR_STATE_CLOSED:
                    all_doors_are_closed = False
            if all_doors_are_closed:
                self.state = constants.BOSS_STATE_IDLE
                self.active_doors = []

    def draw(self):
        """Draws the boss on the screen if he is active."""
        if self.state == constants.BOSS_STATE_YELLING:
            # Alternate between two boss sprites for a yelling animation
            if (pyxel.frame_count // constants.BOSS_ANIMATION_SPEED) % 2 == 0:
                sprite = constants.BOSS_1
            else:
                sprite = constants.BOSS_2

            img, u, v, w, h, colkey = sprite
            draw_y = constants.BOSS_Y + constants.BOSS_DRAW_Y_OFFSET
            
            # Draw on the right side if the right door is active
            if self.door_right in self.active_doors:
                pyxel.blt(constants.BOSS_MARIO, draw_y, img, u, v, abs(w), h, colkey)
            # Draw on the left side (flipped) if the left door is active
            if self.door_left in self.active_doors:
                pyxel.blt(constants.BOSS_LUIGI, draw_y, img, u, v, -abs(w), h, colkey)
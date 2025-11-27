import constants
import pyxel

class Boss:
    """ 
    Manages the Boss sequence. Uses centralized constants.
    """
    def __init__(self, door_left, door_right):
        self.door_left = door_left
        self.door_right = door_right
        
        self.state = constants.BOSS_STATE_IDLE
        self.target = None 
        self.timer = 0
        self.active_doors = []

    # --- GETTERS AND SETTERS ---
    @property
    def state(self) -> int: return self.__state
    @state.setter
    def state(self, value: int):
        if not isinstance(value, int): raise TypeError("State must be int")
        self.__state = value

    @property
    def is_active(self) -> bool:
        return self.state != constants.BOSS_STATE_IDLE

    # --- LOGIC ---
    def appear(self, reason: str):
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
        if self.state == constants.BOSS_STATE_IDLE: return

        if self.state == constants.BOSS_STATE_OPENING:
            if all(d.state == constants.DOOR_STATE_OPEN for d in self.active_doors):
                self.state = constants.BOSS_STATE_YELLING
                self.timer = constants.BOSS_YELL_DURATION

        elif self.state == constants.BOSS_STATE_YELLING:
            self.timer -= 1
            if self.timer <= 0:
                self.state = constants.BOSS_STATE_CLOSING
                for d in self.active_doors: d.close()

        elif self.state == constants.BOSS_STATE_CLOSING:
            if all(d.state == constants.DOOR_STATE_CLOSED for d in self.active_doors):
                self.state = constants.BOSS_STATE_IDLE
                self.active_doors = []

    def draw(self):
        if self.state == constants.BOSS_STATE_YELLING:
            if (pyxel.frame_count // 10) % 2 == 0:
                sprite = constants.BOSS_1
            else:
                sprite = constants.BOSS_2

            img, u, v, w, h, colkey = sprite
            
            # FIX: Changed -16 to -15 to move sprite down 1 pixel relative to floor
            draw_y = constants.BOSS_Y - 15 
            
            if self.target == "BOTH" or self.target == "Mario":
                pyxel.blt(constants.BOSS_MARIO, draw_y, img, u, v, abs(w), h, colkey)
            
            if self.target == "BOTH" or self.target == "Luigi":
                pyxel.blt(constants.BOSS_LUIGI, draw_y, img, u, v, -abs(w), h, colkey)
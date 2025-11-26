import constants
import pyxel

class Boss:
    def __init__(self):
        self.__active = False
        self.__target_character = None
        self.__x = 0
        self.__y = (constants.BOSS_Y) - 16
        self.__animation_frame = 0
        # New: Boss manages his own duration
        self.timer = 0

    @property
    def active(self) -> bool: return self.__active

    @property
    def x(self) -> int: return self.__x

    @property
    def y(self) -> int: return self.__y

    @property
    def is_finished(self) -> bool:
        """ Returns True if the boss is active but time has run out. """
        return self.__active and self.timer <= 0

    def appear(self, character_name: str):
        self.__active = True
        self.__target_character = character_name
        self.__animation_frame = 0
        self.timer = 60  # Duration set here
        
        if character_name == "Mario":
            self.__x = constants.BOSS_MARIO
        else:
            self.__x = constants.BOSS_LUIGI

    def disappear(self):
        self.__active = False
        self.__target_character = None

    def update(self):
        if self.__active:
            self.__animation_frame += 1
            if self.timer > 0:
                self.timer -= 1

    def draw(self):
        if self.__active:
            if (self.__animation_frame // 10) % 2 == 0:
                sprite = constants.BOSS_1
            else:
                sprite = constants.BOSS_2
            
            img, u, v, w, h, colkey = sprite
            
            if self.__target_character == "Luigi":
                w = -w
            
            pyxel.blt(self.x, self.y, img, u, v, w, h, colkey)
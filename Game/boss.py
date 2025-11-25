import constants
import pyxel

class Boss:
    """ 
    This class represents the boss in the game. 
    It manages the appearance and punishment logic.
    """
    def __init__(self):
        # Private attributes
        self.__active = False
        self.__target_character = None
        self.__x = 0
        
        # Floor Y is (BOSS_Y + 2). Boss sprite height is 16.
        self.__y = (constants.BOSS_Y) - 16
        self.__animation_frame = 0

    # --- Properties (Read-Only) ---

    @property
    def active(self) -> bool:
        return self.__active

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    # --- Logic Methods ---

    def appear(self, character_name: str):
        """ Activates the boss to punish a specific character. """
        self.__active = True
        self.__target_character = character_name
        self.__animation_frame = 0
        
        # Determine position based on the target
        if character_name == "Mario":
            self.__x = constants.BOSS_MARIO
        else:
            self.__x = constants.BOSS_LUIGI

    def disappear(self):
        self.__active = False
        self.__target_character = None

    def update(self):
        if self.active:
            self.__animation_frame += 1

    def draw(self):
        if self.active:
            # 1. Select the sprite based on animation frame
            if (self.__animation_frame // 10) % 2 == 0:
                sprite = constants.BOSS_1
            else:
                sprite = constants.BOSS_2
            
            img, u, v, w, h, colkey = sprite

            # 2. Orientation Logic
            # Boss sprites face Left by default.
            # If targeting Luigi (Boss appears on Left), flip to face Right.
            if self.__target_character == "Luigi":
                w = -w
            
            pyxel.blt(self.x, self.y, img, u, v, w, h, colkey)
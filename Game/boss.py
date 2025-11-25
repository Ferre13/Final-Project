import constants
import pyxel

class Boss:
    """ 
    This class represents the boss in the game. 
    """
    def __init__(self):
        # The boss is initially hidden
        self.active = False
        self.target_character = None
        self.x = 0
        
        # FIXED: Y position calculated to stand ON the floor
        # Floor Y is (BOSS_Y + 2). Boss sprite height is 16.
        self.y = (constants.BOSS_Y + 2) - 16
        
        self.animation_frame = 0
        
    def appear(self, character_name: str):
        """
        Activates the boss to punish a specific character.
        """
        self.active = True
        self.target_character = character_name
        self.animation_frame = 0
        
        # Determine position based on the target
        if character_name == "Mario":
            self.x = constants.BOSS_MARIO
        else:
            self.x = constants.BOSS_LUIGI

    def disappear(self):
        self.active = False
        self.target_character = None

    def update(self):
        if self.active:
            self.animation_frame += 1

    def draw(self):
        if self.active:
            # 1. Select the sprite based on animation frame
            if (self.animation_frame // 10) % 2 == 0:
                sprite = constants.BOSS_1
            else:
                sprite = constants.BOSS_2
            
            # 2. Unpack sprite data
            img, u, v, w, h, colkey = sprite

            # 3. Orientation Logic
            # Boss sprites face Left by default.
            # If targeting Luigi (Boss appears on Left), flip to face Right.
            if self.target_character == "Luigi":
                w = -w
            
            pyxel.blt(self.x, self.y, img, u, v, w, h, colkey)
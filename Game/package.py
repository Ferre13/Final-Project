import pyxel
import constants

class Package:
    """
    Represents a package moving through the factory along a predefined route.
    Logic: Move -> Jump to next segment automatically.
    """
    STATE_MOVING = "moving"
    STATE_WAITING = "waiting"
    def __init__(self, difficulty: str, route: list):
        self.difficulty = difficulty
        self.route = route
        self.current_segment_index = 0
        self.sprite_list = self._get_sprite_list()
        
        # --- INITIALIZATION ---
        start_segment = self.route[0]
        self.sprite_h = self.sprite_list[0][4]
        
        self.x = start_segment['start_x']
        self.y = start_segment['start_y'] - self.sprite_h
        
        self.status = self.STATE_MOVING
        self.direction = start_segment['direction']
        
        self.base_speed = self._get_speed_by_difficulty()
        self.speed = self.base_speed

    @property
    def x(self) -> int: return self.__x
    @x.setter
    def x(self, value: int): self.__x = int(value)

    @property
    def y(self) -> int: return self.__y
    @y.setter
    def y(self, value: int): self.__y = int(value)

    def _get_speed_by_difficulty(self) -> float:
        if self.difficulty == "EASY": return constants.SLOW_SPEED
        elif self.difficulty == "MEDIUM": return constants.SLOW_SPEED 
        elif self.difficulty == "EXTREME": return constants.MEDIUM_SPEED
        elif self.difficulty == "CRAZY": return constants.RANDOM_SPEED
        return constants.SLOW_SPEED

    def _get_sprite_list(self) -> list:
        if self.difficulty == "EASY": return constants.PCK_EASY_SPRITES
        elif self.difficulty == "MEDIUM": return constants.PCK_MEDIUM_SPRITES
        elif self.difficulty == "EXTREME": return constants.PCK_EXTREME_SPRITES
        elif self.difficulty == "CRAZY": return constants.PCK_CRAZY_SPRITES
        return constants.PCK_EASY_SPRITES

    def advance(self):
        """ 
        Instantly jumps the package to the start of the NEXT segment.
        """
        self.current_segment_index += 1
        
        if self.current_segment_index < len(self.route):
            # Get next segment data
            next_segment = self.route[self.current_segment_index]
            
            # Teleport coordinates
            self.x = next_segment['start_x']
            self.y = next_segment['start_y'] - self.sprite_h
            self.direction = next_segment['direction']
            
            # Resume moving immediately
            self.status = self.STATE_MOVING
        else:
            # End of route (Truck logic handled in Board)
            pass

    def update(self):
        if self.status == self.STATE_MOVING:
            # Speed Rule: Machine (Segment 0) is always speed 1
            current_speed = 1 if self.current_segment_index == 0 else self.speed
            
            self.x += current_speed * self.direction
            
            # --- CHECK SEGMENT LIMITS ---
            current_segment = self.route[self.current_segment_index]
            limit_x = current_segment['end_x']
            
            # Check if we hit the end based on direction
            reached_end = False
            if self.direction == -1 and self.x <= limit_x: # Moving Left
                self.x = limit_x
                reached_end = True
            elif self.direction == 1 and self.x >= limit_x: # Moving Right
                self.x = limit_x
                reached_end = True
            
            if reached_end:
                self.status = self.STATE_WAITING

    def draw(self):
        # Calculate sprite index
        # Segment 0 (Machine) -> Index 0
        # Segment 1 (Floor 0) -> Index 2
        # Segment 2 (Floor 1) -> Index 4
        # Pattern: index = segment * 2
        
        sprite_idx = self.current_segment_index * 2
            
        # Safety cap
        if sprite_idx >= len(self.sprite_list): 
            sprite_idx = len(self.sprite_list) - 2

        # Simple Sprite Selection
        sprite = self.sprite_list[sprite_idx]

        img, u, v, w, h, colkey = sprite
        
        draw_w = w
        
        pyxel.blt(self.x, self.y, img, u, v, w, h, colkey)
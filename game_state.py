#Phase 4:

class GameState:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.high_score = 0
    
    def add_score(self, popped_count, floating_count):
        base_points = popped_count * 10
        cascade_bonus = floating_count * 20
        level_multiplier = 1 + (self.level - 1) * 0.1
        self.score += int((base_points + cascade_bonus) * level_multiplier)
        
        if self.score > self.high_score:
            self.high_score = self.score
    
    def next_level(self):
        if self.score > self.high_score:
            self.high_score = self.score
        self.score = 0
        self.level += 1
    
    def reset(self):
        self.score = 0
        self.level = 1

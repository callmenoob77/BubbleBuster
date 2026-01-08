#This file is for the class GameState that we use to keep up with the level we re on
#and how to apply the rest of the functions going on 

class GameState:
    #sets up all the starting values
    def __init__(self):
        self.score = 0
        self.level = 1
        self.high_score = 0
        self.color_powers = 0
        self.points_for_next_power = 2000
        self.color_mode = False
        self.selected_bubble = None
    
    #adds points and checks if you earned a color power
    def add_score(self, popped_count, floating_count):
        base_points = popped_count * 10
        cascade_bonus = floating_count * 20
        level_multiplier = 1 + (self.level - 1) * 0.1
        self.score += int((base_points + cascade_bonus) * level_multiplier)
        
        if self.score > self.high_score:
            self.high_score = self.score
        
        while self.score >= self.points_for_next_power and self.color_powers < 3:
            self.color_powers += 1
            self.points_for_next_power += 2000
    
    #moves to next level and resets score
    def next_level(self):
        if self.score > self.high_score:
            self.high_score = self.score
        self.score = 0
        self.level += 1
        self.points_for_next_power = 2000
    
    #resets everything for a new game
    def reset(self):
        self.score = 0
        self.level = 1
        self.color_powers = 0
        self.points_for_next_power = 2000
        self.color_mode = False
        self.selected_bubble = None
    
    #uses one color power
    def use_color_power(self):
        if self.color_powers > 0:
            self.color_powers -= 1
            self.color_mode = False
            self.selected_bubble = None
            return True
        return False
    
    #turns color mode on or off
    def toggle_color_mode(self):
        if self.color_powers > 0:
            self.color_mode = not self.color_mode
            if not self.color_mode:
                self.selected_bubble = None
        else:
            self.color_mode = False
            self.selected_bubble = None
    
    #saves which bubble you want to recolor
    def select_bubble(self, row, col):
        self.selected_bubble = (row, col)
    
    #cancels bubble selection
    def cancel_selection(self):
        self.selected_bubble = None

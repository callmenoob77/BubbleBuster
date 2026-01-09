#This file is for the class GameState that we use to keep up with the level we re on
#and how to apply the rest of the functions going on 

from save_data import load_data, save_data, update_high_score, update_level_high_score, add_bubbles_popped, add_game_played, add_level_completed

class GameState:
    #sets up all the starting values
    def __init__(self):
        self.score = 0
        self.level = 1
        self.color_powers = 0
        self.points_for_next_power = 2000
        self.color_mode = False
        self.selected_bubble = None
        
        #load saved data
        self.save_data = load_data()
        self.high_score = self.save_data["high_score"]
    
    #adds points and checks if you earned a color power
    def add_score(self, popped_count, floating_count):
        base_points = popped_count * 10
        cascade_bonus = floating_count * 20
        level_multiplier = 1 + (self.level - 1) * 0.1
        self.score += int((base_points + cascade_bonus) * level_multiplier)
        
        if self.score > self.high_score:
            self.high_score = self.score
            update_high_score(self.save_data, self.score)
        
        #track bubbles popped
        add_bubbles_popped(self.save_data, popped_count + floating_count)
        
        while self.score >= self.points_for_next_power and self.color_powers < 3:
            self.color_powers += 1
            self.points_for_next_power += 2000
    
    #moves to next level and resets score
    def next_level(self):
        #save level high score
        update_level_high_score(self.save_data, self.level, self.score)
        add_level_completed(self.save_data)
        
        if self.score > self.high_score:
            self.high_score = self.score
            update_high_score(self.save_data, self.score)
        
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
        
        #track games played
        add_game_played(self.save_data)
    
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
    
    #gets stats for display
    def get_stats(self):
        return {
            "high_score": self.save_data["high_score"],
            "total_bubbles": self.save_data["total_bubbles_popped"],
            "games_played": self.save_data["total_games_played"],
            "levels_completed": self.save_data["levels_completed"],
            "level_scores": self.save_data["level_high_scores"]
        }

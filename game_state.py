"""
GameState class - tracks everything for current game session.
"""

from save_data import (
    load_data, save_data, update_high_score, update_level_high_score,
    add_bubbles_popped, add_game_played, add_level_completed
)


class GameState:
    """
    Manages state for a single game session.
    
    Tracks score, current level, available powers,
    and handles saving stats when levels complete.
    
    Attributes:
        score: Points earned this level
        level: Current level number
        color_powers: How many color changes available
        color_mode: True when in color change mode
        selected_bubble: Position of selected bubble or None
        high_score: Best score this session
    """
    
    def __init__(self):
        """Initialize with default values and load saved data."""
        self.score = 0
        self.level = 1
        self.color_powers = 0
        self.points_for_next_power = 2000
        self.color_mode = False
        self.selected_bubble = None
        
        # load persistent data
        self.save_data = load_data()
        self.high_score = self.save_data["high_score"]
    
    def add_score(self, popped, floating):
        """
        Calculate and add score for a pop.
        
        Formula: (popped * 10 + floating * 20) * level_multiplier
        Also awards color powers every 2000 pts.
        
        Args:
            popped: Number of bubbles popped directly
            floating: Number that fell after
        """
        base = popped * 10
        bonus = floating * 20
        multiplier = 1 + (self.level - 1) * 0.1
        
        self.score += int((base + bonus) * multiplier)
        
        # check for new high score
        if self.score > self.high_score:
            self.high_score = self.score
            update_high_score(self.save_data, self.score)
        
        # track stats
        add_bubbles_popped(self.save_data, popped + floating)
        
        # earn powers every 2000 pts (max 3)
        while self.score >= self.points_for_next_power and self.color_powers < 3:
            self.color_powers += 1
            self.points_for_next_power += 2000
    
    def next_level(self):
        """
        Move to next level and save progress.
        
        Saves current level score, updates stats,
        then resets score for new level.
        """
        update_level_high_score(self.save_data, self.level, self.score)
        add_level_completed(self.save_data)
        
        if self.score > self.high_score:
            self.high_score = self.score
            update_high_score(self.save_data, self.score)
        
        self.score = 0
        self.level += 1
        self.points_for_next_power = 2000
    
    def reset(self):
        """
        Reset for a new game.
        
        Clears score, level, powers. Increments game counter.
        """
        self.score = 0
        self.level = 1
        self.color_powers = 0
        self.points_for_next_power = 2000
        self.color_mode = False
        self.selected_bubble = None
        
        add_game_played(self.save_data)
    
    def use_color_power(self):
        """
        Use a color power to change bubble color.
        
        Returns:
            True if power was used, False if none available
        """
        if self.color_powers > 0:
            self.color_powers -= 1
            self.color_mode = False
            self.selected_bubble = None
            return True
        return False
    
    def toggle_color_mode(self):
        """Toggle color change mode on/off."""
        if self.color_powers > 0:
            self.color_mode = not self.color_mode
            if not self.color_mode:
                self.selected_bubble = None
        else:
            self.color_mode = False
            self.selected_bubble = None
    
    def select_bubble(self, row, col):
        """
        Select a bubble for color change.
        
        Args:
            row: Row of bubble
            col: Column of bubble
        """
        self.selected_bubble = (row, col)
    
    def cancel_selection(self):
        """Clear current bubble selection."""
        self.selected_bubble = None
    
    def get_stats(self):
        """
        Get stats for display screen.
        
        Returns:
            Dict with high_score, total_bubbles, games_played, etc
        """
        return {
            "high_score": self.save_data["high_score"],
            "total_bubbles": self.save_data["total_bubbles_popped"],
            "games_played": self.save_data["total_games_played"],
            "levels_completed": self.save_data["levels_completed"],
            "level_scores": self.save_data["level_high_scores"]
        }

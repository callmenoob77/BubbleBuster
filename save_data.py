"""
Save/load module for game data persistence.

Handles reading and writing stats, scores and settings to JSON.
"""

import json
import os

SAVE_FILE = "save_data.json"


def get_default_data():
    """
    Get default structure for new save file.
    
    Returns:
        Dict with all default values for stats and settings
    """
    return {
        "high_score": 0,
        "level_high_scores": {},
        "total_bubbles_popped": 0,
        "total_games_played": 0,
        "levels_completed": 0,
        "settings": {
            "volume": 50,
            "large_window": False
        }
    }


def load_data():
    """
    Load saved data from file.
    
    Merges missing keys from defaults so old saves
    still work when we add new features.
    
    Returns:
        Dict with all game data
    """
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
                
                # merge in any missing keys
                defaults = get_default_data()
                for key in defaults:
                    if key not in data:
                        data[key] = defaults[key]
                
                # also check settings subkeys
                for key in defaults["settings"]:
                    if key not in data["settings"]:
                        data["settings"][key] = defaults["settings"][key]
                
                return data
        except:
            return get_default_data()
    
    return get_default_data()


def save_data(data):
    """
    Write game data to file.
    
    Args:
        data: Dict to save
    """
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=2)


def update_high_score(data, score):
    """
    Update high score if new one is better.
    
    Args:
        data: Save data dict
        score: New score
        
    Returns:
        True if we updated it
    """
    if score > data["high_score"]:
        data["high_score"] = score
        save_data(data)
        return True
    return False


def update_level_high_score(data, level, score):
    """
    Update high score for specific level.
    
    Args:
        data: Save data dict
        level: Level number
        score: Score achieved
        
    Returns:
        True if its a new record
    """
    key = str(level)
    if key not in data["level_high_scores"]:
        data["level_high_scores"][key] = 0 # if the level wasnever played, we create it here
    
    if score > data["level_high_scores"][key]:
        data["level_high_scores"][key] = score
        save_data(data)
        return True
    return False


def add_bubbles_popped(data, count):
    """
    Add to lifetime bubbles popped stat.
    
    Args:
        data: Save data dict
        count: Number to add
    """
    data["total_bubbles_popped"] += count
    save_data(data)


def add_game_played(data):
    """
    Increment games played counter.
    
    Args:
        data: Save data dict
    """
    data["total_games_played"] += 1
    save_data(data)


def add_level_completed(data):
    """
    Increment levels completed counter.
    
    Args:
        data: Save data dict
    """
    data["levels_completed"] += 1
    save_data(data)


def get_level_high_score(data, level):
    """
    Get high score for a level.
    
    Args:
        data: Save data dict
        level: Level number
        
    Returns:
        High score, or 0 if not played
    """
    key = str(level)
    return data["level_high_scores"].get(key, 0)

#This file handles saving and loading game data

import json
import os

SAVE_FILE = "save_data.json"

#default data structure
def get_default_data():
    return {
        "high_score": 0,
        "high_run_score": 0,
        "level_high_scores": {},
        "total_bubbles_popped": 0,
        "total_games_played": 0,
        "levels_completed": 0,
        "settings": {
            "music_on": True,
            "volume": 50,
            "large_window": False
        }
    }

#loads saved data from file
def load_data():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
                defaults = get_default_data()
                for key in defaults:
                    if key not in data:
                        data[key] = defaults[key]
                #also merge settings sub-keys
                for setting_key in defaults["settings"]:
                    if setting_key not in data["settings"]:
                        data["settings"][setting_key] = defaults["settings"][setting_key]
                return data
        except:
            return get_default_data()
    return get_default_data()

#saves data to file
def save_data(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=2)

#updates high score if new score is higher
def update_high_score(data, score):
    if score > data["high_score"]:
        data["high_score"] = score
        save_data(data)
        return True
    return False

#updates high run score if new cumulative run score is higher
def update_high_run_score(data, score):
    if "high_run_score" not in data:
        data["high_run_score"] = 0
        
    if score > data["high_run_score"]:
        data["high_run_score"] = score
        save_data(data)
        return True
    return False

#updates level high score
def update_level_high_score(data, level, score):
    level_key = str(level)
    if level_key not in data["level_high_scores"]:
        data["level_high_scores"][level_key] = 0
    
    if score > data["level_high_scores"][level_key]:
        data["level_high_scores"][level_key] = score
        save_data(data)
        return True
    return False

#adds to total bubbles popped
def add_bubbles_popped(data, count):
    data["total_bubbles_popped"] += count
    save_data(data)

#increments games played
def add_game_played(data):
    data["total_games_played"] += 1
    save_data(data)

#increments levels completed
def add_level_completed(data):
    data["levels_completed"] += 1
    save_data(data)

#gets level high score
def get_level_high_score(data, level):
    level_key = str(level)
    return data["level_high_scores"].get(level_key, 0)

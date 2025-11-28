import json
import os
import subprocess
import sys
from typing import Dict, List, Optional

class GameManager:
    def __init__(self):
        self.games_metadata = {}
        self.games_directory = "."  # Current directory where game files are located
        self.load_game_metadata()
    
    def load_game_metadata(self):
        """Load game metadata from JSON file"""
        try:
            # Try different possible paths for the metadata file
            possible_paths = [
                'game_launcher/game_metadata.json',
                'game_metadata.json',
                os.path.join(os.path.dirname(__file__), 'game_metadata.json')
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    with open(path, 'r') as f:
                        self.games_metadata = json.load(f)
                    print(f"Loaded metadata from: {path}")
                    return
            
            print("Warning: game_metadata.json not found in any expected location")
            self.games_metadata = {}
        except Exception as e:
            print(f"Error loading metadata: {e}")
            self.games_metadata = {}
    
    def get_available_games(self) -> List[str]:
        """Get list of available game files"""
        available_games = []
        print(f"Looking for games in directory: {os.path.abspath(self.games_directory)}")
        
        for game_key in self.games_metadata.keys():
            game_file = f"{game_key}.py"
            game_path = os.path.join(self.games_directory, game_file)
            print(f"Checking for: {game_path} - Exists: {os.path.exists(game_path)}")
            if os.path.exists(game_path):
                available_games.append(game_key)
        
        print(f"Found {len(available_games)} available games: {available_games}")
        return available_games
    
    def get_game_info(self, game_key: str) -> Optional[Dict]:
        """Get metadata for a specific game"""
        return self.games_metadata.get(game_key)
    
    def launch_game(self, game_key: str) -> bool:
        """Launch a game by its key"""
        game_file = f"{game_key}.py"
        game_path = os.path.join(self.games_directory, game_file)
        
        if not os.path.exists(game_path):
            print(f"Error: Game file {game_file} not found at {game_path}")
            return False
        
        try:
            # Change to the games directory and run the game
            print(f"Launching game: {game_path}")
            subprocess.run([sys.executable, game_file], cwd=self.games_directory)
            return True
        except Exception as e:
            print(f"Error launching game {game_key}: {e}")
            return False
    
    def get_games_by_category(self) -> Dict[str, List[str]]:
        """Group games by category"""
        categories = {}
        for game_key, game_info in self.games_metadata.items():
            category = game_info.get('category', 'Other')
            if category not in categories:
                categories[category] = []
            categories[category].append(game_key)
        return categories

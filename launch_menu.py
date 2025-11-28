#!/usr/bin/env python3
"""
Python Games Collection Launcher
Simple script to launch the main menu for the pygame collection.
"""

import sys
import os

def main():
    """Launch the main menu"""
    try:
        # Add the game_launcher directory to the Python path
        launcher_dir = os.path.join(os.path.dirname(__file__), 'game_launcher')
        sys.path.insert(0, launcher_dir)
        
        # Import and run the main menu
        from main_menu import main as run_menu
        run_menu()
        
    except ImportError as e:
        print("Error importing main menu: {}".format(e))
        print("Make sure pygame is installed: pip install pygame")
        sys.exit(1)
    except Exception as e:
        print("Error launching menu: {}".format(e))
        sys.exit(1)

if __name__ == "__main__":
    main()

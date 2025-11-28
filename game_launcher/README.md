# Python Games Collection - Main Menu

A GUI launcher for the Python Games collection that provides an easy way to browse, preview, and launch games.

## Features

- **Game Grid Display**: Visual tiles showing all available games
- **Game Preview Panel**: Detailed information about selected games including:
  - Game description
  - Controls information
  - Difficulty level
  - Category classification
- **One-Click Launch**: Easy game launching with automatic return to menu
- **Categorized Games**: Games organized by type (Action, Puzzle, Strategy, etc.)
- **Visual Indicators**: Difficulty levels shown with color-coded dots

## How to Use

### Running the Main Menu

1. **From the root directory**, run:
   ```bash
   python launch_menu.py
   ```

2. **Or from the game_launcher directory**, run:
   ```bash
   python main_menu.py
   ```

### Using the Interface

1. **Browse Games**: Click on any game tile in the left panel to see details
2. **View Details**: Selected game information appears in the right preview panel
3. **Launch Game**: Click the "PLAY GAME" button to start the selected game
4. **Return to Menu**: Close the game window to return to the main menu

### Button Functions

- **PLAY GAME**: Launch the currently selected game
- **SETTINGS**: Configure global game settings (coming soon)
- **HIGH SCORES**: View leaderboards (coming soon)
- **EXIT**: Close the main menu

## Game Categories

- **Action**: Fast-paced games requiring quick reflexes
- **Puzzle**: Logic and problem-solving games
- **Strategy**: Games requiring planning and tactical thinking
- **Memory**: Games that test memory and pattern recognition
- **Creative**: Drawing and creative applications
- **Animation**: Demonstration programs
- **Template**: Starting points for new games

## Difficulty Levels

- 🔵 **Beginner**: Very easy to learn
- 🟢 **Easy**: Simple gameplay mechanics
- 🟡 **Medium**: Moderate challenge
- 🔴 **Hard**: Challenging gameplay

## Technical Details

### File Structure
```
game_launcher/
├── main_menu.py           # Main application
├── game_manager.py        # Game launching and management
├── ui_components.py       # UI widgets and components
├── game_metadata.json     # Game information database
└── README.md             # This file
```

### Requirements
- Python 3.x
- Pygame library (`pip install pygame`)

### Adding New Games

To add a new game to the launcher:

1. Add the game's `.py` file to the root directory
2. Update `game_metadata.json` with the game's information:
   ```json
   "your_game": {
     "name": "Your Game Name",
     "description": "Description of your game",
     "difficulty": "Easy|Medium|Hard|Beginner",
     "controls": "Control instructions",
     "high_score_enabled": true,
     "category": "Action|Puzzle|Strategy|Memory|Creative|Animation|Template"
   }
   ```

### Customization

You can customize the launcher by modifying:
- **Colors**: Edit color constants in `main_menu.py`
- **Layout**: Adjust positioning in the `setup_ui()` method
- **Game Information**: Update `game_metadata.json`
- **Window Size**: Change `WINDOW_WIDTH` and `WINDOW_HEIGHT` in `main_menu.py`

## Future Enhancements

Planned features for future versions:
- Settings panel for global game configuration
- High score tracking and leaderboards
- Game preview screenshots
- Player profiles
- Game filtering and search
- Favorites system
- Recent games list

## Troubleshooting

### Common Issues

1. **"No games available"**: Make sure game files are in the parent directory
2. **Import errors**: Ensure pygame is installed (`pip install pygame`)
3. **Games won't launch**: Check that game files are executable Python scripts
4. **Missing metadata**: Verify `game_metadata.json` contains entries for all games

### Getting Help

If you encounter issues:
1. Check that all required files are present
2. Verify pygame installation
3. Ensure you're running from the correct directory
4. Check console output for error messages

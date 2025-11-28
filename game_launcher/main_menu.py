import pygame
import sys
import os
from game_manager import GameManager
from ui_components import Button, GameTile, GamePreviewPanel

class MainMenu:
    def __init__(self):
        pygame.init()
        
        # Window settings
        self.WINDOW_WIDTH = 1000
        self.WINDOW_HEIGHT = 700
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Python Games Collection")
        
        # Colors
        self.BG_COLOR = (30, 30, 30)
        self.HEADER_COLOR = (20, 20, 20)
        self.TEXT_COLOR = (255, 255, 255)
        self.ACCENT_COLOR = (100, 150, 200)
        
        # Fonts
        self.title_font = pygame.font.Font(None, 48)
        self.header_font = pygame.font.Font(None, 32)
        self.button_font = pygame.font.Font(None, 24)
        self.tile_font = pygame.font.Font(None, 18)
        
        # Game management
        self.game_manager = GameManager()
        self.available_games = self.game_manager.get_available_games()
        
        # UI components
        self.game_tiles = []
        self.buttons = []
        self.preview_panel = None
        self.selected_game = None
        
        # Clock for FPS
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize all UI components"""
        # Header area
        header_height = 80
        
        # Game grid area (left side)
        grid_x = 20
        grid_y = header_height + 20
        grid_width = 400
        grid_height = self.WINDOW_HEIGHT - grid_y - 80
        
        # Preview panel (right side)
        preview_x = grid_x + grid_width + 20
        preview_y = grid_y
        preview_width = self.WINDOW_WIDTH - preview_x - 20
        preview_height = grid_height - 60
        
        # Create preview panel
        self.preview_panel = GamePreviewPanel(preview_x, preview_y, preview_width, preview_height, self.button_font)
        
        # Create game tiles
        self.create_game_tiles(grid_x, grid_y, grid_width, grid_height)
        
        # Create bottom buttons
        self.create_bottom_buttons()
    
    def create_game_tiles(self, start_x, start_y, grid_width, grid_height):
        """Create game tiles in a grid layout"""
        tile_width = 120
        tile_height = 80
        tiles_per_row = grid_width // (tile_width + 10)
        
        x = start_x
        y = start_y
        
        for i, game_key in enumerate(self.available_games):
            game_info = self.game_manager.get_game_info(game_key)
            if game_info:
                tile = GameTile(x, y, tile_width, tile_height, game_key, game_info, self.tile_font)
                self.game_tiles.append(tile)
                
                # Move to next position
                x += tile_width + 10
                if (i + 1) % tiles_per_row == 0:
                    x = start_x
                    y += tile_height + 10
    
    def create_bottom_buttons(self):
        """Create bottom navigation buttons"""
        button_y = self.WINDOW_HEIGHT - 60
        button_width = 120
        button_height = 40
        
        # Play button
        play_button = Button(440, button_y, button_width, button_height, "PLAY GAME", self.button_font, 
                           color=(0, 150, 0), hover_color=(0, 200, 0))
        play_button.set_callback(self.launch_selected_game)
        self.buttons.append(play_button)
        
        # Settings button
        settings_button = Button(580, button_y, button_width, button_height, "SETTINGS", self.button_font)
        settings_button.set_callback(self.show_settings)
        self.buttons.append(settings_button)
        
        # High Scores button
        scores_button = Button(720, button_y, button_width, button_height, "HIGH SCORES", self.button_font)
        scores_button.set_callback(self.show_high_scores)
        self.buttons.append(scores_button)
        
        # Exit button
        exit_button = Button(860, button_y, button_width, button_height, "EXIT", self.button_font,
                           color=(150, 0, 0), hover_color=(200, 0, 0))
        exit_button.set_callback(self.quit_application)
        self.buttons.append(exit_button)
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Handle button events
            for button in self.buttons:
                button.handle_event(event)
            
            # Handle game tile events
            for tile in self.game_tiles:
                if tile.handle_event(event):
                    # Tile was clicked - select it
                    self.select_game(tile.game_key)
                else:
                    tile.handle_event(event)  # For hover effects
    
    def select_game(self, game_key):
        """Select a game and update preview"""
        self.selected_game = game_key
        
        # Update tile selection states
        for tile in self.game_tiles:
            tile.is_selected = (tile.game_key == game_key)
        
        # Update preview panel
        game_info = self.game_manager.get_game_info(game_key)
        if game_info:
            self.preview_panel.set_game(game_key, game_info)
    
    def launch_selected_game(self):
        """Launch the currently selected game"""
        if self.selected_game:
            print(f"Launching game: {self.selected_game}")
            success = self.game_manager.launch_game(self.selected_game)
            if not success:
                print(f"Failed to launch game: {self.selected_game}")
        else:
            print("No game selected")
    
    def show_settings(self):
        """Show settings panel (placeholder)"""
        print("Settings panel - Coming soon!")
    
    def show_high_scores(self):
        """Show high scores panel (placeholder)"""
        print("High scores panel - Coming soon!")
    
    def quit_application(self):
        """Quit the application"""
        self.running = False
    
    def draw_header(self):
        """Draw the header section"""
        header_rect = pygame.Rect(0, 0, self.WINDOW_WIDTH, 80)
        pygame.draw.rect(self.screen, self.HEADER_COLOR, header_rect)
        
        # Title
        title_surface = self.title_font.render("Python Games Collection", True, self.ACCENT_COLOR)
        title_rect = title_surface.get_rect()
        title_rect.x = 20
        title_rect.centery = header_rect.centery
        self.screen.blit(title_surface, title_rect)
        
        # Game count
        count_text = f"{len(self.available_games)} games available"
        count_surface = self.button_font.render(count_text, True, self.TEXT_COLOR)
        count_rect = count_surface.get_rect()
        count_rect.right = self.WINDOW_WIDTH - 20
        count_rect.centery = header_rect.centery
        self.screen.blit(count_surface, count_rect)
    
    def draw(self):
        """Draw all UI elements"""
        # Clear screen
        self.screen.fill(self.BG_COLOR)
        
        # Draw header
        self.draw_header()
        
        # Draw game tiles
        for tile in self.game_tiles:
            tile.draw(self.screen)
        
        # Draw preview panel
        self.preview_panel.draw(self.screen)
        
        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)
        
        # Draw selection instructions
        if not self.selected_game:
            instruction_text = "Click on a game tile to see details and play"
            instruction_surface = self.button_font.render(instruction_text, True, (128, 128, 128))
            instruction_rect = instruction_surface.get_rect()
            instruction_rect.centerx = self.WINDOW_WIDTH // 2
            instruction_rect.y = self.WINDOW_HEIGHT - 100
            self.screen.blit(instruction_surface, instruction_rect)
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()

def main():
    """Entry point"""
    # Change to the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.dirname(script_dir))  # Go to parent directory
    
    menu = MainMenu()
    menu.run()

if __name__ == "__main__":
    main()

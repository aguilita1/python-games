#!/usr/bin/env python3
"""
Create simple preview images for games
This script generates basic placeholder preview images for each game.
"""

import pygame
import os
import json

def create_preview_image(game_key, game_info, size=(200, 120)):
    """Create a simple preview image for a game"""
    pygame.init()
    
    # Create surface
    surface = pygame.Surface(size)
    
    # Color scheme based on category
    category_colors = {
        'Action': (255, 100, 100),      # Red
        'Puzzle': (100, 255, 100),      # Green
        'Strategy': (100, 100, 255),    # Blue
        'Memory': (255, 255, 100),      # Yellow
        'Creative': (255, 100, 255),    # Magenta
        'Animation': (100, 255, 255),   # Cyan
        'Template': (128, 128, 128)     # Gray
    }
    
    category = game_info.get('category', 'Other')
    bg_color = category_colors.get(category, (100, 100, 100))
    
    # Fill background with category color (darker)
    dark_bg = tuple(c // 3 for c in bg_color)
    surface.fill(dark_bg)
    
    # Add gradient effect
    for y in range(size[1]):
        alpha = y / size[1]
        color = tuple(int(dark_bg[i] + (bg_color[i] - dark_bg[i]) * alpha) for i in range(3))
        pygame.draw.line(surface, color, (0, y), (size[0], y))
    
    # Add game name text
    font = pygame.font.Font(None, 24)
    name_surface = font.render(game_info['name'], True, (255, 255, 255))
    name_rect = name_surface.get_rect()
    name_rect.centerx = size[0] // 2
    name_rect.y = 10
    
    # Add shadow
    shadow_surface = font.render(game_info['name'], True, (0, 0, 0))
    surface.blit(shadow_surface, (name_rect.x + 2, name_rect.y + 2))
    surface.blit(name_surface, name_rect)
    
    # Add category text
    small_font = pygame.font.Font(None, 18)
    category_surface = small_font.render(category, True, (200, 200, 200))
    category_rect = category_surface.get_rect()
    category_rect.centerx = size[0] // 2
    category_rect.y = size[1] - 25
    surface.blit(category_surface, category_rect)
    
    # Add difficulty indicator
    difficulty = game_info.get('difficulty', 'Unknown')
    diff_colors = {
        'Easy': (0, 255, 0),
        'Medium': (255, 255, 0),
        'Hard': (255, 0, 0),
        'Beginner': (0, 200, 255)
    }
    diff_color = diff_colors.get(difficulty, (128, 128, 128))
    pygame.draw.circle(surface, diff_color, (size[0] - 20, 20), 8)
    
    return surface

def main():
    """Generate preview images for all games"""
    # Load game metadata
    try:
        with open('game_metadata.json', 'r') as f:
            games_metadata = json.load(f)
    except FileNotFoundError:
        print("Error: game_metadata.json not found")
        return
    
    # Create previews directory
    preview_dir = '../assets/previews'
    os.makedirs(preview_dir, exist_ok=True)
    
    pygame.init()
    
    print("Generating preview images...")
    
    for game_key, game_info in games_metadata.items():
        print("Creating preview for {}...".format(game_info['name']))
        
        # Create preview image
        preview_surface = create_preview_image(game_key, game_info)
        
        # Save image
        filename = "{}_preview.png".format(game_key)
        filepath = os.path.join(preview_dir, filename)
        pygame.image.save(preview_surface, filepath)
        
        print("  Saved: {}".format(filepath))
    
    pygame.quit()
    print("\nGenerated %d preview images in %s" % len(games_metadata), preview_dir)

if __name__ == "__main__":
    main()

import pygame
from typing import Tuple, Callable, Optional

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str, 
                 font: pygame.font.Font, color: Tuple[int, int, int] = (100, 100, 100),
                 text_color: Tuple[int, int, int] = (255, 255, 255),
                 hover_color: Tuple[int, int, int] = (150, 150, 150)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.text_color = text_color
        self.hover_color = hover_color
        self.is_hovered = False
        self.callback = None
    
    def set_callback(self, callback: Callable):
        self.callback = callback
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and self.callback:
                self.callback()
        elif event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
    
    def draw(self, surface: pygame.Surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

class GameTile:
    def __init__(self, x: int, y: int, width: int, height: int, game_key: str, 
                 game_info: dict, font: pygame.font.Font):
        self.rect = pygame.Rect(x, y, width, height)
        self.game_key = game_key
        self.game_info = game_info
        self.font = font
        self.small_font = pygame.font.Font(None, 16)
        self.is_selected = False
        self.is_hovered = False
        
        # Colors
        self.normal_color = (70, 70, 70)
        self.hover_color = (100, 100, 100)
        self.selected_color = (50, 100, 150)
        self.text_color = (255, 255, 255)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True  # Tile was clicked
        return False
    
    def draw(self, surface: pygame.Surface):
        # Determine color based on state
        if self.is_selected:
            color = self.selected_color
        elif self.is_hovered:
            color = self.hover_color
        else:
            color = self.normal_color
        
        # Draw tile background
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        
        # Draw game name (truncate if too long)
        name = self.game_info['name']
        if len(name) > 12:
            name = name[:12] + "..."
        
        name_surface = self.font.render(name, True, self.text_color)
        name_rect = name_surface.get_rect()
        name_rect.centerx = self.rect.centerx
        name_rect.y = self.rect.y + 10
        surface.blit(name_surface, name_rect)
        
        # Draw category
        category = self.game_info.get('category', 'Other')
        category_surface = self.small_font.render(category, True, (200, 200, 200))
        category_rect = category_surface.get_rect()
        category_rect.centerx = self.rect.centerx
        category_rect.y = self.rect.y + self.rect.height - 25
        surface.blit(category_surface, category_rect)
        
        # Draw difficulty indicator
        difficulty = self.game_info.get('difficulty', 'Unknown')
        diff_colors = {
            'Easy': (0, 255, 0),
            'Medium': (255, 255, 0),
            'Hard': (255, 0, 0),
            'Beginner': (0, 200, 255)
        }
        diff_color = diff_colors.get(difficulty, (128, 128, 128))
        pygame.draw.circle(surface, diff_color, 
                         (self.rect.right - 15, self.rect.y + 15), 5)

class GamePreviewPanel:
    def __init__(self, x: int, y: int, width: int, height: int, font: pygame.font.Font):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.title_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 20)
        self.current_game = None
        self.current_game_info = None
        self.preview_image = None
        
        # Colors
        self.bg_color = (50, 50, 50)
        self.text_color = (255, 255, 255)
        self.accent_color = (100, 150, 200)
    
    def set_game(self, game_key: str, game_info: dict):
        self.current_game = game_key
        self.current_game_info = game_info
        self.load_preview_image(game_key)
    
    def load_preview_image(self, game_key: str):
        """Load preview image for the game"""
        try:
            import os
            preview_path = f"assets/previews/{game_key}_preview.png"
            if os.path.exists(preview_path):
                self.preview_image = pygame.image.load(preview_path)
            else:
                self.preview_image = None
        except:
            self.preview_image = None
    
    def draw(self, surface: pygame.Surface):
        # Draw background
        pygame.draw.rect(surface, self.bg_color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        
        if not self.current_game_info:
            # Draw placeholder text
            placeholder_text = "Select a game to see details"
            text_surface = self.font.render(placeholder_text, True, (128, 128, 128))
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)
            return
        
        y_offset = self.rect.y + 20
        
        # Draw game title
        title_surface = self.title_font.render(self.current_game_info['name'], True, self.accent_color)
        surface.blit(title_surface, (self.rect.x + 20, y_offset))
        y_offset += 50
        
        # Draw preview area
        preview_rect = pygame.Rect(self.rect.x + 20, y_offset, 200, 120)
        pygame.draw.rect(surface, (30, 30, 30), preview_rect)
        pygame.draw.rect(surface, (100, 100, 100), preview_rect, 1)
        
        # Draw preview image or placeholder
        if self.preview_image:
            # Scale image to fit preview area
            scaled_image = pygame.transform.scale(self.preview_image, (preview_rect.width - 4, preview_rect.height - 4))
            surface.blit(scaled_image, (preview_rect.x + 2, preview_rect.y + 2))
        else:
            # Preview placeholder text
            preview_text = "Game Preview"
            preview_surface = self.font.render(preview_text, True, (128, 128, 128))
            preview_text_rect = preview_surface.get_rect(center=preview_rect.center)
            surface.blit(preview_surface, preview_text_rect)
        
        # Draw game info to the right of preview
        info_x = preview_rect.right + 20
        
        # Description
        desc_lines = self._wrap_text(self.current_game_info['description'], 
                                   self.rect.width - (info_x - self.rect.x) - 20, self.small_font)
        for i, line in enumerate(desc_lines[:4]):  # Limit to 4 lines
            line_surface = self.small_font.render(line, True, self.text_color)
            surface.blit(line_surface, (info_x, y_offset + i * 25))
        
        y_offset += 130
        
        # Controls
        controls_text = f"Controls: {self.current_game_info.get('controls', 'N/A')}"
        controls_surface = self.small_font.render(controls_text, True, self.text_color)
        surface.blit(controls_surface, (self.rect.x + 20, y_offset))
        y_offset += 30
        
        # Difficulty
        difficulty_text = f"Difficulty: {self.current_game_info.get('difficulty', 'Unknown')}"
        difficulty_surface = self.small_font.render(difficulty_text, True, self.text_color)
        surface.blit(difficulty_surface, (self.rect.x + 20, y_offset))
        y_offset += 30
        
        # Category
        category_text = f"Category: {self.current_game_info.get('category', 'Other')}"
        category_surface = self.small_font.render(category_text, True, self.text_color)
        surface.blit(category_surface, (self.rect.x + 20, y_offset))
    
    def _wrap_text(self, text: str, max_width: int, font: pygame.font.Font):
        """Wrap text to fit within max_width"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines

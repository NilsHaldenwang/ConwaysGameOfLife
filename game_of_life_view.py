"""
Game of Life Visualization Module

This module implements the visualization layer using PyGame. It follows the
Model-View-Controller (MVC) pattern, where this class represents the View.

Plain-language summary for non-programmers:
- The view draws the grid on the screen: each cell becomes a small square of
    pixels. Alive cells are drawn with a bright color, dead cells with a dark color.
- Coordinates: positions on the screen are in pixels. To map a mouse click to a
    grid cell we subtract a horizontal offset (if the grid is centered) and divide
    by the cell size. That gives the row and column in the logical grid.
- PyGame is the library used to create the window, draw shapes, and handle
    keyboard and mouse events.

The visualization is responsible only for rendering the game state and UI elements,
not for game logic or state management.
"""

import pygame
from typing import Tuple, Optional
import numpy as np


class GameOfLifeView:
    """
    PyGame-based visualization for Conway's Game of Life.
    
    This class handles all rendering concerns including the grid display,
    UI buttons, and user interactions. It is completely separated from
    the game logic (Separation of Concerns).
    
    Attributes:
        screen_width (int): Width of the game window in pixels
        screen_height (int): Height of the game window in pixels
        cell_size (int): Size of each cell in pixels
        ui_height (int): Height reserved for UI controls
        screen: PyGame display surface
        clock: PyGame clock for framerate control
        colors (dict): Color scheme for the visualization
    """
    
    # Color scheme constants
    COLORS = {
        'background': (20, 20, 20),      # Dark background
        'grid_line': (50, 50, 50),       # Grid lines
        'dead_cell': (30, 30, 30),       # Dead cells
        'alive_cell': (0, 255, 100),     # Alive cells (bright green)
        'button': (60, 60, 60),          # Button background
        'button_hover': (80, 80, 80),    # Button hover state
        'button_text': (255, 255, 255),  # Button text
        'ui_background': (40, 40, 40),   # UI panel background
    }
    
    def __init__(self, grid_rows: int, grid_cols: int, cell_size: int = 15):
        """
        Initialize the PyGame visualization.
        
        Args:
            grid_rows: Number of rows in the game grid
            grid_cols: Number of columns in the game grid
            cell_size: Size of each cell in pixels (default: 15)
        """
        pygame.init()
        
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.cell_size = cell_size
        self.ui_height = 80  # Height for control buttons
        
        # Button dimensions
        self.button_width = 100
        self.button_height = 40
        self.button_spacing = 10
        self.button_margin = 20  # Left margin for first button
        # Reserve extra horizontal space on the right of the buttons for
        # status / generation labels so they never overlap the buttons.
        # This value is in pixels and should be large enough to hold two
        # lines of small text comfortably.
        self.label_area_width = 180
        
        # Calculate minimum width needed for all buttons plus reserved label area
        # Buttons + spacing + margins + reserved label area
        num_buttons = 6
        base_buttons_width = (num_buttons * self.button_width + 
                      (num_buttons - 1) * self.button_spacing + 
                      2 * self.button_margin)
        self.min_width = base_buttons_width + self.label_area_width
        
        # Calculate actual grid width
        grid_width = grid_cols * cell_size
        
        # Use the larger of grid width or minimum UI width
        self.screen_width = max(grid_width, self.min_width)
        self.screen_height = grid_rows * cell_size + self.ui_height
        
        # Calculate grid offset to center it if screen is wider than grid
        self.grid_offset_x = (self.screen_width - grid_width) // 2
        
        # Create the display window
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Conway's Game of Life - Educational Demo")
        
        # Clock for controlling framerate
        self.clock = pygame.time.Clock()
        
        # Initialize font for UI text
        self.font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 20)
        
        # Create buttons with proper spacing
        button_y = grid_rows * cell_size + 15
        self._create_buttons(button_y)
        
        # Track which button is currently hovered
        self.hovered_button = None
    
    def _create_buttons(self, button_y: int) -> None:
        """
        Create button rectangles with proper layout.
        
        Args:
            button_y: Y-coordinate for the buttons
        """
        x_pos = self.button_margin
        
        self.start_button = pygame.Rect(x_pos, button_y, self.button_width, self.button_height)
        x_pos += self.button_width + self.button_spacing
        
        self.pause_button = pygame.Rect(x_pos, button_y, self.button_width, self.button_height)
        x_pos += self.button_width + self.button_spacing
        
        self.load_button = pygame.Rect(x_pos, button_y, self.button_width, self.button_height)
        x_pos += self.button_width + self.button_spacing
        
        self.clear_button = pygame.Rect(x_pos, button_y, self.button_width, self.button_height)
        x_pos += self.button_width + self.button_spacing

        # Speed button (cycles through preset framerates)
        self.speed_button = pygame.Rect(x_pos, button_y, self.button_width, self.button_height)
        x_pos += self.button_width + self.button_spacing

        # Randomize button: creates a random starting configuration
        self.random_button = pygame.Rect(x_pos, button_y, self.button_width, self.button_height)
    
    def update_grid_dimensions(self, rows: int, cols: int) -> None:
        """
        Update the grid dimensions and resize the window accordingly.
        
        This is called when a new pattern is loaded with different dimensions.
        
        Args:
            rows: New number of rows
            cols: New number of columns
        """
        self.grid_rows = rows
        self.grid_cols = cols
        
        # Calculate actual grid width
        grid_width = cols * self.cell_size
        
        # Use the larger of grid width or minimum UI width
        self.screen_width = max(grid_width, self.min_width)
        self.screen_height = rows * self.cell_size + self.ui_height
        
        # Calculate grid offset to center it if screen is wider than grid
        self.grid_offset_x = (self.screen_width - grid_width) // 2
        
        # Resize the window
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        
        # Recreate buttons with proper positions
        button_y = rows * self.cell_size + 15
        self._create_buttons(button_y)
    
    def draw_grid(self, grid: np.ndarray) -> None:
        """
        Draw the game grid with cells and grid lines.
        
        The grid is centered horizontally if it's narrower than the window.
        
        Args:
            grid: 2D NumPy array representing the current game state
        """
        # Fill background
        grid_surface_height = self.grid_rows * self.cell_size
        pygame.draw.rect(self.screen, self.COLORS['background'], 
                        (0, 0, self.screen_width, grid_surface_height))
        
        # Draw cells (with horizontal offset for centering)
        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                x = self.grid_offset_x + col * self.cell_size
                y = row * self.cell_size
                
                # Choose color based on cell state
                color = self.COLORS['alive_cell'] if grid[row, col] == 1 else self.COLORS['dead_cell']
                
                # Draw the cell
                pygame.draw.rect(self.screen, color, 
                               (x, y, self.cell_size, self.cell_size))
                
                # Draw grid line (border)
                pygame.draw.rect(self.screen, self.COLORS['grid_line'], 
                               (x, y, self.cell_size, self.cell_size), 1)
    
    def draw_button(self, rect: pygame.Rect, text: str, is_active: bool = True) -> None:
        """
        Draw a single UI button.
        
        Args:
            rect: Rectangle defining button position and size
            text: Text to display on the button
            is_active: Whether the button is in active state
        """
        # Determine button color based on hover state
        color = self.COLORS['button_hover'] if rect == self.hovered_button else self.COLORS['button']
        
        # Draw button background
        pygame.draw.rect(self.screen, color, rect, border_radius=5)
        pygame.draw.rect(self.screen, self.COLORS['button_text'], rect, 2, border_radius=5)
        
        # Draw button text (centered)
        text_surface = self.font.render(text, True, self.COLORS['button_text'])
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
    
    def draw_ui(self, is_running: bool, generation: int, fps: int, filename: Optional[str] = None) -> None:
        """
        Draw the UI control panel with buttons and status information.
        
        Args:
            is_running: Whether the simulation is currently running
            generation: Current generation number
            filename: Name of the loaded pattern file (if any)
        """
        # Draw UI background
        ui_y = self.grid_rows * self.cell_size
        pygame.draw.rect(self.screen, self.COLORS['ui_background'], 
                        (0, ui_y, self.screen_width, self.ui_height))
        
        # Draw buttons
        self.draw_button(self.start_button, "Start")
        self.draw_button(self.pause_button, "Pause")
        self.draw_button(self.load_button, "Load")
        self.draw_button(self.clear_button, "Clear")
        # Speed button shows current FPS
        self.draw_button(self.speed_button, f"Speed: {fps}")
        # Randomize starting configuration
        self.draw_button(self.random_button, "Random")
        
        # Draw generation counter and status. Position them on the right side
        # of the UI, but if the button area reaches that region, shift the text
        # to the right of the buttons to avoid overlapping. We clamp the final
        # x coordinate to stay within the window.
        gen_text = f"Generation: {generation}"
        gen_surface = self.small_font.render(gen_text, True, self.COLORS['button_text'])

        # Determine a safe x position that does not overlap the rightmost button
        buttons_right = getattr(self, 'random_button', getattr(self, 'speed_button', None)).right
        preferred_x = self.screen_width - 150
        safe_x = max(preferred_x, buttons_right + 10)
        # Clamp so text remains visible
        safe_x = min(safe_x, self.screen_width - 150)

        self.screen.blit(gen_surface, (safe_x, ui_y + 10))

        # Draw running status below generation
        status_text = "Running" if is_running else "Paused"
        status_surface = self.small_font.render(status_text, True, self.COLORS['button_text'])
        self.screen.blit(status_surface, (safe_x, ui_y + 35))

        # Draw loaded filename if available (left side)
        if filename:
            file_text = f"Pattern: {filename}"
            file_surface = self.small_font.render(file_text, True, self.COLORS['button_text'])
            self.screen.blit(file_surface, (20, ui_y + 60))

        # FPS is shown on the Speed button; no separate FPS label here to avoid
        # duplicate information and possible overlap.
    
    def render(self, grid: np.ndarray, is_running: bool, generation: int, 
               fps: int, filename: Optional[str] = None) -> None:
        """
        Render the complete frame including grid and UI.
        
        This is the main rendering method that should be called each frame.
        
        Args:
            grid: Current game state
            is_running: Whether simulation is running
            generation: Current generation number
            filename: Loaded pattern filename (optional)
        """
        self.draw_grid(grid)
        self.draw_ui(is_running, generation, fps, filename)
        pygame.display.flip()
    
    def update_hover_state(self, mouse_pos: Tuple[int, int]) -> None:
        """
        Update which button is currently being hovered over.
        
        Args:
            mouse_pos: Current mouse position (x, y)
        """
        buttons = [self.start_button, self.pause_button, self.load_button, self.clear_button]
        self.hovered_button = None
        
        for button in buttons:
            if button.collidepoint(mouse_pos):
                self.hovered_button = button
                break
    
    def get_clicked_button(self, mouse_pos: Tuple[int, int]) -> Optional[str]:
        """
        Determine which button was clicked based on mouse position.
        
        Args:
            mouse_pos: Position where mouse was clicked
            
        Returns:
            String identifier of clicked button or None
        """
        if self.start_button.collidepoint(mouse_pos):
            return "start"
        elif self.pause_button.collidepoint(mouse_pos):
            return "pause"
        elif self.load_button.collidepoint(mouse_pos):
            return "load"
        elif self.clear_button.collidepoint(mouse_pos):
            return "clear"
        elif hasattr(self, 'speed_button') and self.speed_button.collidepoint(mouse_pos):
            return "speed"
        elif hasattr(self, 'random_button') and self.random_button.collidepoint(mouse_pos):
            return "random"
        return None
    
    def get_clicked_cell(self, mouse_pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
        Convert mouse click position to grid cell coordinates.
        
        This allows users to toggle cells by clicking on them.
        Accounts for grid centering when window is wider than grid.
        
        Args:
            mouse_pos: Position where mouse was clicked
            
        Returns:
            Tuple of (row, col) or None if clicked outside grid
        """
        x, y = mouse_pos
        
        # Check if click is within grid area (vertically)
        grid_height = self.grid_rows * self.cell_size
        if y < 0 or y >= grid_height:
            return None
        
        # Account for horizontal grid offset (centering)
        # Explanation: if the window is wider than the grid, the grid is
        # centered and `grid_offset_x` holds how many pixels are left of the
        # grid. We subtract this offset before converting pixels to cell index.
        x_relative = x - self.grid_offset_x
        
        # Check if click is within grid area (horizontally)
        grid_width = self.grid_cols * self.cell_size
        if x_relative < 0 or x_relative >= grid_width:
            return None
        
        # Convert to grid coordinates
        col = x_relative // self.cell_size
        row = y // self.cell_size
        
        return (row, col)
    
    def tick(self, fps: int = 10) -> None:
        """
        Control the framerate of the visualization.
        
        Args:
            fps: Target frames per second
        """
        self.clock.tick(fps)
    
    def cleanup(self) -> None:
        """
        Clean up PyGame resources.
        
        Should be called when the application is closing.
        """
        pygame.quit()

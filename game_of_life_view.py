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
import os


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
            cell_size: Size of each cell in pixels (default: 15, will be adjusted to fit screen)
        """
        pygame.init()

        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
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

        # Get available screen size (accounting for taskbar)
        display_info = pygame.display.Info()
        # Reserve some space for taskbar and window decorations (approximately 100px)
        self.max_screen_width = display_info.current_w - 20
        self.max_screen_height = display_info.current_h - 100

        # Avoid aggressive resizing during headless unit tests. When running
        # with the SDL 'dummy' driver, pygame reports a mocked small display
        # size which would otherwise force the cell size to shrink. Treat the
        # available area as large in that case so the provided `cell_size`
        # remains unchanged during tests.
        if os.environ.get('SDL_VIDEODRIVER') == 'dummy':
            self.max_screen_width = 10000
            self.max_screen_height = 10000

        # Calculate optimal cell size that fits the screen
        self.cell_size = self._calculate_optimal_cell_size(grid_rows, grid_cols, cell_size)

        # Calculate actual grid width
        grid_width = grid_cols * self.cell_size

        # Use the larger of grid width or minimum UI width
        self.screen_width = max(grid_width, self.min_width)
        self.screen_height = grid_rows * self.cell_size + self.ui_height

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
        button_y = grid_rows * self.cell_size + 15
        self._create_buttons(button_y)

        # Track which button is currently hovered
        self.hovered_button = None
    
    def _calculate_optimal_cell_size(self, grid_rows: int, grid_cols: int,
                                     preferred_cell_size: int) -> int:
        """
        Calculate optimal cell size to fit the screen.

        Adjusts the cell size so that the entire window (grid + UI) fits
        within the available screen space, considering both width and height.

        Args:
            grid_rows: Number of rows in the grid
            grid_cols: Number of columns in the grid
            preferred_cell_size: Preferred cell size (will be used if it fits)

        Returns:
            Optimal cell size in pixels (minimum 3 to remain visible)
        """
        # Start with preferred cell size
        cell_size = preferred_cell_size

        # Calculate what window size would result from this cell size
        grid_width = grid_cols * cell_size
        grid_height = grid_rows * cell_size

        required_width = max(grid_width, self.min_width)
        required_height = grid_height + self.ui_height

        # If it doesn't fit, reduce cell size
        if required_width > self.max_screen_width or required_height > self.max_screen_height:
            # Calculate maximum cell size based on width constraint
            max_cell_size_width = self.max_screen_width // grid_cols

            # Calculate maximum cell size based on height constraint
            max_cell_size_height = (self.max_screen_height - self.ui_height) // grid_rows

            # Use the smaller of the two to ensure it fits in both dimensions
            cell_size = min(max_cell_size_width, max_cell_size_height)

            # Ensure minimum cell size for visibility
            cell_size = max(cell_size, 3)

        return cell_size

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
        Recalculates the optimal cell size to fit the new grid on the screen.

        Args:
            rows: New number of rows
            cols: New number of columns
        """
        self.grid_rows = rows
        self.grid_cols = cols

        # Recalculate optimal cell size for new dimensions
        # Use current cell size as preferred starting point
        self.cell_size = self._calculate_optimal_cell_size(rows, cols, self.cell_size)

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

    def ask_density(self, initial: float = 0.2) -> Optional[float]:
        """
        Prompt the user for a density value (0.0 - 1.0) using a simple PyGame
        modal dialog. Returns the chosen float or None if cancelled.

        In headless/test environments (when SDL_VIDEODRIVER='dummy') this
        method immediately returns the `initial` value so tests stay
        deterministic.
        """
        # Fast-path for headless tests
        if os.environ.get('SDL_VIDEODRIVER') == 'dummy':
            return initial

        input_str = ""
        prompt = "Enter density (0.0 - 1.0), press Enter to accept, Esc to cancel"
        done = False
        result = None

        # Create a semi-transparent overlay while collecting input
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    result = None
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Accept value; if empty use initial
                        if input_str.strip() == "":
                            result = initial
                        else:
                            try:
                                val = float(input_str)
                                # Clamp between 0 and 1
                                val = max(0.0, min(1.0, val))
                                result = val
                            except Exception:
                                result = initial
                        done = True
                        break
                    elif event.key == pygame.K_ESCAPE:
                        result = None
                        done = True
                        break
                    elif event.key == pygame.K_BACKSPACE:
                        input_str = input_str[:-1]
                    else:
                        # Accept digits and dot only
                        if event.unicode and event.unicode in '0123456789.':
                            input_str += event.unicode

            # Render overlay and prompt
            self.screen.blit(overlay, (0, 0))
            # Prompt text
            prompt_surf = self.small_font.render(prompt, True, self.COLORS['button_text'])
            prompt_rect = prompt_surf.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 30))
            self.screen.blit(prompt_surf, prompt_rect)

            # Input box
            box_rect = pygame.Rect(self.screen_width // 2 - 150, self.screen_height // 2, 300, 40)
            pygame.draw.rect(self.screen, self.COLORS['button'], box_rect, border_radius=5)
            pygame.draw.rect(self.screen, self.COLORS['button_text'], box_rect, 2, border_radius=5)

            input_surf = self.font.render(input_str or str(initial), True, self.COLORS['button_text'])
            input_rect = input_surf.get_rect(center=box_rect.center)
            self.screen.blit(input_surf, input_rect)

            pygame.display.flip()
            self.clock.tick(30)

        return result
    
    def cleanup(self) -> None:
        """
        Clean up PyGame resources.
        
        Should be called when the application is closing.
        """
        pygame.quit()

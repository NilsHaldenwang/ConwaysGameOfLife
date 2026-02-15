"""
Game of Life Controller Module

This module implements the controller logic that coordinates between the game engine
(Model) and the visualization (View). It follows the Model-View-Controller (MVC)
pattern, where this class represents the Controller.

Plain-language summary for non-programmers:
- The controller is the program's coordinator: it listens for mouse and keyboard
    events, tells the model (engine) when to update the simulation, and asks the
    view to redraw the screen.
- The controller runs a simple loop (the "event loop") that repeats: process
    events → update model → render → wait a short time. This loop runs until the
    user closes the window.

The controller handles user input, manages application state, and orchestrates
the interaction between the model and view components.
"""

import pygame
import os
from tkinter import Tk, filedialog
from typing import Optional
from game_of_life_engine import GameOfLifeEngine
from game_of_life_view import GameOfLifeView


class GameOfLifeController:
    """
    Controller for Conway's Game of Life application.
    
    This class coordinates between the game engine (model) and the visualization (view).
    It handles user input, manages simulation state, and updates both model and view
    accordingly.
    
    Attributes:
        engine: The game logic engine (Model)
        view: The visualization component (View)
        is_running: Whether the simulation is currently running
        generation: Current generation counter
        loaded_filename: Name of the currently loaded pattern file
        target_fps: Target simulation speed in steps per second
    """
    
    def __init__(self, initial_rows: int = 50, initial_cols: int = 50, cell_size: int = 15):
        """
        Initialize the Game of Life controller with model and view components.
        
        Args:
            initial_rows: Initial number of grid rows
            initial_cols: Initial number of grid columns
            cell_size: Size of each cell in pixels for visualization
        """
        # Initialize the model (game engine)
        self.engine = GameOfLifeEngine(initial_rows, initial_cols)
        
        # Initialize the view (visualization)
        self.view = GameOfLifeView(initial_rows, initial_cols, cell_size)
        
        # Simulation state
        self.is_running = False
        self.generation = 0
        self.loaded_filename = None
        
        # Simulation speed (steps per second)
        self.target_fps = 10
    
    def handle_events(self) -> bool:
        """
        Process all PyGame events (user input).
        
        Returns:
            False if the application should quit, True otherwise
        """
        for event in pygame.event.get():
            # Handle window close event
            if event.type == pygame.QUIT:
                return False
            
            # Handle mouse motion for button hover effects
            elif event.type == pygame.MOUSEMOTION:
                self.view.update_hover_state(event.pos)
            
            # Handle mouse clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self._handle_mouse_click(event.pos)
            
            # Handle keyboard shortcuts
            elif event.type == pygame.KEYDOWN:
                self._handle_keyboard_input(event.key)
        
        return True
    
    def _handle_mouse_click(self, pos: tuple) -> None:
        """
        Handle mouse click events on buttons or grid cells.
        
        Args:
            pos: Mouse position (x, y) where click occurred
        """
        # Check if a button was clicked
        clicked_button = self.view.get_clicked_button(pos)
        
        if clicked_button == "start":
            self.start_simulation()
        elif clicked_button == "pause":
            self.pause_simulation()
        elif clicked_button == "load":
            self.load_pattern()
        elif clicked_button == "clear":
            self.clear_grid()
        else:
            # If no button was clicked, check if a cell was clicked
            cell_coords = self.view.get_clicked_cell(pos)
            if cell_coords and not self.is_running:
                # Allow manual cell toggling when simulation is paused
                self._toggle_cell(cell_coords)
    
    def _toggle_cell(self, coords: tuple) -> None:
        """
        Toggle the state of a cell (alive <-> dead).
        
        Args:
            coords: Tuple of (row, col) coordinates
        """
        row, col = coords
        current_state = self.engine.get_cell(row, col)
        new_state = 1 if current_state == 0 else 0
        self.engine.set_cell(row, col, new_state)
    
    def _handle_keyboard_input(self, key: int) -> None:
        """
        Handle keyboard shortcuts for common operations.
        
        Args:
            key: PyGame key constant
        """
        if key == pygame.K_SPACE:
            # Space bar toggles simulation state
            if self.is_running:
                self.pause_simulation()
            else:
                self.start_simulation()
        elif key == pygame.K_c:
            # 'C' key clears the grid
            self.clear_grid()
        elif key == pygame.K_l:
            # 'L' key opens load dialog
            self.load_pattern()
        elif key == pygame.K_ESCAPE:
            # ESC key pauses simulation
            self.pause_simulation()
    
    def start_simulation(self) -> None:
        """
        Start or resume the simulation.
        """
        self.is_running = True
    
    def pause_simulation(self) -> None:
        """
        Pause the simulation.
        """
        self.is_running = False
    
    def clear_grid(self) -> None:
        """
        Clear the grid and reset generation counter.
        """
        self.engine.clear()
        self.generation = 0
        self.is_running = False
    
    def load_pattern(self) -> None:
        """
        Open a file dialog to load a pattern from disk.
        
        Pauses the simulation and resets the generation counter.
        """
        # Pause simulation during file loading
        self.pause_simulation()
        
        # Hide PyGame window temporarily and show file dialog
        # Use tkinter for file dialog (cross-platform)
        root = Tk()
        root.withdraw()  # Hide the main tkinter window
        root.attributes('-topmost', True)  # Bring dialog to front
        
        # Open file dialog
        filename = filedialog.askopenfilename(
            title="Select a Game of Life pattern file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        root.destroy()
        
        # Load the pattern if a file was selected
        if filename:
            try:
                self.engine.load_pattern_from_file(filename)
                
                # Update view dimensions if grid size changed
                rows, cols = self.engine.get_dimensions()
                self.view.update_grid_dimensions(rows, cols)
                
                # Reset generation counter
                self.generation = 0
                
                # Store filename for display
                self.loaded_filename = os.path.basename(filename)
                
                print(f"Successfully loaded pattern: {self.loaded_filename}")
                
            except Exception as e:
                print(f"Error loading pattern: {e}")
                self.loaded_filename = None
    
    def update(self) -> None:
        """
        Update the simulation by one step if it's running.
        
        This method should be called once per frame.
        """
        if self.is_running:
            self.engine.step()
            self.generation += 1
    
    def render(self) -> None:
        """
        Render the current state using the view.
        
        This method should be called once per frame.
        """
        grid = self.engine.get_grid_copy()
        self.view.render(grid, self.is_running, self.generation, self.loaded_filename)
    
    def run(self) -> None:
        """
        Main application loop.
        
        This method runs the game loop, processing events, updating the simulation,
        and rendering frames until the user quits.
        """
        # `running` controls the main loop. It will become False when the user
        # requests to quit (for example by closing the window).
        running = True
        
        print("Conway's Game of Life - Educational Demo")
        print("=" * 50)
        print("Controls:")
        print("  - Start/Pause buttons: Control simulation")
        print("  - Load button: Load pattern from file")
        print("  - Clear button: Clear the grid")
        print("  - Click cells: Toggle cell state (when paused)")
        print("  - SPACE: Toggle simulation")
        print("  - C: Clear grid")
        print("  - L: Load pattern")
        print("  - ESC: Pause simulation")
        print("=" * 50)
        
        # Main event loop: repeat until running is False
        while running:
            # Process user input (keyboard / mouse / window events)
            running = self.handle_events()

            # Advance simulation if it's running
            self.update()

            # Render current state to the window
            self.render()

            # Wait to enforce the target frames-per-second / simulation speed
            self.view.tick(self.target_fps)
        
        # Cleanup when application closes
        self.view.cleanup()
        print("Application closed. Thank you!")
    
    def set_simulation_speed(self, fps: int) -> None:
        """
        Set the simulation speed (generations per second).
        
        Args:
            fps: Target generations per second (must be positive)
        """
        if fps > 0:
            self.target_fps = fps

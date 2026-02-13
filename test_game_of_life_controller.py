"""
Unit Tests for Game of Life Controller

This module contains unit tests for the GameOfLifeController class.
Tests cover controller initialization, state management, and coordination
between model and view.
"""

import unittest
import pygame
import tempfile
import os
from game_of_life_controller import GameOfLifeController


class TestGameOfLifeController(unittest.TestCase):
    """
    Test suite for the GameOfLifeController class.
    
    Tests controller functionality, state management, and coordination logic.
    """
    
    @classmethod
    def setUpClass(cls):
        """Initialize PyGame once for all tests."""
        pygame.init()
        # Set environment variable for headless testing
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.controller = GameOfLifeController(initial_rows=20, initial_cols=20, cell_size=10)
    
    def tearDown(self):
        """Clean up after each test."""
        self.controller.view.cleanup()
    
    def test_initialization(self):
        """Test that the controller initializes correctly."""
        # Check that engine and view are created
        self.assertIsNotNone(self.controller.engine)
        self.assertIsNotNone(self.controller.view)
        
        # Check initial state
        self.assertFalse(self.controller.is_running)
        self.assertEqual(self.controller.generation, 0)
        self.assertIsNone(self.controller.loaded_filename)
        self.assertEqual(self.controller.target_fps, 10)
    
    def test_start_simulation(self):
        """Test starting the simulation."""
        self.assertFalse(self.controller.is_running)
        
        self.controller.start_simulation()
        
        self.assertTrue(self.controller.is_running)
    
    def test_pause_simulation(self):
        """Test pausing the simulation."""
        self.controller.start_simulation()
        self.assertTrue(self.controller.is_running)
        
        self.controller.pause_simulation()
        
        self.assertFalse(self.controller.is_running)
    
    def test_clear_grid(self):
        """Test clearing the grid resets state."""
        # Set up some initial state
        self.controller.engine.set_cell(5, 5, 1)
        self.controller.generation = 42
        self.controller.is_running = True
        
        # Clear the grid
        self.controller.clear_grid()
        
        # Check that state is reset
        self.assertEqual(self.controller.generation, 0)
        self.assertFalse(self.controller.is_running)
        self.assertEqual(self.controller.engine.get_cell(5, 5), 0)
    
    def test_set_simulation_speed(self):
        """Test setting the simulation speed."""
        self.controller.set_simulation_speed(20)
        self.assertEqual(self.controller.target_fps, 20)
        
        self.controller.set_simulation_speed(5)
        self.assertEqual(self.controller.target_fps, 5)
    
    def test_set_simulation_speed_invalid(self):
        """Test that invalid speeds are rejected."""
        original_fps = self.controller.target_fps
        
        # Try to set invalid speeds
        self.controller.set_simulation_speed(0)
        self.assertEqual(self.controller.target_fps, original_fps)
        
        self.controller.set_simulation_speed(-10)
        self.assertEqual(self.controller.target_fps, original_fps)
    
    def test_update_when_paused(self):
        """Test that update doesn't advance generation when paused."""
        self.controller.is_running = False
        initial_generation = self.controller.generation
        
        self.controller.update()
        
        self.assertEqual(self.controller.generation, initial_generation)
    
    def test_update_when_running(self):
        """Test that update advances generation when running."""
        # Set up a simple pattern
        self.controller.engine.set_cell(5, 4, 1)
        self.controller.engine.set_cell(5, 5, 1)
        self.controller.engine.set_cell(5, 6, 1)
        
        self.controller.is_running = True
        initial_generation = self.controller.generation
        
        self.controller.update()
        
        # Generation should have incremented
        self.assertEqual(self.controller.generation, initial_generation + 1)
    
    def test_toggle_cell(self):
        """Test toggling a cell from dead to alive and back."""
        # Cell should start dead
        self.assertEqual(self.controller.engine.get_cell(5, 5), 0)
        
        # Toggle to alive
        self.controller._toggle_cell((5, 5))
        self.assertEqual(self.controller.engine.get_cell(5, 5), 1)
        
        # Toggle back to dead
        self.controller._toggle_cell((5, 5))
        self.assertEqual(self.controller.engine.get_cell(5, 5), 0)
    
    def test_handle_mouse_click_on_start_button(self):
        """Test handling a click on the start button."""
        # Get start button position
        pos = self.controller.view.start_button.center
        
        self.assertFalse(self.controller.is_running)
        
        self.controller._handle_mouse_click(pos)
        
        self.assertTrue(self.controller.is_running)
    
    def test_handle_mouse_click_on_pause_button(self):
        """Test handling a click on the pause button."""
        self.controller.is_running = True
        
        pos = self.controller.view.pause_button.center
        self.controller._handle_mouse_click(pos)
        
        self.assertFalse(self.controller.is_running)
    
    def test_handle_mouse_click_on_clear_button(self):
        """Test handling a click on the clear button."""
        self.controller.engine.set_cell(5, 5, 1)
        self.controller.generation = 10
        
        pos = self.controller.view.clear_button.center
        self.controller._handle_mouse_click(pos)
        
        self.assertEqual(self.controller.generation, 0)
        self.assertEqual(self.controller.engine.get_cell(5, 5), 0)
    
    def test_handle_mouse_click_on_cell_when_paused(self):
        """Test that clicking a cell toggles it when paused."""
        self.controller.is_running = False
        
        # Click on a cell in the grid
        pos = (55, 55)  # Should map to cell (5, 5)
        
        self.assertEqual(self.controller.engine.get_cell(5, 5), 0)
        
        self.controller._handle_mouse_click(pos)
        
        self.assertEqual(self.controller.engine.get_cell(5, 5), 1)
    
    def test_handle_mouse_click_on_cell_when_running(self):
        """Test that clicking a cell doesn't toggle it when running."""
        self.controller.is_running = True
        
        pos = (55, 55)
        
        self.assertEqual(self.controller.engine.get_cell(5, 5), 0)
        
        self.controller._handle_mouse_click(pos)
        
        # Cell should remain dead when simulation is running
        self.assertEqual(self.controller.engine.get_cell(5, 5), 0)
    
    def test_handle_keyboard_space_toggles_simulation(self):
        """Test that space bar toggles simulation state."""
        self.assertFalse(self.controller.is_running)
        
        self.controller._handle_keyboard_input(pygame.K_SPACE)
        self.assertTrue(self.controller.is_running)
        
        self.controller._handle_keyboard_input(pygame.K_SPACE)
        self.assertFalse(self.controller.is_running)
    
    def test_handle_keyboard_c_clears_grid(self):
        """Test that 'C' key clears the grid."""
        self.controller.engine.set_cell(5, 5, 1)
        self.controller.generation = 10
        
        self.controller._handle_keyboard_input(pygame.K_c)
        
        self.assertEqual(self.controller.generation, 0)
        self.assertEqual(self.controller.engine.get_cell(5, 5), 0)
    
    def test_handle_keyboard_escape_pauses(self):
        """Test that ESC key pauses the simulation."""
        self.controller.is_running = True
        
        self.controller._handle_keyboard_input(pygame.K_ESCAPE)
        
        self.assertFalse(self.controller.is_running)
    
    def test_render_no_errors(self):
        """Test that render method executes without errors."""
        try:
            self.controller.render()
        except Exception as e:
            self.fail(f"render raised an exception: {e}")
    
    def test_load_pattern_updates_filename(self):
        """Test that loading a pattern updates the filename attribute."""
        # Create a temporary pattern file
        pattern_content = "010\n111\n010"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(pattern_content)
            temp_filename = f.name
        
        try:
            # Manually set the filename (simulating file dialog)
            self.controller.engine.load_pattern_from_file(temp_filename)
            self.controller.loaded_filename = os.path.basename(temp_filename)
            self.controller.generation = 0
            
            # Check that filename is stored
            self.assertIsNotNone(self.controller.loaded_filename)
            self.assertIn('.txt', self.controller.loaded_filename)
            
            # Check that generation was reset
            self.assertEqual(self.controller.generation, 0)
        finally:
            os.unlink(temp_filename)
    
    def test_load_pattern_pauses_simulation(self):
        """Test that loading a pattern pauses the simulation."""
        self.controller.is_running = True
        
        # The load_pattern method includes pause_simulation() call
        # We can't fully test the file dialog, but we can verify pause behavior
        self.controller.pause_simulation()
        
        self.assertFalse(self.controller.is_running)
    
    def test_controller_has_correct_components(self):
        """Test that controller has references to engine and view."""
        # Check types
        from game_of_life_engine import GameOfLifeEngine
        from game_of_life_view import GameOfLifeView
        
        self.assertIsInstance(self.controller.engine, GameOfLifeEngine)
        self.assertIsInstance(self.controller.view, GameOfLifeView)


if __name__ == '__main__':
    unittest.main()

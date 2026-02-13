"""
Unit Tests for Game of Life View

This module contains unit tests for the GameOfLifeView class.
Tests cover initialization, rendering components, and user interaction detection.
"""

import unittest
import pygame
import numpy as np
from game_of_life_view import GameOfLifeView


class TestGameOfLifeView(unittest.TestCase):
    """
    Test suite for the GameOfLifeView class.
    
    Tests visualization components, button interactions, and rendering logic.
    Note: These tests run in a headless mode for automated testing.
    """
    
    @classmethod
    def setUpClass(cls):
        """Initialize PyGame once for all tests."""
        pygame.init()
        # Set environment variable for headless testing
        import os
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.view = GameOfLifeView(20, 20, cell_size=10)
    
    def tearDown(self):
        """Clean up after each test."""
        self.view.cleanup()
    
    def test_initialization(self):
        """Test that the view initializes with correct dimensions."""
        self.assertEqual(self.view.grid_rows, 20)
        self.assertEqual(self.view.grid_cols, 20)
        self.assertEqual(self.view.cell_size, 10)
        
        # Check calculated dimensions
        expected_width = 20 * 10  # cols * cell_size
        expected_height = 20 * 10 + 80  # rows * cell_size + ui_height
        
        self.assertEqual(self.view.screen_width, expected_width)
        self.assertEqual(self.view.screen_height, expected_height)
    
    def test_initialization_custom_cell_size(self):
        """Test initialization with custom cell size."""
        view = GameOfLifeView(30, 30, cell_size=15)
        
        self.assertEqual(view.grid_rows, 30)
        self.assertEqual(view.grid_cols, 30)
        self.assertEqual(view.cell_size, 15)
        
        expected_width = 30 * 15
        expected_height = 30 * 15 + 80
        
        self.assertEqual(view.screen_width, expected_width)
        self.assertEqual(view.screen_height, expected_height)
        
        view.cleanup()
    
    def test_update_grid_dimensions(self):
        """Test updating grid dimensions resizes the window."""
        # Update to new dimensions
        self.view.update_grid_dimensions(40, 40)
        
        self.assertEqual(self.view.grid_rows, 40)
        self.assertEqual(self.view.grid_cols, 40)
        
        # Check recalculated dimensions
        expected_width = 40 * 10
        expected_height = 40 * 10 + 80
        
        self.assertEqual(self.view.screen_width, expected_width)
        self.assertEqual(self.view.screen_height, expected_height)
    
    def test_button_rectangles_exist(self):
        """Test that all button rectangles are created."""
        self.assertIsInstance(self.view.start_button, pygame.Rect)
        self.assertIsInstance(self.view.pause_button, pygame.Rect)
        self.assertIsInstance(self.view.load_button, pygame.Rect)
        self.assertIsInstance(self.view.clear_button, pygame.Rect)
    
    def test_get_clicked_button_start(self):
        """Test detecting clicks on the start button."""
        # Get the center of the start button
        pos = self.view.start_button.center
        
        clicked = self.view.get_clicked_button(pos)
        self.assertEqual(clicked, "start")
    
    def test_get_clicked_button_pause(self):
        """Test detecting clicks on the pause button."""
        pos = self.view.pause_button.center
        
        clicked = self.view.get_clicked_button(pos)
        self.assertEqual(clicked, "pause")
    
    def test_get_clicked_button_load(self):
        """Test detecting clicks on the load button."""
        pos = self.view.load_button.center
        
        clicked = self.view.get_clicked_button(pos)
        self.assertEqual(clicked, "load")
    
    def test_get_clicked_button_clear(self):
        """Test detecting clicks on the clear button."""
        pos = self.view.clear_button.center
        
        clicked = self.view.get_clicked_button(pos)
        self.assertEqual(clicked, "clear")
    
    def test_get_clicked_button_none(self):
        """Test that clicking outside buttons returns None."""
        # Click at position (0, 0) which should be in the grid area
        clicked = self.view.get_clicked_button((0, 0))
        self.assertIsNone(clicked)
    
    def test_get_clicked_cell_valid(self):
        """Test converting mouse click to grid coordinates."""
        # Click at position (55, 55) with cell_size=10
        # Should map to cell (5, 5)
        cell = self.view.get_clicked_cell((55, 55))
        
        self.assertIsNotNone(cell)
        self.assertEqual(cell, (5, 5))
    
    def test_get_clicked_cell_top_left(self):
        """Test clicking on the top-left cell."""
        cell = self.view.get_clicked_cell((0, 0))
        
        self.assertIsNotNone(cell)
        self.assertEqual(cell, (0, 0))
    
    def test_get_clicked_cell_bottom_right(self):
        """Test clicking on the bottom-right cell."""
        # Last cell is at (19, 19) for a 20x20 grid
        # With cell_size=10, this is at position (190-199, 190-199)
        cell = self.view.get_clicked_cell((195, 195))
        
        self.assertIsNotNone(cell)
        self.assertEqual(cell, (19, 19))
    
    def test_get_clicked_cell_outside_grid(self):
        """Test that clicking outside the grid returns None."""
        # Click in the UI area (below the grid)
        grid_height = 20 * 10  # rows * cell_size = 200
        cell = self.view.get_clicked_cell((10, grid_height + 10))
        
        self.assertIsNone(cell)
    
    def test_get_clicked_cell_negative_coordinates(self):
        """Test that negative coordinates return None."""
        cell = self.view.get_clicked_cell((-10, 10))
        self.assertIsNone(cell)
        
        cell = self.view.get_clicked_cell((10, -10))
        self.assertIsNone(cell)
    
    def test_update_hover_state_start_button(self):
        """Test hover state detection for start button."""
        # Hover over start button
        pos = self.view.start_button.center
        self.view.update_hover_state(pos)
        
        self.assertEqual(self.view.hovered_button, self.view.start_button)
    
    def test_update_hover_state_no_button(self):
        """Test hover state when not over any button."""
        # Position not over any button
        self.view.update_hover_state((0, 0))
        
        self.assertIsNone(self.view.hovered_button)
    
    def test_draw_grid_no_errors(self):
        """Test that drawing the grid doesn't raise errors."""
        # Create a sample grid
        grid = np.zeros((20, 20), dtype=np.int8)
        grid[5, 5] = 1
        grid[10, 10] = 1
        
        # Should not raise an exception
        try:
            self.view.draw_grid(grid)
        except Exception as e:
            self.fail(f"draw_grid raised an exception: {e}")
    
    def test_draw_ui_no_errors(self):
        """Test that drawing the UI doesn't raise errors."""
        # Should not raise an exception
        try:
            self.view.draw_ui(is_running=True, generation=42, filename="test.txt")
            self.view.draw_ui(is_running=False, generation=0, filename=None)
        except Exception as e:
            self.fail(f"draw_ui raised an exception: {e}")
    
    def test_draw_button_no_errors(self):
        """Test that drawing buttons doesn't raise errors."""
        # Should not raise an exception
        try:
            self.view.draw_button(self.view.start_button, "Test", is_active=True)
        except Exception as e:
            self.fail(f"draw_button raised an exception: {e}")
    
    def test_render_no_errors(self):
        """Test that the main render method doesn't raise errors."""
        grid = np.zeros((20, 20), dtype=np.int8)
        
        # Should not raise an exception
        try:
            self.view.render(grid, is_running=True, generation=10, filename="test.txt")
        except Exception as e:
            self.fail(f"render raised an exception: {e}")
    
    def test_tick_no_errors(self):
        """Test that the tick method works without errors."""
        try:
            self.view.tick(fps=10)
        except Exception as e:
            self.fail(f"tick raised an exception: {e}")
    
    def test_color_constants_exist(self):
        """Test that all required color constants are defined."""
        required_colors = [
            'background', 'grid_line', 'dead_cell', 'alive_cell',
            'button', 'button_hover', 'button_text', 'ui_background'
        ]
        
        for color_name in required_colors:
            self.assertIn(color_name, GameOfLifeView.COLORS)
            self.assertIsInstance(GameOfLifeView.COLORS[color_name], tuple)
            self.assertEqual(len(GameOfLifeView.COLORS[color_name]), 3)


if __name__ == '__main__':
    unittest.main()

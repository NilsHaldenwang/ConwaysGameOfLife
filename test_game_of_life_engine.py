"""
Unit Tests for Game of Life Engine

This module contains comprehensive unit tests for the GameOfLifeEngine class.
Tests cover initialization, pattern loading, rule application, and edge cases.
"""

import unittest
import numpy as np
import tempfile
import os
from game_of_life_engine import GameOfLifeEngine


class TestGameOfLifeEngine(unittest.TestCase):
    """
    Test suite for the GameOfLifeEngine class.
    
    Tests all core functionality including initialization, cell management,
    neighbor counting, and game rule application.
    """
    
    def setUp(self):
        """
        Set up test fixtures before each test method.
        
        Creates a fresh engine instance for each test.
        """
        self.engine = GameOfLifeEngine(10, 10)
    
    def test_initialization(self):
        """Test that the engine initializes with correct dimensions and empty grid."""
        self.assertEqual(self.engine.rows, 10)
        self.assertEqual(self.engine.cols, 10)
        self.assertEqual(self.engine.grid.shape, (10, 10))
        # All cells should be dead initially
        self.assertTrue(np.all(self.engine.grid == 0))
    
    def test_set_and_get_cell(self):
        """Test setting and getting individual cell states."""
        # Set a cell to alive
        self.engine.set_cell(5, 5, 1)
        self.assertEqual(self.engine.get_cell(5, 5), 1)
        
        # Set a cell to dead
        self.engine.set_cell(5, 5, 0)
        self.assertEqual(self.engine.get_cell(5, 5), 0)
        
        # Test boundary cells
        self.engine.set_cell(0, 0, 1)
        self.assertEqual(self.engine.get_cell(0, 0), 1)
        
        self.engine.set_cell(9, 9, 1)
        self.assertEqual(self.engine.get_cell(9, 9), 1)
    
    def test_get_cell_out_of_bounds(self):
        """Test that getting cells outside grid bounds returns 0."""
        self.assertEqual(self.engine.get_cell(-1, 5), 0)
        self.assertEqual(self.engine.get_cell(5, -1), 0)
        self.assertEqual(self.engine.get_cell(10, 5), 0)
        self.assertEqual(self.engine.get_cell(5, 10), 0)
    
    def test_set_cell_out_of_bounds(self):
        """Test that setting cells outside bounds doesn't cause errors."""
        # Should not raise an exception
        self.engine.set_cell(-1, 5, 1)
        self.engine.set_cell(5, -1, 1)
        self.engine.set_cell(10, 5, 1)
        self.engine.set_cell(5, 10, 1)
    
    def test_clear(self):
        """Test clearing the grid sets all cells to dead."""
        # Set some cells alive
        self.engine.set_cell(3, 3, 1)
        self.engine.set_cell(4, 4, 1)
        self.engine.set_cell(5, 5, 1)
        
        # Clear the grid
        self.engine.clear()
        
        # All cells should be dead
        self.assertTrue(np.all(self.engine.grid == 0))
    
    def test_get_grid_copy(self):
        """Test that get_grid_copy returns a copy, not a reference."""
        # Set a cell
        self.engine.set_cell(5, 5, 1)
        
        # Get a copy
        grid_copy = self.engine.get_grid_copy()
        
        # Modify the copy
        grid_copy[3, 3] = 1
        
        # Original should be unchanged
        self.assertEqual(self.engine.get_cell(3, 3), 0)
        self.assertEqual(self.engine.get_cell(5, 5), 1)
    
    def test_get_dimensions(self):
        """Test getting grid dimensions."""
        rows, cols = self.engine.get_dimensions()
        self.assertEqual(rows, 10)
        self.assertEqual(cols, 10)
    
    def test_count_neighbors_empty_grid(self):
        """Test neighbor counting on an empty grid."""
        neighbors = self.engine.count_neighbors()
        # All counts should be zero
        self.assertTrue(np.all(neighbors == 0))
    
    def test_count_neighbors_single_cell(self):
        """Test neighbor counting with a single live cell."""
        # Place a cell at (5, 5)
        self.engine.set_cell(5, 5, 1)
        neighbors = self.engine.count_neighbors()
        
        # The cell itself should have 0 neighbors
        self.assertEqual(neighbors[5, 5], 0)
        
        # All 8 adjacent cells should have 1 neighbor
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue  # Skip the center cell
                self.assertEqual(neighbors[5 + dr, 5 + dc], 1)
    
    def test_count_neighbors_corner_cell(self):
        """Test neighbor counting for cells at corners."""
        # Place a cell at top-left corner (0, 0)
        self.engine.set_cell(0, 0, 1)
        neighbors = self.engine.count_neighbors()
        
        # Only 3 cells can be neighbors of a corner cell
        self.assertEqual(neighbors[0, 1], 1)  # Right
        self.assertEqual(neighbors[1, 0], 1)  # Bottom
        self.assertEqual(neighbors[1, 1], 1)  # Bottom-right diagonal
    
    def test_count_neighbors_horizontal_line(self):
        """Test neighbor counting with a horizontal line of cells."""
        # Create a horizontal line: (5, 4), (5, 5), (5, 6)
        self.engine.set_cell(5, 4, 1)
        self.engine.set_cell(5, 5, 1)
        self.engine.set_cell(5, 6, 1)
        
        neighbors = self.engine.count_neighbors()
        
        # Middle cell should have 2 neighbors
        self.assertEqual(neighbors[5, 5], 2)
        
        # End cells should have 1 neighbor each
        self.assertEqual(neighbors[5, 4], 1)
        self.assertEqual(neighbors[5, 6], 1)
    
    def test_step_still_life_block(self):
        """Test that a still life pattern (block) remains stable."""
        # Create a 2x2 block
        self.engine.set_cell(4, 4, 1)
        self.engine.set_cell(4, 5, 1)
        self.engine.set_cell(5, 4, 1)
        self.engine.set_cell(5, 5, 1)
        
        # Save initial state
        initial_grid = self.engine.get_grid_copy()
        
        # Run one step
        self.engine.step()
        
        # Grid should be unchanged (still life)
        np.testing.assert_array_equal(self.engine.grid, initial_grid)
    
    def test_step_oscillator_blinker(self):
        """Test that a blinker oscillator alternates correctly."""
        # Create a horizontal blinker
        self.engine.set_cell(5, 4, 1)
        self.engine.set_cell(5, 5, 1)
        self.engine.set_cell(5, 6, 1)
        
        # After one step, should become vertical
        self.engine.step()
        
        self.assertEqual(self.engine.get_cell(4, 5), 1)
        self.assertEqual(self.engine.get_cell(5, 5), 1)
        self.assertEqual(self.engine.get_cell(6, 5), 1)
        self.assertEqual(self.engine.get_cell(5, 4), 0)
        self.assertEqual(self.engine.get_cell(5, 6), 0)
        
        # After another step, should return to horizontal
        self.engine.step()
        
        self.assertEqual(self.engine.get_cell(5, 4), 1)
        self.assertEqual(self.engine.get_cell(5, 5), 1)
        self.assertEqual(self.engine.get_cell(5, 6), 1)
        self.assertEqual(self.engine.get_cell(4, 5), 0)
        self.assertEqual(self.engine.get_cell(6, 5), 0)
    
    def test_step_lonely_cell_dies(self):
        """Test that a lonely cell (no neighbors) dies."""
        # Create a single cell
        self.engine.set_cell(5, 5, 1)
        
        # Step
        self.engine.step()
        
        # Cell should die (loneliness)
        self.assertEqual(self.engine.get_cell(5, 5), 0)
    
    def test_step_overcrowded_cell_dies(self):
        """Test that an overcrowded cell (>3 neighbors) dies."""
        # Create a cell surrounded by 4 neighbors
        self.engine.set_cell(5, 5, 1)  # Center
        self.engine.set_cell(4, 5, 1)  # Top
        self.engine.set_cell(6, 5, 1)  # Bottom
        self.engine.set_cell(5, 4, 1)  # Left
        self.engine.set_cell(5, 6, 1)  # Right
        
        # Step
        self.engine.step()
        
        # Center cell should die (overpopulation)
        self.assertEqual(self.engine.get_cell(5, 5), 0)
    
    def test_step_birth_with_three_neighbors(self):
        """Test that a dead cell with exactly 3 neighbors becomes alive."""
        # Create an L-shape that will cause birth at (5, 5)
        self.engine.set_cell(4, 4, 1)
        self.engine.set_cell(5, 4, 1)
        self.engine.set_cell(4, 5, 1)
        
        # Cell at (5, 5) has exactly 3 neighbors
        neighbors = self.engine.count_neighbors()
        self.assertEqual(neighbors[5, 5], 3)
        
        # Step
        self.engine.step()
        
        # Cell at (5, 5) should now be alive
        self.assertEqual(self.engine.get_cell(5, 5), 1)
    
    def test_load_pattern_from_file_valid(self):
        """Test loading a valid pattern from a file."""
        # Create a temporary file with a pattern
        pattern_content = "010\n111\n010"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(pattern_content)
            temp_filename = f.name
        
        try:
            # Load the pattern
            self.engine.load_pattern_from_file(temp_filename)
            
            # Check dimensions
            self.assertEqual(self.engine.rows, 3)
            self.assertEqual(self.engine.cols, 3)
            
            # Check pattern
            expected = np.array([[0, 1, 0],
                                [1, 1, 1],
                                [0, 1, 0]], dtype=np.int8)
            np.testing.assert_array_equal(self.engine.grid, expected)
        finally:
            # Clean up temporary file
            os.unlink(temp_filename)
    
    def test_load_pattern_from_file_empty(self):
        """Test that loading an empty file raises ValueError."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("")
            temp_filename = f.name
        
        try:
            with self.assertRaises(ValueError):
                self.engine.load_pattern_from_file(temp_filename)
        finally:
            os.unlink(temp_filename)
    
    def test_load_pattern_from_file_invalid_character(self):
        """Test that loading a file with invalid characters raises ValueError."""
        pattern_content = "010\n1X1\n010"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(pattern_content)
            temp_filename = f.name
        
        try:
            with self.assertRaises(ValueError):
                self.engine.load_pattern_from_file(temp_filename)
        finally:
            os.unlink(temp_filename)
    
    def test_load_pattern_from_file_inconsistent_line_lengths(self):
        """Test that loading a file with inconsistent line lengths raises ValueError."""
        pattern_content = "010\n11\n010"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(pattern_content)
            temp_filename = f.name
        
        try:
            with self.assertRaises(ValueError):
                self.engine.load_pattern_from_file(temp_filename)
        finally:
            os.unlink(temp_filename)
    
    def test_load_pattern_from_file_nonexistent(self):
        """Test that loading a nonexistent file raises FileNotFoundError."""
        with self.assertRaises(FileNotFoundError):
            self.engine.load_pattern_from_file("nonexistent_file.txt")


if __name__ == '__main__':
    unittest.main()

"""
Conway's Game of Life Engine Module

This module implements the core logic for Conway's Game of Life using NumPy
for efficient numerical computations. It follows the Model-View-Controller (MVC)
pattern, where this class represents the Model.

Plain-language summary for non-programmers:
- The world is a rectangular grid made of cells. Each cell is either "alive"
    or "dead" (represented by 1 and 0 respectively).
- The grid is stored as a 2-dimensional NumPy array. The value at position
    (row, column) tells you whether that cell is alive.
- Each generation (step) every cell may change depending on how many live
    neighbors it has. Neighbors are the 8 surrounding cells (up, down, left,
    right and the 4 diagonals).

Rules of Conway's Game of Life (simple):
1. Any live cell with 2 or 3 live neighbors survives.
2. Any dead cell with exactly 3 live neighbors becomes alive.
3. All other cells die or stay dead.

The implementation uses vectorized NumPy operations (array arithmetic and
slice-based shifts) to compute neighbor counts efficiently without explicit
Python loops. This keeps the code fast even for large grids.
"""

import numpy as np
from typing import Tuple


class GameOfLifeEngine:
    """
    Core engine for Conway's Game of Life simulation.
    
    This class handles all game logic and state management using NumPy arrays
    for efficient computation. It is completely independent of any visualization
    or UI concerns (Separation of Concerns).
    
    Attributes:
        grid (np.ndarray): 2D NumPy array representing the current state
        rows (int): Number of rows in the grid
        cols (int): Number of columns in the grid
    """
    
    def __init__(self, rows: int, cols: int):
        """
        Initialize the Game of Life engine with an empty grid.
        
        Args:
            rows: Number of rows in the grid
            cols: Number of columns in the grid
        """
        self.rows = rows
        self.cols = cols
        # Initialize grid with zeros (all cells dead)
        self.grid = np.zeros((rows, cols), dtype=np.int8)
    
    def load_pattern_from_file(self, filename: str) -> None:
        """
        Load a pattern from a text file into the grid.
        
        The file format is:
        - n lines for an n x n grid
        - Each line contains n characters (0 or 1)
        - 0 represents a dead cell, 1 represents a live cell
        
        Args:
            filename: Path to the pattern file
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file format is invalid
        """
        with open(filename, 'r') as file:
            lines = file.read().strip().split('\n')
        
        # Validate file format
        if not lines:
            raise ValueError("Empty file")
        
        n = len(lines)
        
        # Check if all lines have the same length
        for i, line in enumerate(lines):
            if len(line) != n:
                raise ValueError(f"Line {i+1} has length {len(line)}, expected {n}")
        
        # Create a new grid with the size from the file
        new_grid = np.zeros((n, n), dtype=np.int8)
        
        # Parse the file content
        for i, line in enumerate(lines):
            for j, char in enumerate(line):
                if char == '1':
                    new_grid[i, j] = 1
                elif char != '0':
                    raise ValueError(f"Invalid character '{char}' at position ({i}, {j})")
        
        # Update the grid and dimensions
        self.grid = new_grid
        self.rows = n
        self.cols = n
    
    def set_cell(self, row: int, col: int, state: int) -> None:
        """
        Set the state of a specific cell.
        
        Args:
            row: Row index
            col: Column index
            state: Cell state (0 for dead, 1 for alive)
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row, col] = state
    
    def get_cell(self, row: int, col: int) -> int:
        """
        Get the state of a specific cell.
        
        Args:
            row: Row index
            col: Column index
            
        Returns:
            Cell state (0 for dead, 1 for alive)
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return int(self.grid[row, col])
        return 0
    
    def count_neighbors(self) -> np.ndarray:
        """
        Count the number of live neighbors for each cell using efficient NumPy operations.
        
        This method uses array shifting and addition to count neighbors in all 8 directions.
        This is much more efficient than nested loops for each cell.
        
        Returns:
            2D NumPy array with neighbor counts for each cell
        """
        # Simple explanation: create an array the same shape as the grid and
        # add up shifted copies of the grid so that each cell's value becomes
        # the number of neighboring live cells. Indexing/slicing is used so
        # that cells at the edge do not look beyond the array bounds.
        # Initialize neighbor count array
        neighbors = np.zeros_like(self.grid, dtype=np.int8)
        
        # Count neighbors in all 8 directions using array slicing
        # This is a highly efficient vectorized approach
        
        # Top row neighbors
        neighbors[:-1, :] += self.grid[1:, :]      # Bottom neighbor
        neighbors[1:, :] += self.grid[:-1, :]      # Top neighbor
        
        # Left column neighbors
        neighbors[:, :-1] += self.grid[:, 1:]      # Right neighbor
        neighbors[:, 1:] += self.grid[:, :-1]      # Left neighbor
        
        # Diagonal neighbors
        neighbors[:-1, :-1] += self.grid[1:, 1:]   # Bottom-right diagonal
        neighbors[1:, 1:] += self.grid[:-1, :-1]   # Top-left diagonal
        neighbors[:-1, 1:] += self.grid[1:, :-1]   # Bottom-left diagonal
        neighbors[1:, :-1] += self.grid[:-1, 1:]   # Top-right diagonal
        
        return neighbors
    
    def step(self) -> None:
        """
        Advance the simulation by one generation.
        
        Applies Conway's Game of Life rules:
        1. Any live cell with 2 or 3 neighbors survives
        2. Any dead cell with exactly 3 neighbors becomes alive
        3. All other cells die or stay dead
        
        This implementation uses efficient NumPy boolean operations for
        maximum performance.
        """
        # Count neighbors for all cells at once
        neighbors = self.count_neighbors()
        
        # Apply Game of Life rules using vectorized operations
        # Rule 1: Live cells with 2 or 3 neighbors survive
        survive = (self.grid == 1) & ((neighbors == 2) | (neighbors == 3))
        
        # Rule 2: Dead cells with exactly 3 neighbors become alive
        birth = (self.grid == 0) & (neighbors == 3)
        
        # Update grid: cells survive or are born
        self.grid = (survive | birth).astype(np.int8)
    
    def clear(self) -> None:
        """
        Clear the grid (set all cells to dead state).
        """
        self.grid.fill(0)
    
    def get_grid_copy(self) -> np.ndarray:
        """
        Get a copy of the current grid state.
        
        Returns a copy to prevent external modification of internal state.
        
        Returns:
            Copy of the current grid as a NumPy array
        """
        return self.grid.copy()
    
    def get_dimensions(self) -> Tuple[int, int]:
        """
        Get the current grid dimensions.
        
        Returns:
            Tuple of (rows, columns)
        """
        return (self.rows, self.cols)

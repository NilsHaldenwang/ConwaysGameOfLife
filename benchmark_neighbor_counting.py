"""
Benchmark: Array Slicing vs. Nested For-Loops for Neighbor Counting

This script compares two approaches for counting live neighbors in
Conway's Game of Life:

1. Array Slicing (NumPy-vectorized) – the approach used in game_of_life_engine.py
2. Nested For-Loops – the straightforward, intuitive approach

Both methods are verified to produce identical results before timing.
The benchmark runs each method multiple times across several grid sizes
and reports average execution times plus the speedup factor.
"""

import time
import numpy as np


# ---------------------------------------------------------------------------
# Method 1: Array Slicing (from game_of_life_engine.py)
# ---------------------------------------------------------------------------
def count_neighbors_slicing(grid: np.ndarray) -> np.ndarray:
    """
    Count live neighbors using vectorized NumPy array slicing.

    Instead of visiting every cell individually, this method shifts the
    entire grid in each of the 8 directions and accumulates the results.
    Boundary cells are handled implicitly because the slices never reach
    outside the array.
    """
    neighbors = np.zeros_like(grid, dtype=np.int8)

    # Vertical shifts
    neighbors[:-1, :] += grid[1:, :]       # neighbor below
    neighbors[1:, :]  += grid[:-1, :]      # neighbor above

    # Horizontal shifts
    neighbors[:, :-1] += grid[:, 1:]       # neighbor to the right
    neighbors[:, 1:]  += grid[:, :-1]      # neighbor to the left

    # Diagonal shifts
    neighbors[:-1, :-1] += grid[1:, 1:]    # bottom-right
    neighbors[1:, 1:]   += grid[:-1, :-1]  # top-left
    neighbors[:-1, 1:]  += grid[1:, :-1]   # bottom-left
    neighbors[1:, :-1]  += grid[:-1, 1:]   # top-right

    return neighbors


# ---------------------------------------------------------------------------
# Method 2: Nested For-Loops (classic approach)
# ---------------------------------------------------------------------------
def count_neighbors_loops(grid: np.ndarray) -> np.ndarray:
    """
    Count live neighbors using explicit nested for-loops.

    For every cell (row, col) the method iterates over all 8 surrounding
    positions, checks whether each position lies inside the grid, and
    sums up the live neighbors.
    """
    rows, cols = grid.shape
    neighbors = np.zeros_like(grid, dtype=np.int8)

    for row in range(rows):
        for col in range(cols):
            total = 0
            # Iterate over the 3x3 neighborhood
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue                    # skip the cell itself
                    r, c = row + dr, col + dc
                    if 0 <= r < rows and 0 <= c < cols:
                        total += grid[r, c]
            neighbors[row, col] = total

    return neighbors


# ---------------------------------------------------------------------------
# Correctness check
# ---------------------------------------------------------------------------
def verify_correctness(sizes: list[int], num_checks: int = 3) -> bool:
    """Return True if both methods produce identical results on random grids."""
    for size in sizes:
        for _ in range(num_checks):
            grid = (np.random.random((size, size)) < 0.3).astype(np.int8)
            result_slicing = count_neighbors_slicing(grid)
            result_loops   = count_neighbors_loops(grid)
            if not np.array_equal(result_slicing, result_loops):
                print(f"  MISMATCH on {size}x{size} grid!")
                return False
    return True


# ---------------------------------------------------------------------------
# Benchmark helper
# ---------------------------------------------------------------------------
def benchmark(func, grid: np.ndarray, repeats: int) -> float:
    """Run *func(grid)* *repeats* times and return the average time in seconds."""
    start = time.perf_counter()
    for _ in range(repeats):
        func(grid)
    elapsed = time.perf_counter() - start
    return elapsed / repeats


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    grid_sizes = [10, 50, 100, 200, 500]
    # Fewer repeats for large grids to keep total runtime reasonable
    repeats_map = {10: 500, 50: 200, 100: 50, 200: 20, 500: 5}
    density = 0.3

    print("=" * 72)
    print("  Benchmark: Array Slicing vs. Nested For-Loops")
    print("  (Neighbor Counting in Conway's Game of Life)")
    print("=" * 72)

    # --- Correctness verification ---
    print("\n[1] Verifying correctness (both methods must match) ...")
    if verify_correctness([10, 20, 50]):
        print("    OK – both methods produce identical results.\n")
    else:
        print("    FAILED – results differ. Aborting.")
        return

    # --- Benchmark ---
    print("[2] Running benchmarks ...\n")
    header = f"{'Grid Size':>12} | {'Slicing (s)':>14} | {'For-Loops (s)':>14} | {'Speedup':>10}"
    print(header)
    print("-" * len(header))

    results = []

    for size in grid_sizes:
        repeats = repeats_map[size]
        grid = (np.random.random((size, size)) < density).astype(np.int8)

        t_slicing = benchmark(count_neighbors_slicing, grid, repeats)
        t_loops   = benchmark(count_neighbors_loops,   grid, repeats)
        speedup   = t_loops / t_slicing if t_slicing > 0 else float('inf')

        results.append((size, t_slicing, t_loops, speedup))
        print(f"{size:>7}x{size:<4} | {t_slicing:>14.6f} | {t_loops:>14.6f} | {speedup:>9.1f}x")

    # --- Summary ---
    print("\n" + "=" * 72)
    print("  Summary")
    print("=" * 72)
    avg_speedup = sum(r[3] for r in results) / len(results)
    max_speedup = max(results, key=lambda r: r[3])
    print(f"  Average speedup:  {avg_speedup:.1f}x")
    print(f"  Maximum speedup:  {max_speedup[3]:.1f}x  (at {max_speedup[0]}x{max_speedup[0]} grid)")
    print()
    print("  Conclusion:")
    print("  The NumPy array-slicing approach avoids Python-level loops entirely.")
    print("  All 8 neighbor directions are computed as bulk array operations that")
    print("  run in optimized C code inside NumPy. The nested for-loop approach")
    print("  must iterate over every cell and every neighbor individually in pure")
    print("  Python, which is orders of magnitude slower for large grids.")
    print("=" * 72)


if __name__ == "__main__":
    main()

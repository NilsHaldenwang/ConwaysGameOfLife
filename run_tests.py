#!/usr/bin/env python3
"""
Test Runner for Conway's Game of Life

This script runs all unit tests and provides a summary of results.
"""

import unittest
import sys
import os

# Set headless mode for PyGame (required for automated testing)
os.environ['SDL_VIDEODRIVER'] = 'dummy'


def run_tests():
    """
    Discover and run all unit tests.
    
    Returns:
        bool: True if all tests passed, False otherwise
    """
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern='test_*.py')
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)
    
    # Return success status
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)

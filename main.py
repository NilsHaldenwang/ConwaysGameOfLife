"""
Conway's Game of Life - Educational Demo
Main Entry Point

This is the main entry point for the Conway's Game of Life educational demonstration.
The application implements a clean MVC (Model-View-Controller) architecture:

- Model (game_of_life_engine.py): Core game logic using NumPy
- View (game_of_life_view.py): PyGame visualization
- Controller (game_of_life_controller.py): Coordination and user input handling

Author: Educational Demo for Computer Science Professorship
Purpose: Demonstrating design patterns and clean code architecture
"""

from game_of_life_controller import GameOfLifeController


def main():
    """
    Main entry point for the application.
    
    Initializes the controller and starts the game loop.
    """
    # Create the controller (which initializes model and view)
    # Starting with a 50x50 grid with 15-pixel cells
    controller = GameOfLifeController(
        initial_rows=50,
        initial_cols=50,
        cell_size=15
    )
    
    # Set simulation speed (10 generations per second)
    controller.set_simulation_speed(10)
    
    # Run the application
    controller.run()


if __name__ == "__main__":
    main()

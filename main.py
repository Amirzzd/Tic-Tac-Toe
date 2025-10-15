"""
Main entry point for the Tic-Tac-Toe game.

This module initializes and starts the game application.
Run this file to play Tic-Tac-Toe against an AI opponent.

Usage:
    python main.py
"""

from controller import GameController
from ui import GameUI


def main():
    """
    Initialize and run the Tic-Tac-Toe game.
    
    This function:
    1. Creates the game controller
    2. Creates the UI and links it to the controller
    3. Sets up the game window
    4. Starts the main game loop
    """
    # Create the game controller
    controller = GameController()
    
    # Create the UI with the controller
    game_ui = GameUI(controller)
    
    # Setup the game window
    game_ui.setup_window()
    
    # Run the game (starts the Tkinter main loop)
    game_ui.run()


if __name__ == "__main__":
    main()

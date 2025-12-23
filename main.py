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

    controller = GameController()
    
    game_ui = GameUI(controller)
    
    game_ui.setup_window()
    
    game_ui.run()


if __name__ == "__main__":
    main()

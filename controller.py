

from typing import Optional, Callable
from board import Board
from player import Player, PlayerType
from ai import TicTacToeAI


class GameController:

    
    def __init__(self):
        self.game_board: Board = Board()
        self.human_player: Optional[Player] = None
        self.computer_player: Optional[Player] = None
        self.current_turn_player: Optional[Player] = None
        self.ai_opponent: Optional[TicTacToeAI] = None
        self.is_game_active: bool = False
        
        # Callback functions to notify UI of game events
        self.move_made_callback: Optional[Callable] = None
        self.game_ended_callback: Optional[Callable] = None
    
    def start_new_game(self, chosen_symbol_for_human: str) -> None:

        self.game_board.reset()
        
        computer_symbol = 'O' if chosen_symbol_for_human == 'X' else 'X'
        
        self.human_player = Player(chosen_symbol_for_human, PlayerType.HUMAN)
        self.computer_player = Player(computer_symbol, PlayerType.AI)
        
        self.ai_opponent = TicTacToeAI(computer_symbol, chosen_symbol_for_human)
        
        if chosen_symbol_for_human == 'X':
            self.current_turn_player = self.human_player
        else:
            self.current_turn_player = self.computer_player
        
        self.is_game_active = True
        
        if self.current_turn_player.is_ai():
            self._make_ai_move()
    
    def make_human_move(self, row: int, col: int) -> bool:

        # Don't allow moves if game has ended
        if not self.is_game_active:
            return False
        
        # Verify it's the human player's turn
        if not self.current_turn_player or not self.current_turn_player.is_human():
            return False
        
        # Check if the chosen cell is available
        if not self.game_board.is_valid_move(row, col):
            return False
        
        # Place the human player's symbol on the board
        self.game_board.make_move(row, col, self.current_turn_player.symbol)
        
        # Notify UI that a move was made
        if self.move_made_callback:
            self.move_made_callback(row, col, self.current_turn_player.symbol)
        
        # Check if this move ended the game
        if self._check_if_game_ended():
            return True
        
        # Switch turn to AI player
        self.current_turn_player = self.computer_player
        
        # AI move will be triggered by UI after a delay (keeps UI responsive)
        return True
    
    def _make_ai_move(self) -> None:
        """
        Let the AI opponent make its move.
        
        This is a private method called internally when it's the AI's turn.
        """
        # Don't make a move if game has ended or AI is not initialized
        if not self.is_game_active or not self.ai_opponent:
            return
        
        # Ask AI to calculate the best move
        best_move_position = self.ai_opponent.get_best_move(self.game_board)
        
        if best_move_position:
            row_index, column_index = best_move_position
            
            # Place AI's symbol on the board
            self.game_board.make_move(row_index, column_index, self.computer_player.symbol)
            
            # Notify UI that AI made a move
            if self.move_made_callback:
                self.move_made_callback(row_index, column_index, self.computer_player.symbol)
            
            # Check if AI's move ended the game
            if self._check_if_game_ended():
                return
            
            # Switch turn back to human player
            self.current_turn_player = self.human_player
    
    def _check_if_game_ended(self) -> bool:
        """
        Check if the game has ended due to a win or draw.
        
        This method checks for:
        1. A winner (three in a row)
        2. A draw (board full with no winner)
        
        If game has ended, notifies UI via callback.
        
        Returns:
            True if game ended, False if game continues
        """
        # Check if anyone won
        winning_symbol = self.game_board.check_winner()
        
        if winning_symbol:
            # Game over - we have a winner
            self.is_game_active = False
            
            # Determine which player won
            if winning_symbol == self.human_player.symbol:
                winning_player = self.human_player
            else:
                winning_player = self.computer_player
            
            # Notify UI of the winner
            if self.game_ended_callback:
                self.game_ended_callback(winning_player, is_draw=False)
            
            return True
        
        # Check if board is full (draw)
        if self.game_board.is_draw():
            # Game over - it's a draw
            self.is_game_active = False
            
            # Notify UI of the draw (no winner)
            if self.game_ended_callback:
                self.game_ended_callback(None, is_draw=True)
            
            return True
        
        # Game continues
        return False
    
    def reset_game(self) -> None:
        """
        Reset the game state to prepare for a new game.
        
        Clears the board and sets game as inactive.
        """
        self.game_board.reset()
        self.is_game_active = False
        self.current_turn_player = None
    
    def set_move_callback(self, callback_function: Callable) -> None:
        """
        Register a function to be called when any move is made.
        
        The UI uses this to update the display when moves happen.
        
        Args:
            callback_function: Function that accepts (row, col, symbol) parameters
        """
        self.move_made_callback = callback_function
    
    def set_game_over_callback(self, callback_function: Callable) -> None:
        """
        Register a function to be called when the game ends.
        
        The UI uses this to show win/draw messages.
        
        Args:
            callback_function: Function that accepts (winner_player, is_draw) parameters
        """
        self.game_ended_callback = callback_function
    
    def get_cell_value(self, row: int, col: int) -> Optional[str]:
        """
        Get the symbol at a specific board position.
        
        Args:
            row: Row index (0-2)
            col: Column index (0-2)
            
        Returns:
            'X', 'O', or None if the cell is empty
        """
        return self.game_board.get_cell(row, col)



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

        if not self.is_game_active:
            return False
        
        if not self.current_turn_player or not self.current_turn_player.is_human():
            return False
        
        if not self.game_board.is_valid_move(row, col):
            return False
        
        self.game_board.make_move(row, col, self.current_turn_player.symbol)
        
        if self.move_made_callback:
            self.move_made_callback(row, col, self.current_turn_player.symbol)
        
        if self._check_if_game_ended():
            return True
        
        self.current_turn_player = self.computer_player
        
        return True
    
    def _make_ai_move(self) -> None:
        if not self.is_game_active or not self.ai_opponent:
            return
        
        best_move_position = self.ai_opponent.get_best_move(self.game_board)
        
        if best_move_position:
            row_index, column_index = best_move_position
            
            self.game_board.make_move(row_index, column_index, self.computer_player.symbol)
            
            if self.move_made_callback:
                self.move_made_callback(row_index, column_index, self.computer_player.symbol)
            
            if self._check_if_game_ended():
                return
            
            self.current_turn_player = self.human_player
    
    def _check_if_game_ended(self) -> bool:
        winning_symbol = self.game_board.check_winner()
        
        if winning_symbol:
            self.is_game_active = False
            
            if winning_symbol == self.human_player.symbol:
                winning_player = self.human_player
            else:
                winning_player = self.computer_player
            
            if self.game_ended_callback:
                self.game_ended_callback(winning_player, is_draw=False)
            
            return True
        
        if self.game_board.is_draw():
            self.is_game_active = False
            
            if self.game_ended_callback:
                self.game_ended_callback(None, is_draw=True)
            
            return True
        
        return False
    
    def reset_game(self) -> None:
        self.game_board.reset()
        self.is_game_active = False
        self.current_turn_player = None
    
    def set_move_callback(self, callback_function: Callable) -> None:
        self.move_made_callback = callback_function
    
    def set_game_over_callback(self, callback_function: Callable) -> None:
        self.game_ended_callback = callback_function
    
    def get_cell_value(self, row: int, col: int) -> Optional[str]:
        return self.game_board.get_cell(row, col)

from typing import Tuple, Optional
import math
from board import Board


class TicTacToeAI:

    
    def __init__(self, ai_symbol: str, opponent_symbol: str):
        self.ai_symbol: str = ai_symbol
        self.opponent_symbol: str = opponent_symbol
    
    def get_best_move(self, board: Board):
        
        available_cell_positions = board.get_available_moves()
        
        if not available_cell_positions:
            return None
        
        if len(available_cell_positions) == 9:
            return (1, 1)
        

        highest_score = -math.inf
        optimal_move_position = None
        

        for row_index, column_index in available_cell_positions:
            
            simulated_board = board.copy()
            simulated_board.make_move(row_index, column_index, self.ai_symbol)
            
            move_score = self.minimax(
                board=simulated_board,
                is_maximizing_player=False,
                best_maximize_score=-math.inf,
                best_minimize_score=math.inf
            )
            
            if move_score > highest_score:
                highest_score = move_score
                optimal_move_position = (row_index, column_index)
        
        return optimal_move_position
    
    def minimax(self, board: Board, is_maximizing_player: bool, 
                best_maximize_score: float, best_minimize_score: float) -> float:


        game_winner = board.check_winner()
        
        if game_winner == self.ai_symbol:
            return 1 
        
        elif game_winner == self.opponent_symbol:
            return -1  
        
        elif board.is_full():
            return 0
        
        available_cell_positions = board.get_available_moves()
        
        if is_maximizing_player:
            maximum_evaluation = -math.inf
            
            for row_index, column_index in available_cell_positions:
                simulated_board = board.copy()
                simulated_board.make_move(row_index, column_index, self.ai_symbol)
                
                evaluation_score = self.minimax(
                    board=simulated_board,
                    is_maximizing_player=False,
                    best_maximize_score=best_maximize_score,
                    best_minimize_score=best_minimize_score
                )
                
                maximum_evaluation = max(maximum_evaluation, evaluation_score)
                best_maximize_score = max(best_maximize_score, evaluation_score)
                
                if best_minimize_score <= best_maximize_score:
                    break  
            return maximum_evaluation
        
        else:
            minimum_evaluation = math.inf
            
            for row_index, column_index in available_cell_positions:
                simulated_board = board.copy()
                simulated_board.make_move(row_index, column_index, self.opponent_symbol)
                
                evaluation_score = self.minimax(
                    board=simulated_board,
                    is_maximizing_player=True,
                    best_maximize_score=best_maximize_score,
                    best_minimize_score=best_minimize_score
                )
                
                minimum_evaluation = min(minimum_evaluation, evaluation_score)
                
                best_minimize_score = min(best_minimize_score, evaluation_score)
                if best_minimize_score <= best_maximize_score:
                    break 
            
            return minimum_evaluation
        

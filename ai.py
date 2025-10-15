"""
AI module for Tic-Tac-Toe game.
Implements an unbeatable AI using the Minimax algorithm with alpha-beta pruning.
"""

from typing import Tuple, Optional
import math
from board import Board


class TicTacToeAI:
    """
    AI player that uses the Minimax algorithm with alpha-beta pruning.
    
    Responsibilities:
    - Calculate the optimal move for the AI player
    - Use Minimax algorithm to evaluate all possible game states
    - Ensure the AI plays optimally (unbeatable)
    """
    
    def __init__(self, ai_symbol: str, opponent_symbol: str):
        """
        Initialize the AI player.
        
        Args:
            ai_symbol: The symbol the AI uses ('X' or 'O')
            opponent_symbol: The opponent's symbol
        """
        self.ai_symbol: str = ai_symbol
        self.opponent_symbol: str = opponent_symbol
    
    def get_best_move(self, board: Board) -> Optional[Tuple[int, int]]:
        """
        Calculate and return the best move for the AI using the Minimax algorithm.
        
        This method evaluates all possible moves and chooses the one that leads to
        the best outcome for the AI (win or draw).
        
        Args:
            board: Current game board state
            
        Returns:
            Tuple of (row, col) for the best move, or None if no moves available
        """
        available_cell_positions = board.get_available_moves()
        
        # No moves available - board is full
        if not available_cell_positions:
            return None
        
        # First move optimization: play center for best position
        if len(available_cell_positions) == 9:
            return (1, 1)  # Center cell is strategically optimal
        
        # Initialize best score to worst possible value
        highest_score = -math.inf
        optimal_move_position = None
        
        # Try each possible move and evaluate its outcome
        for row_index, column_index in available_cell_positions:
            # Create a copy of the board to test this move
            simulated_board = board.copy()
            simulated_board.make_move(row_index, column_index, self.ai_symbol)
            
            # Calculate the score for this move using minimax algorithm
            move_score = self.minimax(
                board=simulated_board,
                current_depth=0,
                is_maximizing_player=False,  # Next turn is opponent's
                alpha_value=-math.inf,
                beta_value=math.inf
            )
            
            # Keep track of the move with the highest score
            if move_score > highest_score:
                highest_score = move_score
                optimal_move_position = (row_index, column_index)
        
        return optimal_move_position
    
    def minimax(self, board: Board, current_depth: int, is_maximizing_player: bool, 
                alpha_value: float, beta_value: float) -> float:
        """
        Minimax algorithm with alpha-beta pruning for optimal move calculation.
        
        This recursive algorithm explores all possible game outcomes and chooses
        the path that leads to the best result for the AI. Alpha-beta pruning
        eliminates branches that won't affect the final decision, improving performance.
        
        Args:
            board: Current board state to evaluate
            current_depth: How many moves deep we are in the game tree
            is_maximizing_player: True if it's AI's turn (maximize score), 
                                  False if it's opponent's turn (minimize score)
            alpha_value: Best score the maximizing player can guarantee
            beta_value: Best score the minimizing player can guarantee
            
        Returns:
            Score of the board state (positive = good for AI, negative = good for opponent)
        """
        # Check if game has ended (someone won or board is full)
        game_winner = board.check_winner()
        
        # Terminal state: AI won
        if game_winner == self.ai_symbol:
            return 10 - current_depth  # Prefer winning quickly (fewer moves)
        
        # Terminal state: Opponent won
        elif game_winner == self.opponent_symbol:
            return current_depth - 10  # Prefer losing slowly (more moves)
        
        # Terminal state: Draw (board full, no winner)
        elif board.is_full():
            return 0  # Neutral score for draw
        
        # Get all empty cells where a move can be made
        available_cell_positions = board.get_available_moves()
        
        # AI's turn: try to maximize the score
        if is_maximizing_player:
            maximum_evaluation = -math.inf
            
            for row_index, column_index in available_cell_positions:
                # Simulate AI making this move
                simulated_board = board.copy()
                simulated_board.make_move(row_index, column_index, self.ai_symbol)
                
                # Recursively evaluate this move (opponent's turn next)
                evaluation_score = self.minimax(
                    board=simulated_board,
                    current_depth=current_depth + 1,
                    is_maximizing_player=False,
                    alpha_value=alpha_value,
                    beta_value=beta_value
                )
                
                maximum_evaluation = max(maximum_evaluation, evaluation_score)
                
                # Alpha-beta pruning: stop if we found a move that's good enough
                alpha_value = max(alpha_value, evaluation_score)
                if beta_value <= alpha_value:
                    break  # Beta cutoff - no need to explore further
            
            return maximum_evaluation
        
        # Opponent's turn: try to minimize the score
        else:
            minimum_evaluation = math.inf
            
            for row_index, column_index in available_cell_positions:
                # Simulate opponent making this move
                simulated_board = board.copy()
                simulated_board.make_move(row_index, column_index, self.opponent_symbol)
                
                # Recursively evaluate this move (AI's turn next)
                evaluation_score = self.minimax(
                    board=simulated_board,
                    current_depth=current_depth + 1,
                    is_maximizing_player=True,
                    alpha_value=alpha_value,
                    beta_value=beta_value
                )
                
                minimum_evaluation = min(minimum_evaluation, evaluation_score)
                
                # Alpha-beta pruning: stop if we found a move that's good enough
                beta_value = min(beta_value, evaluation_score)
                if beta_value <= alpha_value:
                    break  # Alpha cutoff - no need to explore further
            
            return minimum_evaluation

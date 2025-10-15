"""
Board module for Tic-Tac-Toe game.
Manages the 3x3 grid, move validation, and win/draw detection.
"""

from typing import Optional, List, Tuple


class Board:
    """
    Represents the Tic-Tac-Toe game board.
    
    Responsibilities:
    - Maintain the 3x3 grid state
    - Validate moves
    - Check for winners and draws
    - Provide available moves
    """
    
    def __init__(self):
        """
        Initialize an empty 3x3 Tic-Tac-Toe board.
        
        Creates a 3x3 grid where each cell starts as None (empty).
        """
        # 3x3 grid: None = empty, 'X' or 'O' = player symbol
        self.grid: List[List[Optional[str]]] = [[None for _ in range(3)] for _ in range(3)]
        self.board_size: int = 3  # Standard Tic-Tac-Toe is 3x3
    
    def make_move(self, row: int, col: int, player_symbol: str) -> bool:
        """
        Place a player's symbol (X or O) on the board at the specified position.
        
        Args:
            row: Row index (0 = top, 1 = middle, 2 = bottom)
            col: Column index (0 = left, 1 = middle, 2 = right)
            player_symbol: The player's symbol ('X' or 'O')
            
        Returns:
            True if move was successfully placed, False if cell was occupied or out of bounds
        """
        if self.is_valid_move(row, col):
            self.grid[row][col] = player_symbol
            return True
        return False
    
    def is_valid_move(self, row: int, col: int) -> bool:
        """
        Check if a move can be made at the specified position.
        
        A move is valid if:
        1. The position is within board boundaries (0-2 for both row and col)
        2. The cell is empty (not already occupied by X or O)
        
        Args:
            row: Row index to check
            col: Column index to check
            
        Returns:
            True if the cell is empty and within bounds, False otherwise
        """
        # Check bounds first
        if not (0 <= row < self.board_size and 0 <= col < self.board_size):
            return False
        
        # Check if cell is empty
        return self.grid[row][col] is None
    
    def check_winner(self) -> Optional[str]:
        """
        Check if there's a winner on the board by examining all winning patterns.
        
        Winning patterns:
        - 3 in a row horizontally (any row)
        - 3 in a column vertically (any column)
        - 3 diagonally (top-left to bottom-right OR top-right to bottom-left)
        
        Returns:
            The winning symbol ('X' or 'O') if there's a winner, or None if no winner yet
        """
        # Check all three rows for a horizontal win
        for row_cells in self.grid:
            if row_cells[0] == row_cells[1] == row_cells[2] and row_cells[0] is not None:
                return row_cells[0]  # Return the winning symbol
        
        # Check all three columns for a vertical win
        for column_index in range(self.board_size):
            if (self.grid[0][column_index] == self.grid[1][column_index] == self.grid[2][column_index] 
                and self.grid[0][column_index] is not None):
                return self.grid[0][column_index]  # Return the winning symbol
        
        # Check diagonal from top-left to bottom-right (\)
        if (self.grid[0][0] == self.grid[1][1] == self.grid[2][2] 
            and self.grid[0][0] is not None):
            return self.grid[0][0]  # Return the winning symbol
        
        # Check diagonal from top-right to bottom-left (/)
        if (self.grid[0][2] == self.grid[1][1] == self.grid[2][0] 
            and self.grid[0][2] is not None):
            return self.grid[0][2]  # Return the winning symbol
        
        # No winner found
        return None
    
    def is_full(self) -> bool:
        """
        Check if all cells on the board are occupied (no empty spaces left).
        
        Returns:
            True if every cell has an X or O, False if any cell is empty
        """
        # Check every cell in every row - all must be filled (not None)
        return all(cell_value is not None 
                   for row_cells in self.grid 
                   for cell_value in row_cells)
    
    def is_draw(self) -> bool:
        """
        Check if the game ended in a draw.
        
        A draw occurs when:
        1. The board is completely full (no empty cells)
        2. No player has won (no three-in-a-row)
        
        Returns:
            True if the game is a draw, False otherwise
        """
        return self.is_full() and self.check_winner() is None
    
    def get_available_moves(self) -> List[Tuple[int, int]]:
        """
        Get all empty cell positions where a move can be made.
        
        Returns:
            List of (row, col) tuples for each empty cell.
            Example: [(0, 1), (1, 2), (2, 0)] means cells at those positions are empty
        """
        empty_cell_positions = []
        
        for row_index in range(self.board_size):
            for column_index in range(self.board_size):
                if self.grid[row_index][column_index] is None:
                    empty_cell_positions.append((row_index, column_index))
        
        return empty_cell_positions
    
    def get_cell(self, row: int, col: int) -> Optional[str]:
        """
        Get the symbol (X, O, or empty) at a specific board position.
        
        Args:
            row: Row index (0-2)
            col: Column index (0-2)
            
        Returns:
            'X', 'O', or None (if cell is empty or out of bounds)
        """
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            return self.grid[row][col]
        return None
    
    def reset(self) -> None:
        """
        Clear the entire board to start a new game.
        
        Sets all cells back to None (empty).
        """
        self.grid = [[None for _ in range(3)] for _ in range(3)]
    
    def copy(self) -> 'Board':
        """
        Create an independent copy of the current board.
        
        This is useful for testing potential moves without affecting the actual game board.
        The AI uses this to simulate moves during its decision-making process.
        
        Returns:
            A new Board object with the same cell values as this board
        """
        copied_board = Board()
        # Create a deep copy of the grid (copy each row separately)
        copied_board.grid = [row_cells[:] for row_cells in self.grid]
        return copied_board
    
    def __str__(self) -> str:
        """
        Create a text representation of the board for debugging/testing.
        
        Returns:
            String showing the board layout with X, O, and empty spaces
        """
        text_lines = []
        for row_cells in self.grid:
            # Replace None with space, keep X and O as-is
            row_text = " | ".join(cell_value if cell_value else " " for cell_value in row_cells)
            text_lines.append(row_text)
        
        # Join rows with separator lines
        return "\n" + ("-" * 9 + "\n").join(text_lines)

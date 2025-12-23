
from typing import Optional, List, Tuple


class Board:

    
    def __init__(self):
        self.grid: List[List[Optional[str]]] = [[None for _ in range(3)] for _ in range(3)]
        self.board_size: int = 3  # Standard Tic-Tac-Toe is 3x3
    
    def make_move(self, row: int, col: int, player_symbol: str) -> bool:

        if self.is_valid_move(row, col):
            self.grid[row][col] = player_symbol
            return True
        return False
    
    def is_valid_move(self, row: int, col: int) -> bool:

        if not (0 <= row < self.board_size and 0 <= col < self.board_size):
            return False
    
        return self.grid[row][col] is None
    
    def check_winner(self) -> Optional[str]:
        for row_cells in self.grid:
            if row_cells[0] == row_cells[1] == row_cells[2] and row_cells[0] is not None:
                return row_cells[0]  # Return the winning symbol
        
        for column_index in range(self.board_size):
            if (self.grid[0][column_index] == self.grid[1][column_index] == self.grid[2][column_index] 
                and self.grid[0][column_index] is not None):
                return self.grid[0][column_index]  # Return the winning symbol
        
        if (self.grid[0][0] == self.grid[1][1] == self.grid[2][2] 
            and self.grid[0][0] is not None):
            return self.grid[0][0]  # Return the winning symbol
        
        if (self.grid[0][2] == self.grid[1][1] == self.grid[2][0] 
            and self.grid[0][2] is not None):
            return self.grid[0][2]  # Return the winning symbol
        
        # No winner found
        return None
    
    def is_full(self) -> bool:
        return all(cell_value is not None 
                   for row_cells in self.grid 
                   for cell_value in row_cells)
    
    def is_draw(self) -> bool:
        return self.is_full() and self.check_winner() is None
    
    def get_available_moves(self) -> List[Tuple[int, int]]:
        empty_cell_positions = []
        
        for row_index in range(self.board_size):
            for column_index in range(self.board_size):
                if self.grid[row_index][column_index] is None:
                    empty_cell_positions.append((row_index, column_index))
        
        return empty_cell_positions
    
    def get_cell(self, row: int, col: int) -> Optional[str]:
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            return self.grid[row][col]
        return None
    
    def reset(self) -> None:
        self.grid = [[None for _ in range(3)] for _ in range(3)]
    
    def copy(self) -> 'Board':
        copied_board = Board()
        copied_board.grid = [row_cells[:] for row_cells in self.grid]
        return copied_board
    
    def __str__(self) -> str:
        text_lines = []
        for row_cells in self.grid:
            row_text = " | ".join(cell_value if cell_value else " " for cell_value in row_cells)
            text_lines.append(row_text)
        
        return "\n" + ("-" * 9 + "\n").join(text_lines)

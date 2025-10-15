"""
Player module for Tic-Tac-Toe game.
Represents players (human and AI) with their symbols.
"""

from enum import Enum
from typing import Optional


class PlayerType(Enum):
    """Enumeration for player types."""
    HUMAN = "human"
    AI = "ai"


class Player:
    """
    Represents a player in the Tic-Tac-Toe game.
    
    Responsibilities:
    - Store player symbol (X or O)
    - Identify player type (human or AI)
    """
    
    def __init__(self, symbol: str, player_type: PlayerType, name: Optional[str] = None):
        """
        Initialize a player.
        
        Args:
            symbol: The player's symbol ('X' or 'O')
            player_type: Whether this is a human or AI player
            name: Optional player name for display purposes
        """
        if symbol not in ['X', 'O']:
            raise ValueError("Player symbol must be 'X' or 'O'")
        
        self.symbol: str = symbol
        self.player_type: PlayerType = player_type
        self.name: str = name or (f"Player ({symbol})" if player_type == PlayerType.HUMAN 
                                   else f"AI ({symbol})")
    
    def is_human(self) -> bool:
        """Check if this is a human player."""
        return self.player_type == PlayerType.HUMAN
    
    def is_ai(self) -> bool:
        """Check if this is an AI player."""
        return self.player_type == PlayerType.AI
    
    def __str__(self) -> str:
        """String representation of the player."""
        return self.name
    
    def __repr__(self) -> str:
        """Detailed representation for debugging."""
        return f"Player(symbol='{self.symbol}', type={self.player_type.value}, name='{self.name}')"

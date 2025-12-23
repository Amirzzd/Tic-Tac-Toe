from enum import Enum
from typing import Optional


class PlayerType(Enum):
    HUMAN = "human"
    AI = "ai"


class Player:

    def __init__(self, symbol: str, player_type: PlayerType, name: Optional[str] = None):

        if symbol not in ['X', 'O']:
            raise ValueError("Player symbol must be 'X' or 'O'")
        
        self.symbol: str = symbol
        self.player_type: PlayerType = player_type
        self.name: str = name or (f"Player ({symbol})" if player_type == PlayerType.HUMAN 
                                   else f"AI ({symbol})")
    
    def is_human(self) -> bool:
        return self.player_type == PlayerType.HUMAN
    
    def is_ai(self) -> bool:
        return self.player_type == PlayerType.AI
    
    def __str__(self) -> str:
        return self.name
    
# Tic-Tac-Toe Game with AI

A complete implementation of Tic-Tac-Toe with a graphical user interface and an unbeatable AI opponent using the Minimax algorithm.

## Features

- **Graphical User Interface**: Clean, modern UI built with Tkinter
- **Unbeatable AI**: Uses Minimax algorithm with alpha-beta pruning
- **Symbol Choice**: Choose to play as X or O
- **Color-Coded Symbols**: X is blue, O is red
- **Game State Management**: Detects wins, draws, and invalid moves
- **Play Again**: Option to start a new game after each match
- **Clean Architecture**: Modular, object-oriented design following SOLID principles

## Project Structure

```
TicTok/
├── main.py         # Entry point - starts the application
├── ui.py           # Tkinter GUI implementation
├── controller.py   # Game logic coordinator
├── board.py        # Board state and move validation
├── player.py       # Player representation
├── ai.py           # Minimax AI implementation
└── README.md       # This file
```

## Architecture

The project follows a clean MVC-like architecture:

- **Board**: Manages the 3×3 grid, validates moves, checks for winners/draws
- **Player**: Represents human and AI players with their symbols
- **AI**: Implements the Minimax algorithm for optimal play
- **GameController**: Coordinates gameplay, manages turns, and game state
- **GameUI**: Handles all Tkinter GUI components and user interactions
- **main.py**: Application entry point that wires everything together

## How to Run

1. Make sure you have Python 3.11+ installed
2. Navigate to the project directory
3. Run the game:

```bash
python main.py
```

No external dependencies are required - only Python standard library!

## How to Play

1. **Launch the game** by running `main.py`
2. **Choose your symbol**: Select whether you want to play as X or O
   - X always goes first
   - O always goes second
3. **Make your move**: Click on any empty cell to place your symbol
4. **AI responds**: The AI will automatically make its move
5. **Win or Draw**: The game detects when someone wins or when it's a draw
6. **Play Again**: Choose whether to start a new game

## Game Rules

- Players take turns placing their symbol (X or O) on a 3×3 grid
- The first player to get 3 of their symbols in a row (horizontally, vertically, or diagonally) wins
- If all 9 cells are filled without a winner, the game is a draw
- X always makes the first move

## AI Implementation

The AI uses the **Minimax algorithm** with **alpha-beta pruning**:

- **Minimax**: Recursively evaluates all possible game states to find the optimal move
- **Alpha-Beta Pruning**: Optimization that eliminates branches that won't affect the final decision
- **Evaluation**: Scores positions based on wins (+1), losses (-1), and draws (0)
- **Depth Penalty**: Prefers faster wins and slower losses

The AI is **unbeatable** - the best you can do is draw!

## Code Quality

- **Object-Oriented Design**: Each class has a single, clear responsibility
- **Type Hints**: All functions use type annotations for clarity
- **Docstrings**: Comprehensive documentation for all classes and methods
- **Comments**: Key algorithms and logic are explained with inline comments
- **SOLID Principles**: 
  - Single Responsibility: Each class has one purpose
  - Open/Closed: Easy to extend without modifying existing code
  - Dependency Inversion: Controller depends on abstractions, not concrete implementations
- **No Global Variables**: Everything is properly encapsulated

## Technical Details

- **Language**: Python 3.11+
- **GUI Framework**: Tkinter (standard library)
- **Algorithm**: Minimax with alpha-beta pruning
- **Architecture**: MVC-like separation of concerns
- **Dependencies**: None (only standard library)

## Possible Enhancements

Future improvements could include:

- Difficulty levels (easy = random, medium = some strategy, hard = minimax)
- Score tracking across multiple games
- Animations for moves and wins
- Sound effects
- Different board sizes (4×4, 5×5)
- Network multiplayer
- Save/load game state

## License

Free to use for educational purposes.

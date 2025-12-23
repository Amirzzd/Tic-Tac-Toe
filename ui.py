"""
UI module for Tic-Tac-Toe game.
Handles the Tkinter graphical user interface.
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
from typing import Optional, List
from controller import GameController
from player import Player


class GameUI:

    # Color scheme
    COLOR_X = "#00BFFF" 
    COLOR_O = "#FF4444"  
    COLOR_BG = "#000000"  
    COLOR_BUTTON = "#333333" 
    COLOR_BUTTON_HOVER = "#555555" 
    COLOR_TEXT = "#FFFFFF"
    
    def __init__(self, controller: GameController):
        self.controller = controller
        self.root: Optional[tk.Tk] = None
        self.buttons: List[List[tk.Button]] = []
        self.status_label: Optional[tk.Label] = None
        
        self.controller.set_move_callback(self.on_move_made)
        self.controller.set_game_over_callback(self.on_game_over)
    
    def setup_window(self) -> None:
        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe vs AI")
        self.root.resizable(False, False)  # Fixed size, not scalable
        self.root.configure(bg=self.COLOR_BG)
        
        window_width = 450
        window_height = 550
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        self._create_header()
        self._create_board()
        self._create_footer()
    
    def _create_header(self) -> None:
        header_frame = tk.Frame(self.root, bg=self.COLOR_BG)
        header_frame.pack(pady=20)
        
        title_label = tk.Label(
            header_frame,
            text="TIC-TAC-TOE",
            font=("Arial", 28, "bold"),
            bg=self.COLOR_BG,
            fg=self.COLOR_TEXT
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Human vs AI",
            font=("Arial", 12),
            bg=self.COLOR_BG,
            fg="#888888"
        )
        subtitle_label.pack(pady=5)
        
        self.status_label = tk.Label(
            header_frame,
            text="",
            font=("Arial", 16, "bold"),
            bg=self.COLOR_BG,
            fg=self.COLOR_TEXT,
            height=2
        )
        self.status_label.pack(pady=10)
    
    def _create_board(self) -> None:
        """Create the 3x3 grid of square buttons (fixed size, centered)."""
        board_frame = tk.Frame(self.root, bg=self.COLOR_BG)
        board_frame.pack(pady=10)
        
        self.buttons = []
        
        button_size = 100
        
        for row in range(3):
            button_row = []
            for col in range(3):
                button = tk.Button(
                    board_frame,
                    text="",
                    font=("Arial", 40, "bold"),
                    width=button_size,
                    height=button_size,
                    bg=self.COLOR_BUTTON,
                    fg=self.COLOR_TEXT,
                    activebackground=self.COLOR_BUTTON_HOVER,
                    activeforeground=self.COLOR_TEXT,
                    relief=tk.FLAT,
                    bd=0,
                    command=lambda r=row, c=col: self.on_cell_click(r, c)
                )
                button.place(
                    x=col * (button_size + 5),
                    y=row * (button_size + 5),
                    width=button_size,
                    height=button_size
                )
                button_row.append(button)
            self.buttons.append(button_row)
        
        board_frame.config(width=3 * button_size + 2 * 5, height=3 * button_size + 2 * 5)
    
    def _create_footer(self) -> None:
        footer_frame = tk.Frame(self.root, bg=self.COLOR_BG)
        footer_frame.pack(pady=25)
        
        new_game_button = tk.Button(
            footer_frame,
            text="NEW GAME",
            font=("Arial", 14, "bold"),
            bg="#444444",
            fg=self.COLOR_TEXT,
            activebackground="#555555",
            activeforeground=self.COLOR_TEXT,
            width=20,
            height=2,
            relief=tk.FLAT,
            bd=0,
            command=self.start_new_game
        )
        new_game_button.pack()
    
    def on_cell_click(self, row: int, col: int) -> None:
        if self.controller.is_game_active:
            success = self.controller.make_human_move(row, col)
            if success and self.controller.is_game_active:
                self.root.after(300, self._trigger_ai_move)
    
    def on_move_made(self, row: int, col: int, symbol: str) -> None:
        
        button = self.buttons[row][col]
        button.config(
            text=symbol,
            state=tk.DISABLED,
            disabledforeground=self.COLOR_X if symbol == 'X' else self.COLOR_O,
            bg="#1a1a1a"  
        )
        
        if self.controller.is_game_active:
            current_player = self.controller.current_turn_player
            if current_player and current_player.is_human():
                self.status_label.config(
                    text=f"Your Turn ({current_player.symbol})",
                    fg=self.COLOR_X if current_player.symbol == 'X' else self.COLOR_O
                )
            else:
                self.status_label.config(
                    text="AI is thinking...",
                    fg="#FFAA00"
                )
        
        self.root.update()
    
    def _trigger_ai_move(self) -> None:
        if self.controller.is_game_active and self.controller.current_turn_player:
            if self.controller.current_turn_player.is_ai():
                self.controller._make_ai_move()
    
    def on_game_over(self, winner: Optional[Player], is_draw: bool) -> None:

        if is_draw:
            self.status_label.config(text="DRAW!", fg="#FFAA00")
            title = "Draw!"
            message = "It's a draw!\nThe game ended in a tie.\n\nPlay again?"
        else:
            if winner.is_human():
                self.status_label.config(text="YOU WON!", fg="#00FF00")
                title = "Victory!"
                message = f"Congratulations!\nYou won as {winner.symbol}!\n\nPlay again?"
            else:
                self.status_label.config(text="AI WON!", fg="#FF4444")
                title = "Defeat"
                message = f"AI won as {winner.symbol}.\nBetter luck next time!\n\nPlay again?"
        
        self._disable_all_buttons()
        
        self.root.after(500, lambda: self._show_game_over_dialog(message, title))
    
    def _show_game_over_dialog(self, message: str, title: str) -> None:
        play_again = messagebox.askyesno(title, message)
        
        if play_again:
            self.start_new_game()
        else:
            self.root.quit()
    
    def start_new_game(self) -> None:
        choice = self._ask_symbol_choice()
        
        if choice:
            self._reset_board_display()
            
            self.controller.start_new_game(choice)
            
            if self.controller.current_turn_player and self.controller.current_turn_player.is_human():
                self.status_label.config(
                    text=f"Your Turn (X)",
                    fg=self.COLOR_X
                )
            else:
                self.status_label.config(
                    text="AI goes first...",
                    fg=self.COLOR_O
                )
                self.root.after(500, self._trigger_ai_move)
    
    def _ask_symbol_choice(self) -> Optional[str]:

        dialog = tk.Toplevel(self.root)
        dialog.title("Choose Your Symbol")
        dialog.geometry("400x250")
        dialog.resizable(False, False)
        dialog.configure(bg=self.COLOR_BG)
        dialog.transient(self.root)
        dialog.grab_set()
        
        dialog.update_idletasks()
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        x = (screen_width // 2) - 200
        y = (screen_height // 2) - 125
        dialog.geometry(f'+{x}+{y}')
        
        result = [None]
        
        label = tk.Label(
            dialog,
            text="Choose your symbol:",
            font=("Arial", 16, "bold"),
            bg=self.COLOR_BG,
            fg=self.COLOR_TEXT
        )
        label.pack(pady=30)
        
        button_frame = tk.Frame(dialog, bg=self.COLOR_BG)
        button_frame.pack(pady=20)
        
        def choose_x():
            result[0] = 'X'
            dialog.destroy()
        
        def choose_o():
            result[0] = 'O'
            dialog.destroy()
        
        x_button = tk.Button(
            button_frame,
            text="X\n(Go First)",
            font=("Arial", 18, "bold"),
            bg=self.COLOR_BUTTON,
            fg=self.COLOR_X,
            activebackground=self.COLOR_BUTTON_HOVER,
            activeforeground=self.COLOR_X,
            width=10,
            height=3,
            relief=tk.FLAT,
            bd=0,
            command=choose_x
        )
        x_button.pack(side=tk.LEFT, padx=15)
        
        o_button = tk.Button(
            button_frame,
            text="O\n(Go Second)",
            font=("Arial", 18, "bold"),
            bg=self.COLOR_BUTTON,
            fg=self.COLOR_O,
            activebackground=self.COLOR_BUTTON_HOVER,
            activeforeground=self.COLOR_O,
            width=10,
            height=3,
            relief=tk.FLAT,
            bd=0,
            command=choose_o
        )
        o_button.pack(side=tk.LEFT, padx=15)
        
        info_label = tk.Label(
            dialog,
            text="X always makes the first move",
            font=("Arial", 10),
            bg=self.COLOR_BG,
            fg="#888888"
        )
        info_label.pack(pady=15)
        
        self.root.wait_window(dialog)
        return result[0]
    
    def _reset_board_display(self) -> None:
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(
                    text="",
                    state=tk.NORMAL,
                    bg=self.COLOR_BUTTON,
                    fg=self.COLOR_TEXT
                )
    
    def _disable_all_buttons(self) -> None:
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(state=tk.DISABLED)
    
    def run(self) -> None:
        if self.root:
            # Start the first game
            self.start_new_game()
            # Run the main loop
            self.root.mainloop()

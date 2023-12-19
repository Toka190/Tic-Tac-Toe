import tkinter as tk
from tkinter import messagebox
import random

# Constants
EMPTY = ""
PLAYER = "X"
COMPUTER = "O"
WINNING_COMBINATIONS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
    [0, 4, 8], [2, 4, 6]  # Diagonals
]

class TicTacToe:
    def __init__(self):
        self.board = [EMPTY] * 9
        self.current_player = PLAYER
        self.root = tk.Tk()
        self.buttons = []
        self.new_game_button = None

    def start(self):
        self.root.title("Tic Tac Toe")
        self.root.resizable(False, False)

        for i in range(9):
            button = tk.Button(self.root, text=EMPTY, font=("Arial", 20), width=6, height=3, bg="lightblue")
            button.grid(row=i // 3, column=i % 3)
            button.config(command=lambda idx=i: self.make_move(idx))
            button.config(fg="red", disabledforeground="red")
            self.buttons.append(button)

        self.new_game_button = tk.Button(self.root, text="New Game", font=("Arial", 14), width=10, height=3)
        self.new_game_button.grid(row=3, columnspan=3)
        self.new_game_button.config(command=self.reset_game)

        # Player starts first
        self.current_player = PLAYER

        self.root.mainloop()

    def make_move(self, index):
        if self.board[index] == EMPTY:
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player, state="disabled")
            if self.check_winner(self.current_player):
                self.game_over(self.current_player)
            elif EMPTY in self.board:
                self.current_player = COMPUTER
                self.root.after(500, self.computer_move)
            else:
                self.game_over(None)

    def computer_move(self):
        best_move = self.get_best_move()
        self.board[best_move] = COMPUTER
        self.buttons[best_move].config(text=COMPUTER, state="disabled")
        self.current_player = PLAYER
        if self.check_winner(COMPUTER):
            self.game_over(COMPUTER)

    def get_best_move(self):
        best_score = float('-inf')
        best_move = None
        depth = len([cell for cell in self.board if cell == EMPTY])  # Count remaining empty cells

        for move in range(len(self.board)):
            if self.board[move] == EMPTY:
                self.board[move] = COMPUTER
                score = self.minimax(self.board, PLAYER, depth-1)
                self.board[move] = EMPTY
                if score > best_score:
                    best_score = score
                    best_move = move
        return best_move

    def minimax(self, board, player, depth):
        if self.check_winner(PLAYER):
            return -1
        elif self.check_winner(COMPUTER):
            return 1
        elif EMPTY not in board or depth == 0:
            return 0

        scores = []
        for move in range(len(board)):
            if board[move] == EMPTY:
                board[move] = player
                scores.append(self.minimax(board, PLAYER if player == COMPUTER else COMPUTER, depth-1))
                board[move] = EMPTY

        return max(scores) if player == COMPUTER else min(scores)

    def check_winner(self, player):
        for combination in WINNING_COMBINATIONS:
            if all(self.board[idx] == player for idx in combination):
                return True
        return False

    def game_over(self, winner):
        for button in self.buttons:
            button.config(state="disabled")

        if winner is None:
            messagebox.showinfo("Game Over", "It's a tie!")
        else:
            messagebox.showinfo("Game Over", f"{winner} wins!")

        self.new_game_button.config(state="normal")

    def reset_game(self):
        self.board = [EMPTY] * 9
        self.current_player = PLAYER

        for button in self.buttons:
            button.config(text=EMPTY, state="normal")

        # Player starts first
        self.current_player = PLAYER

        self.new_game_button.config(state="disabled")

if __name__ == "__main__":
    game = TicTacToe()
    game.start()
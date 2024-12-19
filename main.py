import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
import random

class TicTacToe:
    def __init__(self, board_size=4):
        self.board_size = board_size
        self.board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.node_counts = {"with_pruning": []}

    def reset(self):
        self.__init__(board_size=self.board_size)

    def check_winner(self):
        size = self.board_size
        lines = []

        # Rows and columns
        for i in range(size):
            lines.append(self.board[i])  # Row
            lines.append([self.board[j][i] for j in range(size)])  # Column

        # Diagonals
        lines.append([self.board[i][i] for i in range(size)])  # Main diagonal
        lines.append([self.board[i][size - i - 1] for i in range(size)])  # Anti-diagonal

        for line in lines:
            if all(cell == self.current_player for cell in line):
                self.game_over = True
                self.winner = self.current_player
                return True

        if all(self.board[r][c] != ' ' for r in range(size) for c in range(size)):
            self.game_over = True
            return True

        return False

    def evaluate(self, difficulty):
        size = self.board_size
        score = 0

        def evaluate_line(line):
            nonlocal score
            x_count = line.count('X')
            o_count = line.count('O')
            empty = line.count(' ')

            if o_count == size:
                score += 1000
            elif x_count == size:
                score -= 1000
            elif difficulty == 'easy':
                # Simplified scoring for easy difficulty
                if o_count == size - 1 and empty == 1:
                    score += 20
                elif x_count == size - 1 and empty == 1:
                    score -= 10
            else:
                # Standard scoring for medium/hard difficulty
                if o_count == size - 1 and empty == 1:
                    score += 50
                elif x_count == size - 1 and empty == 1:
                    score -= 50

        # Evaluate rows, columns, and diagonals
        for i in range(size):
            evaluate_line(self.board[i])
            evaluate_line([self.board[j][i] for j in range(size)])
        evaluate_line([self.board[i][i] for i in range(size)])
        evaluate_line([self.board[i][size - i - 1] for i in range(size)])

        return score

    def minimax(self, depth, maximizing, alpha, beta, difficulty, node_count):
        node_count[0] += 1  # Increment node count
        if depth == 0 or self.game_over:
            return self.evaluate(difficulty)

        best_score = float('-inf') if maximizing else float('inf')

        for r in range(self.board_size):
            for c in range(self.board_size):
                if self.board[r][c] == ' ':
                    self.board[r][c] = 'O' if maximizing else 'X'
                    score = self.minimax(depth - 1, not maximizing, alpha, beta, difficulty, node_count)
                    self.board[r][c] = ' '

                    if maximizing:
                        best_score = max(best_score, score)
                        alpha = max(alpha, best_score)
                    else:
                        best_score = min(best_score, score)
                        beta = min(beta, best_score)

                    if alpha >= beta:
                        break

        return best_score

    def iterative_deepening_minimax(self, max_depth, difficulty):
        best_move = None
        best_score = float('-inf')
        node_count = [0]

        for depth in range(1, max_depth + 1):
            for r in range(self.board_size):
                for c in range(self.board_size):
                    if self.board[r][c] == ' ':
                        self.board[r][c] = 'O'
                        score = self.minimax(depth, False, float('-inf'), float('inf'), difficulty, node_count)
                        self.board[r][c] = ' '

                        if score > best_score:
                            best_score = score
                            best_move = (r, c)

            if abs(best_score) == 1000:  # Early exit if a winning move is found
                break

        self.node_counts["with_pruning"].append(node_count[0])
        return best_move

    def ai_move(self, difficulty):
        if not self.game_over:
            depth_map = {'easy': 1, 'medium': 3, 'hard': 5}
            depth = depth_map.get(difficulty, 3)

            # Add randomness for easy difficulty
            if difficulty == 'easy' and random.random() < 0.5:
                empty_spaces = [(r, c) for r in range(self.board_size) for c in range(self.board_size) if self.board[r][c] == ' ']
                move = random.choice(empty_spaces)
                self.node_counts["with_pruning"].append(0)  # Track 0 nodes for random moves
            else:
                move = self.iterative_deepening_minimax(depth, difficulty)

            if move:
                self.board[move[0]][move[1]] = 'O'
                self.current_player = 'O'


class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("4x4 Tic Tac Toe AI")
        self.master.geometry("800x800")
        self.game = TicTacToe()
        self.difficulty = tk.StringVar(value="medium")
        self.buttons = []

        self.setup_ui()

    def setup_ui(self):
        # Difficulty Selector
        difficulty_frame = tk.Frame(self.master)
        difficulty_frame.pack(pady=10)

        tk.Label(difficulty_frame, text="Difficulty:").pack(side=tk.LEFT)
        for level in ["easy", "medium", "hard"]:
            tk.Radiobutton(difficulty_frame, text=level.capitalize(), variable=self.difficulty, value=level).pack(side=tk.LEFT)

        # Board Buttons
        self.board_frame = tk.Frame(self.master)
        self.board_frame.pack()

        for r in range(4):
            row = []
            for c in range(4):
                button = tk.Button(self.board_frame, text='', width=10, height=5, command=lambda r=r, c=c: self.player_move(r, c))
                button.grid(row=r, column=c)
                row.append(button)
            self.buttons.append(row)

        # Reset Button
        reset_btn = tk.Button(self.master, text="Reset Game", command=self.reset_game)
        reset_btn.pack(pady=10)

        # Plot Button
        plot_btn = tk.Button(self.master, text="Plot Performance", command=self.plot_performance)
        plot_btn.pack(pady=10)

    def player_move(self, r, c):
        if self.game.board[r][c] == ' ' and not self.game.game_over:
            self.game.board[r][c] = 'X'
            self.game.current_player = 'X'
            self.game.check_winner()
            self.update_ui()
            if not self.game.game_over:
                self.master.after(500, self.ai_move)

    def ai_move(self):
        if not self.game.game_over:
            self.game.ai_move(self.difficulty.get())
            self.update_ui()
            if self.game.check_winner():
                self.master.after(100, self.update_ui)

    def update_ui(self):
        for r in range(4):
            for c in range(4):
                text = self.game.board[r][c]
                self.buttons[r][c].config(text=text, fg='blue' if text == 'X' else 'red' if text == 'O' else 'black')

        if self.game.game_over:
            for row in self.buttons:
                for btn in row:
                    btn.config(state=tk.DISABLED)

            if self.game.winner:
                self.master.after(100, lambda: messagebox.showinfo("Game Over", f"{self.game.winner} wins!"))
            else:
                self.master.after(100, lambda: messagebox.showinfo("Game Over", "It's a draw!"))

    def reset_game(self):
        self.game.reset()
        for row in self.buttons:
            for btn in row:
                btn.config(text='', state=tk.NORMAL)

    def plot_performance(self):
        with_pruning = self.game.node_counts["with_pruning"]

        if not with_pruning:
            messagebox.showinfo("No Data", "No AI moves have been made yet to analyze.")
            return

        plt.figure(figsize=(10, 5))
        plt.plot(with_pruning, label="With Alpha-Beta Pruning", marker='o')
        plt.title("Node Evaluations per Move")
        plt.xlabel("Move Number")
        plt.ylabel("Nodes Evaluated")
        plt.legend()
        plt.grid(True)
        plt.show()


def main():
    root = tk.Tk()
    gui = TicTacToeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

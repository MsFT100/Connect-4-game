import numpy as np
import random

def choose_opponent():
    print("Select opponent:")
    print("1: Human")
    print("2: Random AI")
    print("3: Smart AI")
    print("4: Minimax AI")
    choice = input("Enter your choice (1-4): ")
    return {"1": "human", "2": "random", "3": "smart", "4": "minimax"}.get(choice, "human")

class Connect4:
    ROWS = 6
    COLS = 7

    def __init__(self, player2_type="human"):
        self.board = np.full((self.ROWS, self.COLS), ' ', dtype=str)
        self.current_player = '●'  # Player 1 starts
        self.player2_type = player2_type  # "human", "random", "smart", "minimax"

    def print_board(self):
        print("\n".join(["|" + "|".join(row) + "|" for row in self.board]))
        print(" " + " ".join(map(str, range(self.COLS))))

    def drop_disc(self, col):
        if self.board[0][col] != ' ':  # Column full
            return False
        for row in range(self.ROWS - 1, -1, -1):
            if self.board[row][col] == ' ':
                self.board[row][col] = self.current_player
                return row, col  # Return the placed position
        return False

    def check_win(self, player):
        for r in range(self.ROWS):
            for c in range(self.COLS - 3):
                if all(self.board[r, c+i] == player for i in range(4)):
                    return True

        for r in range(self.ROWS - 3):
            for c in range(self.COLS):
                if all(self.board[r+i, c] == player for i in range(4)):
                    return True

        for r in range(self.ROWS - 3):
            for c in range(self.COLS - 3):
                if all(self.board[r+i, c+i] == player for i in range(4)):
                    return True

        for r in range(3, self.ROWS):
            for c in range(self.COLS - 3):
                if all(self.board[r-i, c+i] == player for i in range(4)):
                    return True

        return False

    def switch_player(self):
        self.current_player = '○' if self.current_player == '●' else '●'

    def is_full(self):
        return all(self.board[0, c] != ' ' for c in range(self.COLS))

    def get_random_move(self):
        valid_moves = [c for c in range(self.COLS) if self.board[0][c] == ' ']
        return random.choice(valid_moves)

    def undo_move(self, row, col):
        self.board[row][col] = ' '

    def minimax(self, depth, maximizingPlayer, alpha, beta):
        if self.check_win('○'):
            return 100 - depth
        if self.check_win('●'):
            return -100 + depth
        if self.is_full() or depth == 0:
            return self.evaluate_board()

        valid_moves = [c for c in range(self.COLS) if self.board[0][c] == ' ']
        valid_moves.sort(key=lambda x: abs(3 - x))

        if maximizingPlayer:
            max_eval = -float('inf')
            for col in valid_moves:
                row, = self.drop_disc(col)
                eval = self.minimax(depth - 1, False, alpha, beta)
                self.undo_move(row,col)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for col in valid_moves:
                row, = self.drop_disc(col)
                eval = self.minimax(depth - 1, True, alpha, beta)
                self.undo_move(row, col)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_minimax_move(self, depth=6):
        best_score = -float('inf')
        best_col = None
        valid_moves = [c for c in range(self.COLS) if self.board[0][c] == ' ']
        valid_moves.sort(key=lambda x: abs(3 - x))

        for col in valid_moves:
            row, = self.drop_disc(col)
            score = self.minimax(depth - 1, False, -float('inf'), float('inf'))
            self.undo_move(row, col)

            if score > best_score:
                best_score = score
                best_col = col

        return best_col
    def play(self):
        while True:
            self.print_board()
            if self.current_player == '○':
                if self.player2_type == "random":
                    col = self.get_random_move()
                    print(f"AI (Random) chooses column {col}")
                elif self.player2_type == "smart":
                    col = self.get_smart_move()
                    print(f"AI (Smart) chooses column {col}")
                elif self.player2_type == "minimax":
                    col = self.get_minimax_move()
                    print(f"AI (Minimax) chooses column {col}")
                else:
                    col = int(input(f"Player {self.current_player}, choose a column (0-{self.COLS-1}): "))
            else:
                col = int(input(f"Player {self.current_player}, choose a column (0-{self.COLS-1}): "))

            if 0 <= col < self.COLS and self.board[0][col] == ' ':
                row, _ = self.drop_disc(col)
                if self.check_win(self.current_player):
                    self.print_board()
                    print(f"Player {self.current_player} wins!")
                    break
                elif self.is_full():
                    self.print_board()
                    print("Game ends in a draw!")
                    break
                self.switch_player()
            else:
                print("Invalid move, try again.")

    def evaluate_board(self):
        score = 0

        if self.check_win('○'):
            return 1000  # AI wins
        elif self.check_win('●'):
            return -1000  # Human wins

        center_column = [self.board[r][self.COLS // 2] for r in range(self.ROWS)]
        score += center_column.count('○') * 3  # Center preference

        return score

    def get_smart_move(self):
        for col in range(self.COLS):
            if self.drop_disc(col):
                if self.check_win(self.current_player):
                    self.board[np.where(self.board == self.current_player)[0][-1], col] = ' '
                    return col
                self.board[np.where(self.board == self.current_player)[0][-1], col] = ' '

        for col in range(self.COLS):
            if self.drop_disc(col):
                self.switch_player()
                if self.check_win(self.current_player):
                    self.switch_player()
                    self.board[np.where(self.board == self.current_player)[0][-1], col] = ' '
                    return col
                self.switch_player()
                self.board[np.where(self.board == self.current_player)[0][-1], col] = ' '

        return self.get_random_move()



if __name__ == "__main__":
    opponent = choose_opponent()
    game = Connect4(player2_type=opponent)
    game.play()

import numpy as np

# Game Constants
ROWS, COLS = 6, 7
SQUARESIZE = 80
RADIUS = SQUARESIZE // 2 - 5

class Connect4Game:
    def __init__(self):
        self.board = np.full((ROWS, COLS), ' ', dtype=str)
        self.turn = 0  # 0 for Player 1 (Red), 1 for Player 2 (Yellow)
        self.game_over = False

    def get_board_state(self):
        """Returns the board state as a numerical array."""
        mapping = {' ': 0, '●': 1, '○': -1}  # Convert symbols to numbers
        return np.vectorize(mapping.get)(self.board)  # Convert board to numbers

    def get_valid_columns(self):
        """Returns a list of columns that are not full."""
        return [c for c in range(COLS) if self.board[0][c] == ' ']

    def copy(self):
        """Creates a deep copy of the game state for simulation purposes."""
        new_game = Connect4Game()
        new_game.board = np.copy(self.board)
        new_game.turn = self.turn
        new_game.game_over = self.game_over
        return new_game

    def get_lowest_empty_row(self, col):
        """Returns the lowest available row in a column."""
        for r in range(ROWS-1, -1, -1):
            if self.board[r][col] == ' ':
                return r
        return None  # Column full

    def drop_piece(self, col, piece=None):
        """Places a piece in the given column and checks for a win."""
        if self.game_over:
            return False  # No more moves allowed

        row = self.get_lowest_empty_row(col)
        if row is not None:
            piece = piece if piece else ('●' if self.turn == 0 else '○')
            self.board[row][col] = piece
            if self.check_winner(row, col, piece):
                self.game_over = True
                return piece  # Return the winning piece

            self.turn = 1 - self.turn  # Switch turns
            return True  # Move was successful
        return False  # Invalid move

    def check_winner(self, row, col, piece):
        """Checks if placing a piece at (row, col) wins the game."""
        return (self.check_direction(row, col, piece, 1, 0) or  # Vertical
                self.check_direction(row, col, piece, 0, 1) or  # Horizontal
                self.check_direction(row, col, piece, 1, 1) or  # Diagonal /
                self.check_direction(row, col, piece, 1, -1))   # Diagonal \

    def check_winner_piece(self, piece):
        """Checks if a given piece has won the game."""
        for r in range(ROWS):
            for c in range(COLS):
                if self.board[r][c] == piece:
                    if (self.check_direction(r, c, piece, 1, 0) or  # Vertical
                            self.check_direction(r, c, piece, 0, 1) or  # Horizontal
                            self.check_direction(r, c, piece, 1, 1) or  # Diagonal /
                            self.check_direction(r, c, piece, 1, -1)):  # Diagonal \
                        return True
        return False


    def check_direction(self, row, col, piece, dr, dc):
        """Checks 4 in a row in a given direction."""
        count = 1  # Include the current piece
        # Check one direction
        for i in range(1, 4):
            r, c = row + dr * i, col + dc * i
            if 0 <= r < ROWS and 0 <= c < COLS and self.board[r][c] == piece:
                count += 1
            else:
                break
        # Check the opposite direction
        for i in range(1, 4):
            r, c = row - dr * i, col - dc * i
            if 0 <= r < ROWS and 0 <= c < COLS and self.board[r][c] == piece:
                count += 1
            else:
                break
        return count >= 4  # Win if 4 or more in a row

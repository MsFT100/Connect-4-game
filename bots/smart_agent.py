import random
from connect_4_game import Connect4Game

class SmartAI:
    def __init__(self, piece):
        self.piece = piece  # '●' for Player 1, '○' for Player 2

    def get_move(self, game: Connect4Game):
        """Returns the best move based on simple rules."""
        valid_moves = [col for col in range(7) if game.get_lowest_empty_row(col) is not None]
        opponent_piece = '●' if self.piece == '○' else '○'

        # Rule 1: Check if it can win
        for col in valid_moves:
            temp_game = game.copy()
            row = temp_game.get_lowest_empty_row(col)
            if row is not None:
                temp_game.board[row][col] = self.piece
                if temp_game.check_winner(row, col, self.piece):  # ✅ Fix: Pass row, col, and piece
                    return col  # Play winning move

        # Rule 2: Block opponent's win
        for col in valid_moves:
            temp_game = game.copy()
            row = temp_game.get_lowest_empty_row(col)
            if row is not None:
                temp_game.board[row][col] = opponent_piece
                if temp_game.check_winner(row, col, opponent_piece):  # ✅ Fix: Pass row, col, and piece
                    return col  # Block opponent's win

        # Rule 3: Prioritize center column
        if 3 in valid_moves:
            return 3

        # Rule 4: Choose a move that builds a two-in-a-row setup
        for col in valid_moves:
            row = game.get_lowest_empty_row(col)
            if row is not None:
                temp_game = game.copy()
                temp_game.board[row][col] = self.piece  # Simulate move
                if temp_game.check_winner(row, col, self.piece):  # ✅ Fix: Pass row, col, and piece
                    return col

        # Rule 5: Pick a random valid move if no better option
        return random.choice(valid_moves)

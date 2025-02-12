import random
import math
from connect_4_game import Connect4Game

class MiniMaxAI:
    def __init__(self, piece, depth=6):
        self.piece = piece  # '●' or '○'
        self.depth = depth
        self.opponent_piece = '●' if piece == '○' else '○'

    def evaluate_position(self, game):
        """Returns a score based on board evaluation."""
        if game.check_winner_piece(self.piece):
            return 10000
        elif game.check_winner_piece(self.opponent_piece):
            return -10000
        return 0  # Neutral state

    def minimax(self, game, depth, alpha, beta, maximizing_player):
        valid_columns = game.get_valid_columns()
        is_terminal = game.check_winner_piece(self.piece) or game.check_winner_piece(self.opponent_piece) or len(valid_columns) == 0

        if depth == 0 or is_terminal:
            return None, self.evaluate_position(game)

        if maximizing_player:
            value = -math.inf
            best_column = random.choice(valid_columns)
            for col in valid_columns:
                temp_game = game.copy()
                temp_game.drop_piece(col, self.piece)
                _, new_score = self.minimax(temp_game, depth-1, alpha, beta, False)
                if new_score > value:
                    value = new_score
                    best_column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return best_column, value
        else:
            value = math.inf
            best_column = random.choice(valid_columns)
            for col in valid_columns:
                temp_game = game.copy()
                temp_game.drop_piece(col, self.opponent_piece)
                _, new_score = self.minimax(temp_game, depth-1, alpha, beta, True)
                if new_score < value:
                    value = new_score
                    best_column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return best_column, value

    def get_move(self, game: Connect4Game):
        """Returns the best move using Minimax algorithm."""
        best_col, _ = self.minimax(game, self.depth, -math.inf, math.inf, True)
        return best_col

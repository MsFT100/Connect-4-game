import random

class RandomAI:
    def __init__(self, piece):
        self.piece = piece

    def get_move(self, game):
        """Returns a random valid column."""
        valid_columns = [c for c in range(7) if game.get_lowest_empty_row(c) is not None]
        return random.choice(valid_columns) if valid_columns else None

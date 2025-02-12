class HumanPlayer:
    def __init__(self, piece):
        self.piece = piece  # '●' for Player 1, '○' for Player 2

    def get_move(self, game):
        """The GUI handles human input, so this class may be optional."""
        pass  # GUI will manage this directly

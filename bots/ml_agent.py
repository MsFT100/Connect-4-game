import joblib
import numpy as np
import pandas as pd

class MLAgent:
    def __init__(self, model_path, piece):
        """Initialize the ML agent by loading the trained model."""
        self.model = joblib.load(model_path)  # Load saved ML model
        self.piece = piece

    def get_move(self, game):
        """Predict the best move using the trained ML model."""
        # Convert board state to DataFrame with correct feature names
        board_state = np.array(game.get_board_state()).flatten()
        column_names = [f"col_{i}" for i in range(42)]
        board_state_df = pd.DataFrame([board_state], columns=column_names)

        # Predict the best column to drop the piece in
        predicted_move = self.model.predict(board_state_df)[0]  # Extract single prediction

        # Ensure the move is valid
        valid_moves = game.get_valid_columns()
        if predicted_move not in valid_moves:
            predicted_move = np.random.choice(valid_moves)  # Fallback if prediction is invalid

        return predicted_move

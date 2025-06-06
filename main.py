import pygame

from bots.minimax_agent import MiniMaxAI
from bots.ml_agent import MLAgent
from bots.random_agent import RandomAgent
from bots.smart_agent import SmartAgent
from connect_4_game import Connect4Game
from bots.human_player import HumanPlayer

# Constants
ROWS, COLS = 6, 7
SQUARESIZE = 80
RADIUS = SQUARESIZE // 2 - 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
HIGHLIGHT = (100, 100, 255)
path = "ml_training/connect4_ml_agent.pkl"
class Connect4GUI:
    def __init__(self, player1, player2):
        pygame.init()
        self.width = COLS * SQUARESIZE
        self.height = (ROWS + 1) * SQUARESIZE
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Connect 4")

        self.game = Connect4Game()
        self.players = [player1, player2]
        self.hover_column = None

    def draw_board(self):
        self.screen.fill(BLACK)
        if self.hover_column is not None:
            pygame.draw.rect(self.screen, HIGHLIGHT,
                             (self.hover_column * SQUARESIZE, 0, SQUARESIZE, (ROWS + 1) * SQUARESIZE))

        for r in range(ROWS):
            for c in range(COLS):
                pygame.draw.rect(self.screen, BLUE, (c * SQUARESIZE, (r+1) * SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(self.screen, WHITE, (c * SQUARESIZE + SQUARESIZE//2, (r+1) * SQUARESIZE + SQUARESIZE//2), RADIUS)

        for r in range(ROWS):
            for c in range(COLS):
                if self.game.board[r][c] == '●':
                    pygame.draw.circle(self.screen, (255, 0, 0), (c * SQUARESIZE + SQUARESIZE//2, (r+1) * SQUARESIZE + SQUARESIZE//2), RADIUS)
                elif self.game.board[r][c] == '○':
                    pygame.draw.circle(self.screen, (255, 255, 0), (c * SQUARESIZE + SQUARESIZE//2, (r+1) * SQUARESIZE + SQUARESIZE//2), RADIUS)

        pygame.display.update()

    def show_dialog(self, message):
        """Displays a game over message and waits for user input."""
        font = pygame.font.Font(None, 50)
        text_surface = font.render(message, True, WHITE)

        dialog_width, dialog_height = 400, 150
        dialog_x = (self.width - dialog_width) // 2
        dialog_y = (self.height - dialog_height) // 2

        pygame.draw.rect(self.screen, BLACK, (dialog_x, dialog_y, dialog_width, dialog_height), border_radius=10)
        pygame.draw.rect(self.screen, WHITE, (dialog_x, dialog_y, dialog_width, dialog_height), 3, border_radius=10)

        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(text_surface, text_rect)

        pygame.display.update()
        pygame.time.delay(330)
        pygame.quit()

        # Show for 3 seconds

    def run(self):
        self.draw_board()
        running = True

        while running:
            current_player = self.players[self.game.turn]

            if isinstance(current_player, HumanPlayer):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEMOTION:
                        self.hover_column = event.pos[0] // SQUARESIZE
                        self.draw_board()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        col = event.pos[0] // SQUARESIZE
                        self.process_move(col)
            else:
                pygame.time.delay(500)  # AI move delay
                col = current_player.get_move(self.game)
                if col is not None:
                    self.process_move(col)

        pygame.quit()

    def process_move(self, col):
        row = self.game.get_lowest_empty_row(col)
        if row is not None:
            piece = '●' if self.game.turn == 0 else '○'
            self.animate_falling_piece(row, col, piece)
            result = self.game.drop_piece(col)
            self.draw_board()
            if self.game.game_over:
                winner_text = f"{'Player 1 (Red) Wins' if result == '●' else 'Player 2 (Yellow) Wins'}"
                self.show_dialog(winner_text)



    def animate_falling_piece(self, row, col, piece):
        y_pos = SQUARESIZE // 2
        color = (255, 0, 0) if piece == '●' else (255, 255, 0)
        while y_pos < (row+1) * SQUARESIZE + SQUARESIZE//2:
            self.draw_board()
            pygame.draw.circle(self.screen, color, (col * SQUARESIZE + SQUARESIZE//2, y_pos), RADIUS)
            pygame.display.update()
            y_pos += 10
            pygame.time.delay(20)

import pygame

def show_selection_screen():
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Select Game Mode")

    font = pygame.font.Font(None, 30)  # Adjust font size
    options = [
        "1. Human vs Human",
        "2. Human vs Random AI",
        "3. Human vs Smart AI",
        "4. Random AI vs Smart AI",
        "5. Smart AI vs Smart AI",
        "6. Minimax AI vs Human",
        "7. Minimax AI vs Random AI",
        "8. Minimax AI vs Smart AI",
        "9. Minimax AI vs Minimax AI",
        "10. Human vs ML Agent",
        "11. ML Agent vs Minimax AI"
    ]

    selected_index = 0  # Track highlighted option
    BLACK, WHITE, YELLOW = (0, 0, 0), (255, 255, 255), (255, 255, 0)

    while True:
        screen.fill(BLACK)

        for i, text in enumerate(options):
            # Highlight selected option in yellow
            color = YELLOW if i == selected_index else WHITE
            text_surface = font.render(text, True, color)
            screen.blit(text_surface, (50, 50 + i * 40))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:  # Move down
                    selected_index = (selected_index + 1) % len(options)
                elif event.key == pygame.K_UP:  # Move up
                    selected_index = (selected_index - 1) % len(options)
                elif event.key == pygame.K_RETURN:  # Confirm selection
                    return selected_index + 1  # Return selection (1-based index)


if __name__ == "__main__":
    mode = show_selection_screen()

    if mode == 1:
        player1 = HumanPlayer('●')
        player2 = HumanPlayer('○')
    elif mode == 2:
        player1 = HumanPlayer('●')
        player2 = RandomAgent('○')
    elif mode == 3:
        player1 = HumanPlayer('●')
        player2 = SmartAgent('○')
    elif mode == 4:
        player1 = RandomAgent('●')
        player2 = SmartAgent('○')
    elif mode == 5:
        player1 = SmartAgent('●')
        player2 = SmartAgent('○')
    elif mode == 6:
        player1 = MiniMaxAI('●')
        player2 = HumanPlayer('○')
    elif mode == 7:
        player1 = MiniMaxAI('●')
        player2 = RandomAgent('○')
    elif mode == 8:
        player1 = MiniMaxAI('●')
        player2 = SmartAgent('○')
    elif mode == 9:
        player1 = MiniMaxAI('●')
        player2 = MiniMaxAI('○')
    elif mode == 10:
        player1 = HumanPlayer('●')
        player2 = MLAgent(path,'○')
    elif mode == 11:
        player1 = MLAgent(path,'●')
        player2 = MiniMaxAI('○')


game_gui = Connect4GUI(player1, player2)
game_gui.run()



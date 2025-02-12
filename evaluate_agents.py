import time
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

from bots.minimax_agent import MiniMaxAI
from bots.ml_agent import MLAgent
from bots.random_agent import RandomAgent
from bots.smart_agent import SmartAgent
from connect_4_game import Connect4Game


class PerformanceEvaluator:
    def __init__(self, agent1, agent2, game_class, num_games=500):
        """Initialize evaluation between two agents."""
        self.agent1 = agent1
        self.agent2 = agent2
        self.game_class = game_class
        self.num_games = num_games
        self.results = {
            "Agent1 Wins": 0,
            "Agent2 Wins": 0,
            "Draws": 0,
            "Game Lengths": [],
            "Execution Times": [],
        }
        self.search_metrics = defaultdict(list)  # Store Minimax search metrics

    def run_games(self):
        """Run multiple games and collect performance metrics."""
        for game_num in range(self.num_games):
            game = self.game_class()  # Initialize new game
            agents = [self.agent1, self.agent2]
            current_agent_idx = 0
            move_count = 0
            start_time = time.time()

            while not game.game_over:
                agent = agents[current_agent_idx]
                move = agent.get_move(game)  # Get move from agent
                game.drop_piece(move)


                move_count += 1
                current_agent_idx = 1 - current_agent_idx  # Switch agent

                # If Minimax, track search depth & nodes expanded
                if hasattr(agent, "last_search_depth"):
                    self.search_metrics["Depth"].append(agent.last_search_depth)
                    self.search_metrics["Nodes Expanded"].append(agent.last_nodes_expanded)

            # Collect results
            game_duration = time.time() - start_time
            self.results["Execution Times"].append(game_duration)
            self.results["Game Lengths"].append(move_count)

            #Determine a winner if any
            winner, winner_agent = None, None

            if game.check_winner_piece('●'):
                print(f"Game {game_num+1}: Red (●) is detected as the winner!")
                print(game.board)  # Debugging
                winner = 'Red'
                winner_agent = self.agent1 if self.agent1.piece == 1 else self.agent2
            elif game.check_winner_piece('○'):
                print(f"Game {game_num+1}: Yellow (○) is detected as the winner!")
                print(game.board)  # Debugging
                winner = 'Yellow'
                winner_agent = self.agent1 if self.agent1.piece == 1 else self.agent2
            else:
                print(f"Game {game_num+1}: No winner detected.")
                print(game.board)  # Debugging
                winner = None

            if winner_agent:
                print(f"Game {game_num+1}: {winner} ({winner_agent.__class__.__name__}) is detected as the winner!")
            else:
                print(f"Game {game_num+1}: No winner detected.")



            piece_to_color = {self.agent1.piece: "Red", self.agent2.piece: "Yellow"}

            if winner == piece_to_color.get(self.agent1.piece):
                self.results["Agent1 Wins"] += 1
            elif winner == piece_to_color.get(self.agent2.piece):
                self.results["Agent2 Wins"] += 1
            else:
                self.results["Draws"] += 1
            #print(f"Agent 1: {self.agent1.__class__.__name__} ({self.agent1.piece})")
            #print(f"Agent 2: {self.agent2.__class__.__name__} ({self.agent2.piece})")


            print(f"Game {game_num+1}/{self.num_games} completed. Winner: {winner} ({winner_agent.__class__.__name__ if winner_agent else 'None'})")

    def display_results(self):
        """Print and visualize the performance metrics."""
        total_games = self.num_games
        win_rate_agent1 = (self.results["Agent1 Wins"] / total_games) * 100
        win_rate_agent2 = (self.results["Agent2 Wins"] / total_games) * 100
        draw_rate = (self.results["Draws"] / total_games) * 100

        # Get agent names
        agent1_name = self.agent1.__class__.__name__
        agent2_name = self.agent2.__class__.__name__

        print("\n--- Performance Summary ---")
        print(f"{agent1_name} Wins: {self.results['Agent1 Wins']} ({win_rate_agent1:.2f}%)")
        print(f"{agent2_name} Wins: {self.results['Agent2 Wins']} ({win_rate_agent2:.2f}%)")
        print(f"Draws: {self.results['Draws']} ({draw_rate:.2f}%)")
        print(f"Avg. Game Length: {np.mean(self.results['Game Lengths']):.2f} moves")
        print(f"Avg. Execution Time: {np.mean(self.results['Execution Times']):.4f} sec")

        # Plot win/loss/draw rates
        labels = [f"{agent1_name} Wins", f"{agent2_name} Wins", "Draws"]
        values = [self.results["Agent1 Wins"], self.results["Agent2 Wins"], self.results["Draws"]]

        plt.figure(figsize=(7, 5))
        plt.bar(labels, values, color=["blue", "red", "gray"])
        plt.title(f"{agent1_name} (Red) vs {agent2_name} (Yellow) - Win/Loss/Draw Rates")
        plt.xlabel("Outcome")
        plt.ylabel("Count")
        plt.show()

        # Search Performance Metrics (only for Minimax)
        if self.search_metrics["Depth"]:
            plt.figure(figsize=(7, 5))
            plt.hist(self.search_metrics["Depth"], bins=10, color="purple", alpha=0.7, label="Search Depth")
            plt.hist(self.search_metrics["Nodes Expanded"], bins=10, color="orange", alpha=0.7, label="Nodes Expanded")
            plt.title(f"{agent1_name} vs {agent2_name} - Minimax Search Metrics")
            plt.xlabel("Value")
            plt.ylabel("Frequency")
            plt.legend()
            plt.show()


# --- RUNNING THE EXPERIMENTS ---
if __name__ == "__main__":
    # Initialize agents
    random_agent = RandomAgent('●')
    smart_agent_game_one = SmartAgent('●')
    smart_agent_game_two = SmartAgent('○')
    minimax_agent_one = MiniMaxAI('●', depth=6)
    minimax_agent_two = MiniMaxAI('○', depth=6)
    ml_agent = MLAgent("ml_training/connect4_ml_agent.pkl", '○')

    # Run evaluations
    evaluator1 = PerformanceEvaluator(random_agent, smart_agent_game_two, Connect4Game, num_games=500)
    evaluator1.run_games()
    evaluator1.display_results()

    evaluator2 = PerformanceEvaluator(smart_agent_game_one, minimax_agent_two, Connect4Game, num_games=500)
    evaluator2.run_games()
    evaluator2.display_results()

    evaluator3 = PerformanceEvaluator(ml_agent,minimax_agent_one, Connect4Game, num_games=500)
    evaluator3.run_games()
    evaluator3.display_results()

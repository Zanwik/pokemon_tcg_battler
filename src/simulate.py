import logging
import random
import csv
from collections import defaultdict

from src.card import standard_pokemon_cards, standard_trainer_cards
from src.player import Player
from src.game import Game
from src.ai import AIPlayer, build_balanced_deck

archetype_win_stats = defaultdict(int)

def run_simulation(num_games=100):
    global archetype_win_stats

    for _ in range(num_games):
        archetype1 = random.choice(["Control", "Aggro", "Stall"])
        archetype2 = random.choice(["Control", "Aggro", "Stall"])

        deck1 = build_balanced_deck(archetype1)
        deck2 = build_balanced_deck(archetype2)

        ai_ash = Player("AI-Ash", deck1)
        ai_misty = Player("AI-Misty", deck2)

        game = Game(ai_ash, ai_misty, ai_enabled=True)
        winner = None

        while not game.play_turn():
            pass  

        if ai_ash.prize_cards == 0:
            winner = "AI-Ash"
            archetype_win_stats[archetype1] += 1
        elif ai_misty.prize_cards == 0:
            winner = "AI-Misty"
            archetype_win_stats[archetype2] += 1

    save_archetype_results(archetype_win_stats)

def save_archetype_results(stats):
    """ Saves AI archetype performance to CSV for analysis. """
    with open("archetype_performance.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Archetype", "Wins"])
        for archetype, wins in stats.items():
            writer.writerow([archetype, wins])
    logging.info("📊 AI archetype performance saved.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_simulation(100)

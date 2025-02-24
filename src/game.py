import tkinter as tk
from tkinter import scrolledtext, Canvas, messagebox
import random
import threading
import time
from PIL import Image, ImageTk
from src.game import Game
from src.player import Player
from src.card import standard_pokemon_cards

IMAGE_FOLDER = "images/"  # Ensure this folder contains Pokémon & Trainer images

class BattleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokémon TCG AI Battle")
        self.root.geometry("1200x750")
        
        self.simulation_running = False
        self.card_images = {}
        
        # Title Label
        self.title_label = tk.Label(self.root, text="AI Pokémon TCG Battle", font=("Arial", 18, "bold"))
        self.title_label.pack(pady=10)
        
        # Input for number of matches
        self.match_label = tk.Label(self.root, text="Number of Matches:", font=("Arial", 12))
        self.match_label.pack()
        self.match_entry = tk.Entry(self.root, font=("Arial", 12), width=5)
        self.match_entry.pack(pady=5)
        self.match_entry.insert(0, "1")
        
        # Game Board Canvas
        self.battle_canvas = Canvas(self.root, width=1100, height=500, bg="lightgray")
        self.battle_canvas.pack(pady=10)
        
        # Create Game Board Sections
        self.create_game_board_areas()
        
        # Battle Log
        self.battle_log = scrolledtext.ScrolledText(self.root, width=100, height=10, wrap=tk.WORD)
        self.battle_log.pack(pady=10)
        
        # Control Buttons
        self.start_button = tk.Button(self.root, text="Start Battle", command=self.start_battle, font=("Arial", 12), bg="green", fg="white")
        self.start_button.pack(pady=5)
        
        self.end_button = tk.Button(self.root, text="End Battle", command=self.end_battle, font=("Arial", 12), bg="orange", fg="black")
        self.end_button.pack(pady=5)
        
        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit, font=("Arial", 12), bg="red", fg="white")
        self.exit_button.pack(pady=5)

    def create_game_board_areas(self):
        """ Creates labeled sections for Pokémon TCG gameplay """
        
        # AI-Ash (Top Section)
        self.active_pokemon_p1 = self.create_card_area(500, 120, "Active Pokémon")
        self.bench_pokemon_p1 = self.create_card_area(300, 120, "Bench")
        self.deck_p1 = self.create_card_area(800, 120, "Deck")
        self.discard_pile_p1 = self.create_card_area(850, 120, "Discard Pile")
        self.prize_cards_p1 = self.create_card_area(50, 120, "Prize Cards")
        self.hand_p1 = self.create_card_area(300, 180, "Hand")

        # AI-Misty (Bottom Section)
        self.active_pokemon_p2 = self.create_card_area(500, 380, "Active Pokémon")
        self.bench_pokemon_p2 = self.create_card_area(300, 380, "Bench")
        self.deck_p2 = self.create_card_area(800, 380, "Deck")
        self.discard_pile_p2 = self.create_card_area(850, 380, "Discard Pile")
        self.prize_cards_p2 = self.create_card_area(50, 380, "Prize Cards")
        self.hand_p2 = self.create_card_area(300, 440, "Hand")

    def create_card_area(self, x, y, text):
        """ Creates card areas for displaying Pokémon & Trainer images """
        rect = self.battle_canvas.create_rectangle(x, y, x + 200, y + 60, outline="black", fill="white")
        label = self.battle_canvas.create_text(x + 100, y + 30, text=text, font=("Arial", 10))
        return {"rect": rect, "label": label}

    def log_message(self, message):
        """ Logs battle events to the GUI """
        self.battle_log.insert(tk.END, message + "\n")
        self.battle_log.yview(tk.END)

    def start_battle(self):
        """ Starts a new AI vs AI battle in a separate thread. """
        self.simulation_running = True
        self.battle_log.delete(1.0, tk.END)
        self.log_message("⚔️ AI Battle Started!")

        num_matches = int(self.match_entry.get())
        battle_thread = threading.Thread(target=self.run_battle, args=(num_matches,))
        battle_thread.start()

    def run_battle(self, num_matches):
        """ Runs AI battle simulation with real-time GUI updates. """
        for match in range(num_matches):
            if not self.simulation_running:
                break

            self.log_message(f"⚡ Match {match + 1} Begins!")
            self.player1 = Player("AI-Ash", random.sample(standard_pokemon_cards, 20))
            self.player2 = Player("AI-Misty", random.sample(standard_pokemon_cards, 20))
            self.game = Game(self.player1, self.player2, ai_enabled=True)

            while not self.game.play_turn():
                if not self.simulation_running:
                    break
                time.sleep(1)
                self.update_board()

            if self.simulation_running:
                self.log_message(f"🏆 {self.game.players[self.game.turn % 2].name} Wins the Battle!")
                messagebox.showinfo("Game Over", f"{self.game.players[self.game.turn % 2].name} Wins!")

    def end_battle(self):
        """ Ends the AI battle simulation early. """
        self.simulation_running = False
        self.log_message("⏹️ Battle Simulation Ended!")

    def update_board(self):
        """ Updates the displayed Pokémon and Trainer card images for all areas. """
        self.display_cards(self.player1.hand, self.hand_p1)
        self.display_cards(self.player2.hand, self.hand_p2)
        self.display_cards([self.player1.active_pokemon], self.active_pokemon_p1)
        self.display_cards([self.player2.active_pokemon], self.active_pokemon_p2)

    def display_cards(self, cards, area):
        """ Displays Pokémon & Trainer card images in the specified game area. """
        if not cards or cards[0] is None:
            self.battle_canvas.itemconfig(area["rect"], fill="white")
            return

        self.battle_canvas.itemconfig(area["rect"], fill="yellow")

if __name__ == "__main__":
    root = tk.Tk()
    app = BattleGUI(root)
    root.mainloop()

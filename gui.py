import tkinter as tk
from tkinter import scrolledtext, Canvas, PhotoImage, messagebox
import random
import threading
import time
import sys
import traceback
from PIL import Image, ImageTk
from src.simulate import run_simulation
from src.player import Player
from src.card import standard_pokemon_cards, standard_trainer_cards
from src.reinforcements import RLModel

IMAGE_FOLDER = "images/"

class BattleGUI:
    def __init__(self, root):
        try:
            self.root = root
            self.root.title("Pokémon TCG AI Battle")
            self.root.geometry("1920x1080")
            self.root.configure(bg="black")
            self.root.state("zoomed")

            self.simulation_running = False
            self.card_images = {}
            self.rl_model = RLModel()

            sys.stderr = self.ErrorLogger(self)

            self.title_label = tk.Label(self.root, text="AI Pokémon TCG Battle", font=("Arial", 20, "bold"), bg="black", fg="white")
            self.title_label.pack(pady=10)

            self.match_frame = tk.Frame(self.root, bg="black")
            self.match_frame.pack(pady=5)

            self.match_label = tk.Label(self.match_frame, text="Number of Matches:", font=("Arial", 14), bg="black", fg="white")
            self.match_label.pack(side=tk.LEFT, padx=10)

            self.match_entry = tk.Entry(self.match_frame, font=("Arial", 14), width=5)
            self.match_entry.pack(side=tk.LEFT)
            self.match_entry.insert(0, "1")

            self.battle_canvas = Canvas(self.root, width=1600, height=700, bg="black")
            self.battle_canvas.pack(pady=10, expand=True, fill=tk.BOTH)

            self.hp_bar_p1 = self.battle_canvas.create_rectangle(100, 250, 300, 270, fill="green")
            self.hp_bar_p2 = self.battle_canvas.create_rectangle(500, 250, 700, 270, fill="green")

            self.battle_log = scrolledtext.ScrolledText(self.root, width=100, height=10, wrap=tk.WORD, font=("Arial", 12), bg="black", fg="white")
            self.battle_log.pack(pady=10, expand=True, fill=tk.BOTH)

            self.error_log = scrolledtext.ScrolledText(self.root, width=100, height=5, wrap=tk.WORD, font=("Arial", 12), bg="black", fg="red")
            self.error_log.pack(pady=10, expand=True, fill=tk.BOTH)

            self.button_frame = tk.Frame(self.root, bg="black")
            self.button_frame.pack(pady=10)

            self.start_button = tk.Button(self.button_frame, text="Start Battle", command=self.start_battle, font=("Arial", 14, "bold"), bg="green", fg="white")
            self.start_button.pack(side=tk.LEFT, padx=10)

            self.exit_button = tk.Button(self.button_frame, text="Exit Game", command=self.root.quit, font=("Arial", 14, "bold"), bg="blue", fg="white")
            self.exit_button.pack(side=tk.LEFT, padx=10)

            self.log_message("✅ GUI Initialized Successfully.")

        except Exception as e:
            self.log_error(f"GUI Init Error: {str(e)}")

    def start_battle(self):
        try:
            self.simulation_running = True
            self.battle_log.delete(1.0, tk.END)
            self.error_log.delete(1.0, tk.END)
            self.log_message("⚔️ AI Battle Started!")
            num_matches = int(self.match_entry.get())
            battle_thread = threading.Thread(target=self.run_battle, args=(num_matches,))
            battle_thread.start()
        except Exception as e:
            self.log_error(f"Start Battle Error: {str(e)}")

    def run_battle(self, num_matches):
        try:
            for match in range(num_matches):
                if not self.simulation_running:
                    break
                
                self.log_message(f"⚡ Match {match + 1} Begins!")
                self.player1 = Player("AI-Ash", random.sample(standard_pokemon_cards, 10))
                self.player2 = Player("AI-Misty", random.sample(standard_pokemon_cards, 10))
                self.game = run_simulation(1)
                
                self.load_pokemon_images(self.player1.active_pokemon.name, self.player2.active_pokemon.name)

                while not self.game.play_turn():
                    time.sleep(1)
                    self.update_hp_bars()
                    self.log_message(f"🎮 {self.game.players[self.game.current_player].name}'s Turn!")

                self.log_message(f"🏆 {self.game.players[self.game.current_player].name} Wins the Battle!")
        except Exception as e:
            self.log_error(f"Battle Error: {str(e)}")

    def load_pokemon_images(self, p1_pokemon, p2_pokemon):
        try:
            p1_image = Image.open(f"{IMAGE_FOLDER}{p1_pokemon}.png").resize((150, 150))
            p2_image = Image.open(f"{IMAGE_FOLDER}{p2_pokemon}.png").resize((150, 150))
            self.p1_photo = ImageTk.PhotoImage(p1_image)
            self.p2_photo = ImageTk.PhotoImage(p2_image)
            self.battle_canvas.create_image(100, 50, image=self.p1_photo, anchor=tk.NW)
            self.battle_canvas.create_image(500, 50, image=self.p2_photo, anchor=tk.NW)
        except Exception as e:
            self.log_message(f"❌ Image Load Error: {e}")

    def update_hp_bars(self):
        p1_hp = max(0, self.player1.active_pokemon.hp)
        p2_hp = max(0, self.player2.active_pokemon.hp)
        p1_width = int((p1_hp / 200) * 200)
        p2_width = int((p2_hp / 200) * 200)
        self.battle_canvas.coords(self.hp_bar_p1, 100, 250, 100 + p1_width, 270)
        self.battle_canvas.coords(self.hp_bar_p2, 500, 250, 500 + p2_width, 270)

    def log_message(self, message):
        self.battle_log.insert(tk.END, message + "\n")
        self.battle_log.yview(tk.END)

    def log_error(self, message):
        self.error_log.insert(tk.END, "❌ " + message + "\n")
        self.error_log.yview(tk.END)

    class ErrorLogger:
        def __init__(self, gui):
            self.gui = gui
        def write(self, message):
            if message.strip():
                self.gui.log_error(message)
        def flush(self):
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = BattleGUI(root)
    root.mainloop()

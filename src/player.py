import logging
import random
from src.card import standard_pokemon_cards, standard_trainer_cards

class Player:
    def __init__(self, name, deck):
        self.name = name
        self.deck = deck
        self.hand = []
        self.active_pokemon = None
        self.bench = []
        self.discard_pile = []
        self.prize_cards = 6  # Each player starts with 6 prize cards
        self.special_conditions = {}  # Tracks status conditions like Burned or Paralyzed
        self.attack_log = []  # Logs damage dealt per turn
        self.energy_attached = 0  # Tracks energy attachments
        self.trainers_used = 0  # Tracks Trainer card usage

        self.shuffle_deck()
        self.draw_initial_hand()

    def shuffle_deck(self):
        """ Shuffles the player's deck. """
        random.shuffle(self.deck)
        logging.info(f"🔀 {self.name} shuffled their deck.")

    def draw_initial_hand(self):
        """ Draws 7 cards at the start of the game. """
        for _ in range(7):
            self.draw_card()

    def draw_card(self):
        """ Draws a card from the deck to the hand. """
        if self.deck:
            card = self.deck.pop(0)
            self.hand.append(card)
            logging.info(f"📝 {self.name} drew {card['name']}.")
        else:
            logging.info(f"🚨 {self.name} has no cards left to draw! This may result in a Deck Out loss.")

    def play_pokemon(self, pokemon):
        """ Plays a Pokémon from hand to active spot or bench. """
        if pokemon in self.hand:
            if self.active_pokemon is None:
                self.active_pokemon = pokemon
                logging.info(f"🃏 {self.name} played {pokemon['name']} as Active Pokémon.")
            else:
                if len(self.bench) < 5:
                    self.bench.append(pokemon)
                    logging.info(f"🃏 {self.name} placed {pokemon['name']} on the Bench.")
                else:
                    logging.warning(f"⚠️ {self.name}'s Bench is full. Cannot place {pokemon['name']}.")
            self.hand.remove(pokemon)
        else:
            logging.warning(f"⚠️ {self.name} tried to play {pokemon['name']}, but it’s not in hand!")

    def attach_energy(self, energy_card):
        """ Attaches an energy card to the active Pokémon. """
        if self.active_pokemon:
            self.energy_attached += 1
            self.active_pokemon["energy_attached"] = self.active_pokemon.get("energy_attached", 0) + 1
            self.hand.remove(energy_card)
            logging.info(f"⚡ {self.name} attached {energy_card['name']} to {self.active_pokemon['name']}.")
        else:
            logging.warning(f"⚠️ {self.name} has no active Pokémon to attach Energy!")

    def attack(self, opponent):
        """ AI chooses the best attack option. """
        if self.active_pokemon and "attacks" in self.active_pokemon:
            attack = random.choice(self.active_pokemon["attacks"])
            damage = int(attack.get("damage", 0))
            opponent.active_pokemon["hp"] -= damage
            self.record_attack(damage)
            logging.info(f"💥 {self.name}'s {self.active_pokemon['name']} used {attack['name']}! {damage} damage!")

    def take_prize_card(self):
        """ Player takes a Prize Card when they knock out an opponent's Pokémon. """
        if self.prize_cards > 0:
            self.prize_cards -= 1
            logging.info(f"🏆 {self.name} took a Prize Card! Remaining: {self.prize_cards}")

    def record_attack(self, damage):
        """ Records damage dealt to analyze playstyle. """
        self.attack_log.append(damage)

    def play_trainer_card(self, trainer_card):
        """ Logs Trainer card usage. """
        self.trainers_used += 1
        logging.info(f"🎴 {self.name} played Trainer: {trainer_card['name']}")

    def classify_playstyle(self):
        """ Determines AI or Player's playstyle based on attack & trainer usage. """
        avg_attack = sum(self.attack_log) / max(1, len(self.attack_log))  # Prevent division by zero

        if avg_attack >= 60 and self.trainers_used > 3:
            return "Aggressive"
        elif avg_attack < 40 and self.trainers_used <= 2:
            return "Defensive"
        else:
            return "Balanced"

    def apply_special_condition(self, condition):
        """ Applies special conditions (Burned, Paralyzed, etc.). """
        self.special_conditions[condition] = True
        logging.info(f"🔥 {self.name}'s Pokémon is now {condition}.")

    def clear_special_condition(self, condition):
        """ Removes a special condition. """
        if condition in self.special_conditions:
            del self.special_conditions[condition]
            logging.info(f"✅ {self.name}'s Pokémon is no longer {condition}.")

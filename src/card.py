import requests
import json
import os
import logging
import time

API_URL = "https://api.pokemontcg.io/v2/cards"
API_KEY = "6e055483-f06a-42d0-82fd-1d45692cd42e"
CACHE_FILE = "card_data.json"
MAX_RETRIES = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class Card:
    def __init__(self, id, name, supertype, subtypes, attacks, hp, types, weaknesses, effects):
        self.id = id
        self.name = name
        self.supertype = supertype
        self.subtypes = subtypes
        self.attacks = attacks
        self.hp = hp
        self.types = types
        self.weaknesses = weaknesses
        self.effects = effects

    def __repr__(self):
        return f"{self.name} ({self.supertype})"


def load_cached_data():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as file:
                logging.info("✅ Loading Pokémon data from cache...")
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logging.warning(f"⚠️ Cache file corrupted or missing. Fetching new data... ({e})")
    return None


def fetch_cards(supertype):
    cached_data = load_cached_data()
    if cached_data:
        return cached_data

    headers = {"X-Api-Key": API_KEY}
    all_cards = []
    page = 1

    while True:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                logging.info(f"🔄 Fetching {supertype} cards, Page {page} (Attempt {attempt}/{MAX_RETRIES})...")
                response = requests.get(
                    f"{API_URL}?q=supertype:{supertype} legalities.standard:Legal&page={page}&pageSize=250",
                    headers=headers,
                    timeout=10
                )
                response.raise_for_status()
                data = response.json()

                if "data" not in data or not data["data"]:
                    logging.info(f"✅ No more {supertype} cards to fetch.")
                    break

                for card in data["data"]:
                    all_cards.append(Card(
                        id=card["id"],
                        name=card["name"],
                        supertype=card["supertype"],
                        subtypes=card.get("subtypes", []),
                        attacks=card.get("attacks", []),
                        hp=int(card.get("hp", "0")) if card.get("hp", "0").isdigit() else 0,
                        types=card.get("types", []),
                        weaknesses=card.get("weaknesses", []),
                        effects=card.get("text", [])
                    ))
                page += 1
                break

            except requests.exceptions.RequestException as e:
                logging.error(f"❌ API Request Failed (Attempt {attempt}/{MAX_RETRIES}): {e}")
                if attempt == MAX_RETRIES:
                    logging.error("❌ Maximum retries reached. Some cards may be missing.")
                else:
                    time.sleep(2)

    with open(CACHE_FILE, "w") as file:
        json.dump([card.__dict__ for card in all_cards], file, indent=4)
        logging.info(f"✅ Saved {len(all_cards)} Pokémon to cache.")

    return all_cards

standard_pokemon_cards = fetch_cards("Pokémon")
standard_trainer_cards = fetch_cards("Trainer")

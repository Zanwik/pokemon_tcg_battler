import requests
import json
import time

# Define API URL
API_URL = "https://api.pokemontcg.io/v2/cards"
HEADERS = {
    "X-Api-Key": "6e055483-f06a-42d0-82fd-1d45692cd42e"  # If you have an API key, replace here; otherwise, remove this line.
}

def fetch_all_cards(max_retries=3, delay=5):
    """ Fetch all Pokémon TCG cards with pagination, retries, and error handling """
    all_cards = []
    page = 1
    page_size = 250  # Max allowed per request

    while True:
        for attempt in range(max_retries):
            try:
                print(f"🔄 Fetching page {page} (Attempt {attempt + 1}/{max_retries})...")
                response = requests.get(f"{API_URL}?page={page}&pageSize={page_size}", headers=HEADERS, timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    if not data["data"]:  # If no more cards, break the loop
                        print("✅ All cards have been fetched.")
                        break

                    all_cards.extend(data["data"])
                    page += 1
                    break  # Exit retry loop if successful
                else:
                    print(f"⚠️ Error {response.status_code}: {response.text}")
                    time.sleep(delay)  # Wait before retrying
            except requests.exceptions.RequestException as e:
                print(f"🚨 API request failed: {e}")
                time.sleep(delay)  # Wait before retrying

        else:
            print("❌ Max retries reached. Exiting.")
            break

    # Save all cards to JSON
    with open("pokemon_cards.json", "w") as file:
        json.dump({"data": all_cards}, file, indent=4)

    print(f"🎉 Successfully saved {len(all_cards)} cards to 'pokemon_cards.json'")

if __name__ == "__main__":
    fetch_all_cards()

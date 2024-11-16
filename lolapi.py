import requests

# Replace with your actual API key
API_KEY = 'RGAPI-aeeb6455-e91b-49f7-9530-6c0524fd63e6'
BASE_URL = 'https://sea.api.riotgames.com'

# Function to get summoner information by name
def get_summoner_info(summoner_name):
    url = f"{BASE_URL}/lol/summoner/v4/summoners/by-name/{summoner_name}"
    headers = {
        "X-Riot-Token": API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching summoner info: {response.status_code}")
        return None

# Function to get live game data for a summoner by summoner ID
def get_live_game_data(summoner_id):
    url = f"{BASE_URL}/lol/spectator/v4/active-games/by-summoner/{summoner_id}"
    headers = {
        "X-Riot-Token": API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        print("Summoner is not currently in a game.")
        return None
    else:
        print(f"Error fetching live game data: {response.status_code}")
        return None

# Main script
if __name__ == "__main__":
    summoner_name = "IIIga"  # Replace with the actual summoner name
    region = "th2"  # Replace with the desired region (e.g., na1, euw1, etc.)
    
    # Step 1: Get summoner info
    summoner_info = get_summoner_info(summoner_name)
    if summoner_info:
        summoner_id = summoner_info["id"]
        print(f"Summoner ID: {summoner_id}")

        # Step 2: Get live game data
        live_game_data = get_live_game_data(summoner_id)
        if live_game_data:
            print("Live Game Data:")
            print(live_game_data)

import requests
import csv
from bs4 import BeautifulSoup

# url = 'https://www.betika.com/en-ke/'
# response = requests.get(url)
# html_content = response.text
# # print(html_content)

# soup = BeautifulSoup(html_content, 'html.parser')

# define sports data api
sports_apis = [
    {
        "sport": "Football",
        "url": "https://api.betika.com/v1/uo/matches",
        "params": {
            "page": 1,
            "limit": None,
            "tab": "",
            "sub_type_id": "1,186,340",
            "sport_id": "14",
            "sort_id": "1",
            "period_id": "-2",
            "esports": "false",
        },
    },
    {
        "sport": "Basketball",
        "url": "https://api.betika.com/v1/uo/matches",
        "params": {
            "page": 1,
            "limit": None,
            "tab": "",
            "sub_type_id": "1,186,340",
            "sport_id": "30",
            "sort_id": "1",
            "period_id": "-2",
            "esports": "false",
        },
    },
    {
        "sport": "Tennis",
        "url": "https://api.betika.com/v1/uo/matches",
        "params": {
            "page": 1,
            "limit": None,
            "tab": "",
            "sub_type_id": "1,186,340",
            "sport_id": "28",
            "sort_id": "1",
            "period_id": "-2",
            "esports": "false",
        },
    },
]

#retrieve game data
def fetch_games(api_url, params, sport_name):
    games = []
    while True: # run it continously stop when there is an error
        response = requests.get(api_url, params=params)
        if response.status_code != 200:
            print(f"Failed to fetch data for {sport_name}: {response.status_code}")
            break

        data = response.json()
        matches = data.get("data", [])

        if not matches: #stop if no matches are available
            break

        for match in matches:
            games.append(
                [
                    sport_name,
                    match.get("home_team", "Unknown"),
                    match.get("away_team", "Unknown"),
                    match.get("start_time", "Unknown"),
                    match.get("competition_name", "Unknown"),
                    match.get("category", "Unknown"),
                ]
            )
        #check if there is another page to fetch
        if not data.get("pagination", {}).get("has_next_page", False):
            break
        params["page"] += 1

    return games

#store all sports data
all_games = []

#loop throush sports data and store them
for sport in sports_apis:
    print(f"Fetching data for {sport['sport']}...")
    sport_games = fetch_games(sport["url"], sport["params"], sport["sport"])
    all_games.extend(sport_games)

#store the data in csv
with open("betika_all_games.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    #add columns
    writer.writerow(
        ["Sport", "Home Team", "Away Team", "Start Time", "Competition", "Category"]
    )
    #add rows
    writer.writerows(all_games)



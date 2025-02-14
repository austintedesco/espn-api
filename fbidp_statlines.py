# Import necessary libraries
from dotenv import load_dotenv
import os
from espn_api.basketball import League
import pandas as pd
from datetime import datetime

# Load environment variables
load_dotenv()

# ESPN Fantasy League Credentials
league_id = os.getenv("LEAGUE_ID")
espn_s2 = os.getenv("ESPN_S2")
swid = os.getenv("SWID")

# Define range of seasons (update this based on your league's history)
start_year = 2020  # league's first season
end_year = datetime.now().year + 1

# Store extracted data
nba_game_data = []

# Loop through each season
for year in range(start_year, end_year + 1):
    try:
        print(f"Fetching data for season {year}...")

        # Initialize league for the specific season
        league = League(league_id=league_id, year=year, espn_s2=espn_s2, swid=swid)

        # List of all player IDs
        player_ids = list(league.player_map.keys())

        # Loop through every player to retrieve stats
        for player_id in player_ids:
            player = league.player_info(playerId=player_id)

            # Skip if player data is missing
            if not player:
                # print(f"Skipping playerId {player_id} (No data found)")
                continue

            player_name = player.name

            for game_id, game_stats in player.stats.items():
                if "total" in game_stats and game_id in player.schedule:
                    nba_game_data.append({
                        "season": year,
                        "playerId": player_id,
                        "player_name": player_name,
                        "game_id": game_id,
                        "date": player.schedule[game_id]["date"].strftime("%Y-%m-%d"),  # Format date
                        "opponent_team": player.schedule[game_id]["team"],  # Opponent team
                        "fantasy_points": game_stats.get("applied_total", 0),  # Fantasy points
                        **game_stats["total"]  # Include all raw stats
                    })

    except Exception as e:
        print(f"Error fetching data for season {year}: {e}")
        continue  # Skip to next season if an error occurs

# Convert to DataFrame
df = pd.DataFrame(nba_game_data)

# Save to Excel
df.to_excel("fbidp_statlines.xlsx", index=False)

print("Excel file created: fbidp_statlines.xlsx")
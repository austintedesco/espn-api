# Get data from all years in the league's history

# NBA Import
from espn_api.basketball import League
import pandas as pd
import sqlite3
from dotenv import load_dotenv
import os

# ESPN Fantasy League Credentials
year = 2025
load_dotenv()  # Load variables from .env

league_id = os.getenv("LEAGUE_ID")
espn_s2 = os.getenv("ESPN_S2")
swid = os.getenv("SWID")

league = League(league_id=league_id, year=year, espn_s2=espn_s2, swid=swid)

for matchup_period in range(1, league.currentMatchupPeriod + 1):  # Adjust range as needed
    box_scores = league.box_scores(matchup_period=matchup_period)

    for box_score in box_scores:
        for box_player in box_score.home_lineup + box_score.away_lineup:  # Ensures BoxPlayer objects
            if box_player in box_score.home_lineup:
                owner = box_score.home_team.owners
            if box_player in box_score.away_lineup:
                owner = box_score.away_team.owners
            else:
                owner = "Elegant Fail"
            print(f"Week: {matchup_period}")
            print(f"Fantasy Owner: {owner}")  # Owner of the player that week
            print(f"Player: {box_player.name}")
            print(f"Position: {box_player.slot_position}")
            print(f"Opponent: {box_player.pro_opponent}")
            print(f"Fantasy Points: {box_player.points}")
            print("Stat Breakdown:")
            for stat, value in box_player.points_breakdown.items():
                print(f"  {stat}: {value}")
            print("-" * 30)


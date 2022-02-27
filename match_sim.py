from unittest import result
from matplotlib.pyplot import draw
from understat_scrapper import UnderstatScrapper
import pandas as pd
from random import randint

class MatchSim:

    def __init__(self, home_frame, away_frame):
        self.home_goals = home_frame["xG"].astype(float).tolist()
        self.away_goals = away_frame["xG"].astype(float).tolist()
        cols =["Home Goals", "Away Goals", "Goal Difference", "Home Points", "Away Points"]
        self.results_df = pd.DataFrame(columns = cols)

    def evaluate_shots(self, shots):
        goals = 0
        for shot in shots:
            num = randint(0, 10000) / 10000
            if shot > num:
                goals += 1
        return goals 

    def play_match(self, index):
        home_goals = self.evaluate_shots(self.home_goals)
        away_goals = self.evaluate_shots(self.away_goals)
        dif = home_goals - away_goals
        if home_goals > away_goals:
            home_points = 3
            away_points = 0
        elif home_goals < away_goals:
            home_points = 0
            away_points = 3
        elif home_goals == away_goals:
            home_points = 1
            away_points = 1
        self.results_df.loc[index] = [home_goals, 
                                      away_goals, 
                                      dif, 
                                      home_points,
                                      away_points]

    def get_average(self, n):
        for match in range(1, n):
            self.play_match(match)
        results = self.results_df["Result"].tolist()
        print(f"Across {n} matches")
        print("Home wins:", results.count("Home win"))
        print("Away wins:", results.count("Away win"))
        print("Draws:", results.count("Draw"))
        print("Average home GD:", self.results_df["Goal Difference"].mean())

if __name__ == "__main__":
    scrapper = UnderstatScrapper()
    sim = MatchSim(scrapper.home_shot_table, scrapper.away_shot_table)
    sim.get_average(10000)

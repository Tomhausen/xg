from understat_scrapper import UnderstatScrapper
import pandas as pd
from random import randint
from numpy import mean
import matplotlib.pyplot as plt


class MatchSim:

    def __init__(self, match):
        self.match = match
        home_frame = match.home_shot_table
        away_frame = match.away_shot_table
        self.home_goals = home_frame["xG"].astype(float).tolist()
        self.away_goals = away_frame["xG"].astype(float).tolist()
        self.mean_home_points = 0
        self.mean_away_points = 0
        self.home_wins = 0
        self.away_wins = 0
        self.draws = 0
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

    def get_results(self, n):
        for match in range(1, n):
            self.play_match(match)
        home_points_list = self.results_df["Home Points"].tolist()
        away_points_list = self.results_df["Away Points"].tolist()
        self.mean_home_points = mean(home_points_list)
        self.mean_away_points = mean(away_points_list)

    def count_results(self):
        home_points_list = self.results_df["Home Points"].tolist()
        for result in home_points_list:
            if result == 3:
                self.home_wins += 1
            elif result == 1:
                self.draws += 1
            elif result == 0:
                self.away_wins += 1

    def pie_chart(self):
        counts = [self.home_wins, self.away_wins, self.draws]
        labels = [f"{self.match.home_team} win", f"{self.match.away_team} win", "Draw"]
        plt.pie(counts, labels = labels)
        plt.show()       

    def histogram(self):
        gd = self.results_df["Goal Difference"].tolist()
        plt.hist(gd)
        plt.show()

    def output_results(self):
        self.get_results(10000)
        self.count_results()
        print(f"{self.match.home_team}'s average points:", self.mean_home_points)
        print(f"{self.match.away_team}'s average points:", self.mean_away_points)
        self.pie_chart()
        self.histogram()


if __name__ == "__main__":
    scrapper = UnderstatScrapper()
    sim = MatchSim(scrapper)
    sim.output_results()

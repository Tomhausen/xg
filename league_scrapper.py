from scrapper import Scrapper
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

class LeagueScrapper(Scrapper):

    season = 2021

    def __init__(self):
        Scrapper.__init__(self)
        self.df = None
        self.home_teams = []
        self.home_xg = []
        self.home_goals = []
        self.away_goals = []
        self.away_xg = []
        self.away_teams = []
        self.cols = [self.home_teams, self.home_xg, self.home_goals,
                     self.away_goals, self.away_xg, self.away_teams]
        
    def run(self):
        url = self.base_url + "league/EPL/" + str(self.season - 1)
        self.get_json(url)
        url = self.base_url + "league/EPL/" + str(self.season)
        self.get_json(url)
        self.extract_json_to_lists()
        self.build_frame()
        
    def extract_json_to_lists(self):
        for season in self.data:
            for game in season:
                if game["goals"]["h"] != None:
                    self.cols[0].append(game["h"]["title"])
                    self.cols[1].append(game["xG"]["h"])
                    self.cols[2].append(game["goals"]["h"])
                    self.cols[3].append(game["goals"]["a"])
                    self.cols[4].append(game["xG"]["a"])
                    self.cols[5].append(game["a"]["title"])

    def build_frame(self):
        col_names = ["Home Team", "Home xG", "Home Goals", 
                     "Away Goals", "Away xG", "Away Team"]
        self.df = pd.DataFrame(self.cols, index = col_names)
        self.df = self.df.T


if __name__ == "__main__":
    scrapper = LeagueScrapper()
    scrapper.run()
    print(scrapper.df)

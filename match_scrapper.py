from scrapper import Scrapper
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd


class UnderstatScrapper(Scrapper):

    def __init__(self):
        Scrapper.__init__(self)
        self.home_team = ""
        self.away_team = ""
        self.home_df = None
        self.away_df = None        
        
        self.minute = []
        self.x = []
        self.y = []
        self.xg = []
        self.result = []
        self.situation = []
        self.shot_type = []
        self.player = []
        self.assisted = []
        self.last_action = []
        self.team = []
        self.cols = [self.minute, self.x, self.y, self.xg, self.result,
                     self.situation, self.shot_type, self.player, self.assisted,    
                     self.last_action, self.team]
        self.json_keys = ["minute", "X", "Y", "xG", "result", "situation",
                          "shotType", "player", "player_assisted", "lastAction"]

    def run(self):
        url = self.base_url + "match/" + self.get_match_id()
        self.get_json(url)
        self.data = self.data[0]
        self.get_frames()
        self.get_teams()

    def get_match_id(self):
        match_id = input("Please enter match id: ")
        if len(match_id) == 0:
            match_id = "16658"
        try:
            match_id = int(match_id)
            match_id = str(match_id)
        except ValueError:
            print("Please enter a valid id")
            self.get_match_id()
        if len(match_id) != 5:
            print("Please enter a valid id")
            self.get_match_id()
        return match_id

    def get_frames(self):    
        self.extract_json_to_lists("h")
        self.home_df = self.build_data_frame()
        for list in self.cols:
            list.clear()
        self.extract_json_to_lists("a")
        self.away_df = self.build_data_frame()

    def extract_json_to_lists(self, side):
        for shot in self.data[side]:
            for column_index in range(len(self.cols)-1):
                self.cols[column_index].append(shot[self.json_keys[column_index]])
            if side == "h":
                self.team.append(shot["h_team"])
            else:
                self.team.append(shot["a_team"])

    def build_data_frame(self):
        col_names = ["Minute", "X", "Y", "xG", "Result", "Situation", 
                     "Shot Type", "Player", "Assisted By", "Last Action", "Team"]
        shot_map_df = pd.DataFrame(self.cols, index = col_names)
        shot_map_df = shot_map_df.T
        return shot_map_df

    def get_teams(self):
        self.home_team = self.home_df["Team"][0]
        self.away_team = self.away_df["Team"][0]


if __name__ == "__main__":
    scrapper = UnderstatScrapper()
    scrapper.run()
    print(scrapper.home_df)
    print(scrapper.away_df)
    print(scrapper.home_team)
    print(scrapper.away_team)

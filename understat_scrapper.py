import requests
from bs4 import BeautifulSoup
import json
import pandas as pd


class UnderstatScrapper:

    base_url = "https://understat.com/match/"

    def __init__(self):
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
        match_id = self.get_match_id()
        url = self.base_url + match_id
        self.data = self.get_json(url)
        self.extract_json_to_lists("h")
        self.home_shot_table = self.build_data_frame()
        for list in self.cols:
            list.clear()
        self.extract_json_to_lists("a")
        self.away_shot_table = self.build_data_frame()


    def get_match_id(self):
        match_id = input("Please enter match id: ")
        if len(match_id) == 0:
            match_id = "16641"
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

    def get_json(self, url):    
        # get json of data
        res = requests.get(url)
        soup = BeautifulSoup(res.content, "lxml")
        # find tag in html
        scripts = soup.find_all("script")
        strings = str(scripts[1])
        # trim
        index_start = strings.index("('") + 2
        index_end = strings.index("')")
        json_data = strings[index_start: index_end]
        # encode and transform
        json_data = json_data.encode('utf8').decode('unicode_escape')
        data = json.loads(json_data)
        return data

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


if __name__ == "__main__":
    scrapper = UnderstatScrapper()
    print(scrapper.home_shot_table)
    print(scrapper.away_shot_table)


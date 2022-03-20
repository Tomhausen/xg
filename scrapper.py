import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

class Scrapper:

    base_url = "https://understat.com/"

    def __init__(self):
        self.data = []
        self.url = ""

    def get_json(self, url):
        res = requests.get(url)
        soup = BeautifulSoup(res.content, "lxml")
        scripts = soup.find_all("script")
        try:
            strings = str(scripts[1])
        except IndexError:
            return
        index_start = strings.index("('") + 2
        index_end = strings.index("')")
        json_data = strings[index_start: index_end]
        json_data = json_data.encode('utf8').decode('unicode_escape')
        data = json.loads(json_data)
        self.data.append(data)


if __name__ == "__main__":
    scrapper = Scrapper()
    scrapper.get_json()
    print(scrapper.data)

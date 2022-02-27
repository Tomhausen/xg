import matplotlib.pyplot as plt
from understat_scrapper import UnderstatScrapper

class XgFlowChart:

    def __init__(self, home_frame, away_frame):
        self.home_frame = home_frame
        self.away_frame = away_frame

    def remove_spare_cols(self, frame):
        keep_cols = ["Minute", "xG"]
        for col in frame.columns:
            if col not in keep_cols:
                frame.pop(col)

    def add_cumulative_xg(self, frame):
        cumulative_xg = []
        cumulation = 0
        for shot in frame.get("xG"):
            cumulation += float(shot)
            cumulative_xg.append(cumulation)
        frame.insert(2, "Cumulative xG", cumulative_xg)
        frame.pop("xG")
        # add match start
        frame.loc[-1] = [0, 0]
        frame.index = frame.index + 1
        frame = frame.sort_index()
        # double info for horizontal and veritcal lines
        frame.index = frame.index * 2
        minute = frame["Minute"]
        cumulative = frame["Cumulative xG"]
        max = (frame.shape[0] * 2) - 2
        for i in range(1, max, 2):
            frame.loc[i] = [minute[i + 1], cumulative[i - 1]]
        frame = frame.sort_index()
        # add max
        final_i = frame.shape[0] - 1
        if int(minute[final_i]) < 90:
            final = [90, cumulative[final_i]]
            frame.loc[frame.shape[0]] = final
        frame["Minute"] = frame["Minute"].astype(int)
        print(frame)
        return frame

    def make_chart(self, frame):
        minutes = frame["Minute"].values.tolist()
        xg = frame["Cumulative xG"].values.tolist()
        plt.plot(minutes, xg)

    def build(self):
        self.remove_spare_cols(self.home_frame)
        self.remove_spare_cols(self.away_frame)
        self.home_frame = self.add_cumulative_xg(self.home_frame)
        self.away_frame = self.add_cumulative_xg(self.away_frame)
        self.make_chart(self.home_frame)
        self.make_chart(self.away_frame)
        plt.show()


if __name__ == "__main__":
    scrapper = UnderstatScrapper()
    chart = XgFlowChart(scrapper.home_shot_table, scrapper.away_shot_table)
    chart.build()
import pandas as pd

class MovingAverageCrossover:
    def __init__(self, short_window=20, long_window=50):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data):
        data["Short_MA"] = data["Close"].rolling(self.short_window).mean()
        data["Long_MA"] = data["Close"].rolling(self.long_window).mean()
        data["Signal"] = 0
        data.loc[data["Short_MA"] > data["Long_MA"], "Signal"] = 1
        data.loc[data["Short_MA"] <= data["Long_MA"], "Signal"] = -1
        return data

class VolumeFilter:
    def __init__(self, window=50):
        self.window = window

    def apply(self, data):
        data["Avg_Volume"] = data["Volume"].rolling(self.window).mean()
        data.loc[data["Volume"] < data["Avg_Volume"], "Signal"] = 0
        return data

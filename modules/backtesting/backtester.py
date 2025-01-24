class Backtester:
    def __init__(self, data, strategy, filters=[]):
        self.data = data
        self.strategy = strategy
        self.filters = filters

    def run(self):
        # Generate signals using the strategy
        data_with_signals = self.strategy.generate_signals(self.data)

        # Apply each filter
        for filter_obj in self.filters:
            data_with_signals = filter_obj.apply(data_with_signals)

        # Placeholder for performance calculation
        return data_with_signals[["Close", "Signal"]]

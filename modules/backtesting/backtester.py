class Backtester:
    def __init__(self, data, strategy, filters=[]):
        self.data = data
        self.strategy = strategy
        self.filters = filters

    def run(self):
        # Generate signals using the strategy
        print("Running strategy...")
        data_with_signals = self.strategy.generate_signals(self.data)

        # Debugging: Check if signals are added
        print("Data after signal generation:")
        print(data_with_signals.head())

        # Apply filters if any
        for filter_obj in self.filters:
            data_with_signals = filter_obj.apply(data_with_signals)

        # Return the full DataFrame with all columns preserved
        return data_with_signals

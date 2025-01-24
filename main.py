import json
from modules.utils.data_loader import download_data, load_data
from modules.strategies.ma_crossover import MovingAverageCrossover
from modules.filters.volume_filter import VolumeFilter
from modules.backtesting.backtester import Backtester
from modules.utils.plotting import plot_signals

# Step 1: Load configuration
with open("config/strategies.json") as config_file:
    config = json.load(config_file)

# Step 2: Iterate over assets in the configuration
for ticker, settings in config.items():
    print(f"\n=== Backtesting {ticker} ===")

    # Step 3: Download and load data
    file_path = f"data/{ticker}.csv"
    download_data(ticker, "1900-01-01", "2026-12-31", file_path)
    data = load_data(file_path)

    # Step 4: Initialize strategy
    strategy = None
    if "ma_crossover" in settings["strategies"]:
        strategy = MovingAverageCrossover(short_window=20, long_window=50)

    # Step 5: Initialize filters
    filters = []
    if "volume_filter" in settings["filters"]:
        filters.append(VolumeFilter(window=50))

    # Step 6: Run backtesting
    backtester = Backtester(data, strategy, filters)
    results = backtester.run()

    # Step 7: Display results
    print(f"Results for {ticker}:\n", results.tail())

    # Step 8: Plot the signals
    plot_signals(results)

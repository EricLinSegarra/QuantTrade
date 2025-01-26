import json
from modules.utils.data_loader import download_data, load_data
from modules.strategies.ma_crossover import MovingAverageCrossover
from modules.strategies.weinstein_breakout import WeinsteinBreakoutEMA
from modules.filters.volume_filter import VolumeFilter
from modules.backtesting.backtester import Backtester
from modules.utils.plotting import plot_signals, plot_weinstein_signals_ema

# Step 1: Load configuration
with open("config/strategies.json") as config_file:
    config = json.load(config_file)

# Step 2: Iterate over assets in the configuration
for ticker, settings in config.items():
    print(f"\n=== Backtesting {ticker} ===")

    # Step 3: Download and load data
    file_path = f"data/{ticker}.csv"
    download_data(ticker, "2020-01-01", "2023-12-31", file_path)
    data = load_data(file_path)

    # Debugging: Verify data structure
    print(f"Data columns: {data.columns}")
    print(f"Data index type: {data.index.dtype}")
    print(data.head())

    # Step 4: Initialize strategy
    strategy_name = settings["strategy"]
    strategy = None
    if strategy_name == "ma_crossover":
        print("Running Moving Average Crossover strategy...")
        strategy = MovingAverageCrossover(short_window=20, long_window=50)
    elif strategy_name == "weinstein_breakout_ema":
        print("Running Weinstein Breakout EMA strategy...")
        strategy = WeinsteinBreakoutEMA(volume_window=50)
    else:
        print(f"Error: Unknown strategy '{strategy_name}' for {ticker}. Skipping...")
        continue

    # Step 5: Initialize filters
    filters = []
    if "filters" in settings:
        for filter_name in settings["filters"]:
            if filter_name == "volume_filter":
                filters.append(VolumeFilter(window=50))
            else:
                print(f"Error: Unknown filter '{filter_name}' for {ticker}. Skipping...")

    # Step 6: Run backtesting
    backtester = Backtester(data, strategy, filters)
    results = backtester.run()

    # Step 7: Display results
    print(f"Results for {ticker}:\n", results.tail())

    # Step 8: Plot the signals
    if strategy_name == "weinstein_breakout_ema":
        plot_weinstein_signals_ema(results)
    elif strategy_name == "ma_crossover":
        plot_signals(results)

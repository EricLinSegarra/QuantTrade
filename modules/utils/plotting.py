import mplfinance as mpf
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt


def plot_signals_ohlc(data, file_path, max_points=500):
    """
    Plots OHLC chart with Moving Average Crossover signals and volume using mplfinance.
    Skips plotting if there are no buy signals.

    Args:
        data (pd.DataFrame): Market data with 'Open', 'High', 'Low', 'Close', 'Volume', and 'Signal'.
        file_path (str): Path to the CSV file, used to extract the ticker name.
        max_points (int): Maximum number of data points to display (default: 500).
    """
    ticker = file_path.split("/")[-1].replace(".csv", "")
    data = data.iloc[:max_points].copy()

    # Ensure the index is DatetimeIndex and correctly formatted
    if not isinstance(data.index, pd.DatetimeIndex):
        data.index = pd.to_datetime(data.index)

    # 🚨 Force the index to be unique and sorted
    data = data[~data.index.duplicated(keep="first")]
    data = data.sort_index()

    # Debug: Print first dates
    print(f"📅 {ticker} - First date in dataset: {data.index.min().strftime('%b %Y')}")

    if data.empty or (data["Signal"] == 1).sum() == 0:
        print(f"⚠️ No buy signals for {ticker}, skipping plot.")
        return

    # Calculate moving averages
    data["Short_MA"] = data["Close"].rolling(window=20).mean()
    data["Long_MA"] = data["Close"].rolling(window=50).mean()
    data.dropna(inplace=True)

    # Buy signals
    buy_signal_series = data["Close"].copy()
    buy_signal_series[data["Signal"] != 1] = None

    add_plots = [
        mpf.make_addplot(data["Short_MA"], color="blue", linestyle="dashed", width=1),
        mpf.make_addplot(data["Long_MA"], color="red", linestyle="dashed", width=1),
        mpf.make_addplot(buy_signal_series, type="scatter", marker="^", color="g", markersize=100),
    ]

    # Create figure and axes
    fig, ax = mpf.plot(
        data,
        type="ohlc",
        volume=True,
        style="charles",
        show_nontrading=False,
        figsize=(12, 8),
        addplot=add_plots,
        panel_ratios=(3, 1),
        returnfig=True,
        title=f"MA Crossover Signals - {ticker}",
    )

    # 🔹 Fix date formatting issue
    ax[0].xaxis.set_major_locator(mdates.MonthLocator())
    ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))  # "Jan 20", "Feb 20"
    plt.setp(ax[0].xaxis.get_majorticklabels(), rotation=30)

    plt.show()


def plot_weinstein_signals_ohlc(data, file_path, max_points=500):
    ticker = file_path.split("/")[-1].replace(".csv", "")  # Extract ticker name
    data = data.iloc[:max_points].copy()  # Limit to first N data points

    # Ensure the index is DatetimeIndex
    if not isinstance(data.index, pd.DatetimeIndex):
        data.index = pd.to_datetime(data.index)

    # Ensure index is unique and sorted
    data = data[~data.index.duplicated(keep="first")]
    data = data.sort_index()

    # Debugging: Check first date
    print(f"📅 {ticker} - First date in dataset: {data.index.min().strftime('%b %Y')}")

    # Check for buy signals
    if data.empty or (data["Signal"] == 1).sum() == 0:
        print(f"⚠️ No buy signals for {ticker}, skipping plot.")
        return

    # Buy signals
    buy_signal_series = data["Close"].copy()
    buy_signal_series[data["Signal"] != 1] = None  # Keep same length, only show buy signals

    # Create addplots
    add_plots = [
        mpf.make_addplot(data["EMA_30_Week"], color="orange", width=1.5),
        mpf.make_addplot(buy_signal_series, type="scatter", marker="^", color="g", markersize=100),
    ]

    fig, ax = mpf.plot(
        data,
        type="ohlc",
        volume=True,
        style="charles",
        figsize=(12, 8),
        addplot=add_plots,
        panel_ratios=(3, 1),
        returnfig=True,
        title=f"Weinstein Breakout with 30-Week EMA - {ticker}",
    )

    mpf.show()


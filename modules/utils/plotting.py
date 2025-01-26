import matplotlib.pyplot as plt


def plot_signals(data):
    """
    Plot the close price along with buy/sell signals.

    Args:
        data (pd.DataFrame): Data with 'Close' and 'Signal' columns.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data["Close"], label="Close Price", alpha=0.6)

    # Buy signals (Signal = 1)
    buy_signals = data[data["Signal"] == 1]
    plt.scatter(buy_signals.index, buy_signals["Close"], label="Buy Signal", marker="^", color="green")

    # Sell signals (Signal = -1)
    sell_signals = data[data["Signal"] == -1]
    plt.scatter(sell_signals.index, sell_signals["Close"], label="Sell Signal", marker="v", color="red")

    plt.legend()
    plt.title("Trading Signals")
    plt.show()


def plot_weinstein_signals_ema(data):
    """
    Plot price data with Weinstein breakout signals using a 30-week EMA.

    Args:
        data (pd.DataFrame): Historical data with 'Close', 'EMA_30_Week', and 'Signal' columns.
    """
    # Check if EMA_30_Week exists
    if 'EMA_30_Week' not in data.columns:
        raise ValueError("Column 'EMA_30_Week' is missing. Ensure the strategy was run correctly.")

    import matplotlib.pyplot as plt

    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data["Close"], label="Close Price", color="blue", alpha=0.6)
    plt.plot(data.index, data["EMA_30_Week"], label="30-Week EMA", color="orange", alpha=0.8)

    # Breakout signals (Signal = 1)
    breakout_signals = data[data["Signal"] == 1]
    plt.scatter(breakout_signals.index, breakout_signals["Close"], label="Breakout Signal", marker="^", color="green")

    plt.legend()
    plt.title("Weinstein Breakout Signals with 30-Week EMA")
    plt.show()

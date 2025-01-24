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

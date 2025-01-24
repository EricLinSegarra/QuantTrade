import pandas as pd


class EMAFilter:
    """
    A flexible EMA filter that allows trading based on the relationship between
    short-term and long-term EMAs with customizable parameters.
    """


    def __init__(self, short_window=10, long_window=20):
        """
        Initializes the EMAFilter with specified short-term and long-term windows.

        Args:
            short_window (int): Window size for the short-term EMA.
            long_window (int): Window size for the long-term EMA.
        """
        self.short_window = short_window
        self.long_window = long_window


    def apply(self, data, short_window=None, long_window=None):
        """
        Apply the EMA filter to the dataset with optional user-defined parameters.

        Args:
            data (pd.DataFrame): Data with a 'Close' column.
            short_window (int, optional): Overrides the default short-term EMA window.
            long_window (int, optional): Overrides the default long-term EMA window.

        Returns:
            pd.DataFrame: Data with added 'EMA_Short', 'EMA_Long', and 'EMA_Signal' columns.
        """
        # Use user-defined windows if provided, otherwise fall back to defaults
        short_window = short_window if short_window is not None else self.short_window
        long_window = long_window if long_window is not None else self.long_window

        # Calculate short-term EMA
        data['EMA_Short'] = data['Close'].ewm(span=short_window, adjust=False).mean()

        # Calculate long-term EMA
        data['EMA_Long'] = data['Close'].ewm(span=long_window, adjust=False).mean()

        # Generate EMA Signal: 1 for long, -1 for short
        data['EMA_Signal'] = 0
        data.loc[data['EMA_Short'] > data['EMA_Long'], 'EMA_Signal'] = 1  # Long allowed
        data.loc[data['EMA_Short'] <= data['EMA_Long'], 'EMA_Signal'] = -1  # Short allowed

        return data

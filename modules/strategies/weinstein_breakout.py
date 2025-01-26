import pandas as pd
import numpy as np


class WeinsteinBreakoutEMA:
    """
    Implements Stan Weinstein's breakout strategy using a 30-week EMA on daily data,
    dynamically adjusting for market frequency.
    """


    def __init__(self, volume_window=50):
        """
        Initialize the Weinstein breakout strategy with a dynamically adjusted EMA window.

        Args:
            volume_window (int): Window size for average volume (default: 50 days).
        """
        self.volume_window = volume_window

    def detect_market_frequency(self, data):
        """
        Detect market frequency (trading vs continuous) and calculate the appropriate EMA window.

        Args:
            data (pd.DataFrame): Historical price data with 'Date' as index.

        Returns:
            int: Adjusted EMA window based on market type.
        """
        # Ensure the index is DatetimeIndex
        if not isinstance(data.index, pd.DatetimeIndex):
            raise ValueError("Index must be a DatetimeIndex to detect market frequency.")

        # Use the index to group by weeks
        data['Week'] = data.index.isocalendar().week
        weekly_counts = data.groupby('Week').size()  # Count days per week
        avg_days_per_week = weekly_counts.mean()

        # Estimate EMA window: 30 weeks x avg days per week
        ema_window = int(30 * avg_days_per_week)
        return ema_window

    def generate_signals(self, data):
        """
        Generate buy signals based on the Weinstein breakout strategy using a dynamic 30-week EMA.

        Args:
            data (pd.DataFrame): Historical price data with columns ['Close', 'Volume'] and 'Date' as index.

        Returns:
            pd.DataFrame: Input data with added 'Signal' column (1 = Buy, 0 = No action).
        """
        # Ensure the index is datetime
        if not isinstance(data.index, pd.DatetimeIndex):
            data.index = pd.to_datetime(data.index)

        # Debugging: Check data before calculations
        print("Data before EMA calculation:")
        print(data.head())

        # Detect market frequency
        ema_window = self.detect_market_frequency(data)

        # Calculate 30-week EMA
        data['EMA_30_Week'] = data['Close'].ewm(span=ema_window, adjust=False).mean()

        # Debugging: Check if EMA_30_Week is created
        if 'EMA_30_Week' in data.columns:
            print("EMA_30_Week calculated successfully.")
        else:
            print("Error: EMA_30_Week not calculated.")

        # Calculate average volume
        data['Avg_Volume'] = data['Volume'].rolling(window=self.volume_window).mean()

        # Generate signals
        data['Signal'] = 0
        data.loc[
            (data['Close'] > data['EMA_30_Week']) &
            (data['Close'].shift(1) <= data['EMA_30_Week']) &
            (data['Volume'] > data['Avg_Volume']),
            'Signal'
        ] = 1

        return data



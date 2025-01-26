import os
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

def is_file_outdated(file_path, max_age_days=1):
    """
    Checks if a file is older than the specified maximum age.

    Args:
        file_path (str): Path to the file.
        max_age_days (int): Maximum age in days for the file to be considered up-to-date.

    Returns:
        bool: True if the file is outdated or doesn't exist, False otherwise.
    """
    if not os.path.exists(file_path):
        return True  # File doesn't exist, it's outdated by default

    # Check file modification time
    file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
    if datetime.now() - file_mod_time > timedelta(days=max_age_days):
        return True  # File is older than max_age_days

    return False  # File is up-to-date

def download_data(ticker, start_date, end_date, file_path):
    """
    Always downloads the full historical market data from Yahoo Finance,
    saves it as a clean CSV file, and removes any invalid rows (e.g., extra headers).

    Args:
        ticker (str): Ticker symbol (e.g., 'AAPL').
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        file_path (str): Path to save the CSV file.
    """
    print(f"Downloading full historical data for {ticker}...")

    # Remove old file if it exists
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Old data for {ticker} removed: {file_path}")

    # Attempt to download data from Yahoo Finance
    try:
        data = yf.download(ticker, start=start_date, end=end_date)

        # Ensure the data is not empty
        if not data.empty:
            # Reset index to make 'Date' a column
            data.reset_index(inplace=True)

            # Keep only relevant columns
            data = data[["Date", "Open", "High", "Low", "Close", "Volume"]]

            # Save to CSV
            data.to_csv(file_path, index=False)
            print(f"New data for {ticker} saved to {file_path}")

            # Check and clean the second row of the file
            clean_csv(file_path)

        else:
            print(f"Warning: No data downloaded for {ticker}. Skipping.")

    except Exception as e:
        print(f"Error downloading data for {ticker}: {e}")




def clean_csv(file_path):
    """
    Cleans the CSV file by ensuring the header and data rows are valid.

    Args:
        file_path (str): Path to the CSV file.
    """
    print(f"Validating and cleaning {file_path}...")

    # Read the file into a list of lines
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Ensure the header is valid
    expected_header = ["Date", "Open", "High", "Low", "Close", "Volume"]
    header = lines[0].strip().split(",")
    if header != expected_header:
        raise ValueError(f"Invalid header in {file_path}: {header}. Expected: {expected_header}")

    # Check if the second row is invalid (contains non-numeric data)
    if len(lines) > 1:  # Ensure there's at least one data row to check
        second_row = lines[1].strip().split(",")
        if all(not item.replace('.', '', 1).isdigit() for item in second_row[1:]):  # Exclude 'Date'
            print("Invalid second row detected. Removing it...")
            lines.pop(1)

    # Write the cleaned content back to the file
    with open(file_path, "w") as file:
        file.writelines(lines)

    print(f"{file_path} cleaned successfully.")



def load_data(file_path):
    """
    Loads historical market data from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Market data with 'Date' as index.
    """
    print(f"Loading data from {file_path}...")
    data = pd.read_csv(
        file_path,
        parse_dates=["Date"],  # Ensure 'Date' is parsed as datetime
        index_col="Date"       # Set 'Date' as the DataFrame index
    )

    if data.empty:
        raise ValueError(f"Data in {file_path} is empty.")

    return data


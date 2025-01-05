import os
import pandas as pd

# Path to raw and preprocessed data
raw_data_path = "/mnt/e/projects/BullBot/data/raw"
preprocessed_data_path = "/mnt/e/projects/BullBot/data/preprocessed"

# Ensure the preprocessed directory exists
os.makedirs(preprocessed_data_path, exist_ok=True)

def preprocess_data(file_name, start_date=None, end_date=None):
    """
    Clean and filter stock data by date range.
    Args:
        file_name (str): Name of the file to preprocess.
        start_date (str): Start date in 'YYYY-MM-DD' format (optional).
        end_date (str): End date in 'YYYY-MM-DD' format (optional).
    """
    file_path = os.path.join(raw_data_path, file_name)
    try:
        # Read the .csv file
        df = pd.read_csv(file_path, parse_dates=['Date'], dayfirst=False)
        print(f"Processing file: {file_name}")
    except Exception as e:
        print(f"Error reading {file_name}: {e}")
        return

    # Remove rows with NaN values
    original_rows = len(df)
    df.dropna(inplace=True)
    print(f"Dropped NaN rows: {original_rows - len(df)} rows removed")

    # Filter by date range
    if start_date:
        df = df[df['Date'] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df['Date'] <= pd.to_datetime(end_date)]

    if df.empty:
        print(f"Skipping {file_name}: No data after filtering")
        return

    # Save preprocessed data
    save_path = os.path.join(preprocessed_data_path, file_name)
    df.to_csv(save_path, index=False)
    print(f"Preprocessed data saved to {save_path}")

if __name__ == "__main__":
    # Specify your date range here
    START_DATE = "2000-01-01"
    END_DATE = "2024-12-31"

    # Process all .csv files in the raw directory
    for file_name in os.listdir(raw_data_path):
        if file_name.endswith('.csv'):
            preprocess_data(file_name, START_DATE, END_DATE)

    print("Data preprocessing complete.")

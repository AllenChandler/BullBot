import os
import pandas as pd

# Paths for raw and cleaned data
raw_data_path = "/mnt/e/projects/BullBot/data/polygon/raw"
cleaned_data_path = "/mnt/e/projects/BullBot/data/polygon/clean"
os.makedirs(cleaned_data_path, exist_ok=True)

def clean_data(file_path):
    try:
        # Load the CSV into a DataFrame
        df = pd.read_csv(file_path)

        # Remove rows with NaN values
        df.dropna(inplace=True)

        # Validate `window_start` column (ensure it exists but do not convert)
        if 'window_start' in df.columns:
            df = df[df['window_start'].notnull()]

        # Validate `close` column
        if 'close' in df.columns:
            df['close'] = pd.to_numeric(df['close'], errors='coerce')
            df.dropna(subset=['close'], inplace=True)

        # Save cleaned data
        save_path = os.path.join(cleaned_data_path, os.path.basename(file_path))
        df.to_csv(save_path, index=False)

    except Exception as e:
        pass  # Log or handle error if needed

# Process each raw data file
for file_name in os.listdir(raw_data_path):
    if file_name.endswith('.csv'):
        file_path = os.path.join(raw_data_path, file_name)
        clean_data(file_path)

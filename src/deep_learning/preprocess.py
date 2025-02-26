import os
import yaml
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load config file
CONFIG_PATH = "E:/projects/BullBot_backup/config.yaml"
with open(CONFIG_PATH, "r") as file:
    config = yaml.safe_load(file)

# Paths from config
input_dir = config["data_paths"]["continuous_data"]
output_dir = config["data_paths"]["processed_deep_learning"]

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Columns to use from the config
selected_columns = config["preprocessing"]["metrics_columns"]

# Spike detection settings
SPIKE_THRESHOLD = 1.7  # 70% increase (1.7x original price)
SPIKE_LOOKBACK_HOURS = 6  # Detect spikes based on price from 6 hours ago
PRE_SPIKE_LABEL_HOURS = 4  # Label `1` starting 4 hours before the spike
STOP_LABEL_MINUTES = 15  # Stop labeling 15 minutes before the spike

# Initialize scaler
scaler = MinMaxScaler()

# Process each CSV file in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".csv"):
        filepath = os.path.join(input_dir, filename)
        print(f"Processing {filename}...")

        # Load CSV file
        df = pd.read_csv(filepath)

        # Ensure all required columns exist
        if not all(col in df.columns for col in selected_columns):
            print(f"Skipping {filename}: missing required columns.")
            continue  # Skip if columns are missing

        # Convert timestamp column to datetime
        df["window_start"] = pd.to_datetime(df["window_start"])

        # Sort by time to ensure correct sequential order
        df = df.sort_values(by="window_start")

        # Add a column for spike labels (default `0`)
        df["spike_label"] = 0

        # Loop through the dataset to find spikes
        for i in range(len(df)):
            current_time = df.loc[i, "window_start"]
            lookback_time = current_time - pd.Timedelta(hours=SPIKE_LOOKBACK_HOURS)

            # Find price 6 hours ago
            past_prices = df[df["window_start"] <= lookback_time]["close"]
            if not past_prices.empty:
                past_price = past_prices.iloc[-1]

                # Check if current price is 70% higher than the past price
                if df.loc[i, "close"] >= past_price * SPIKE_THRESHOLD:
                    spike_time = df.loc[i, "window_start"]

                    # Label `1` for PRE_SPIKE_LABEL_HOURS leading up to the spike
                    pre_spike_start = spike_time - pd.Timedelta(hours=PRE_SPIKE_LABEL_HOURS)
                    pre_spike_end = spike_time - pd.Timedelta(minutes=STOP_LABEL_MINUTES)

                    df.loc[
                        (df["window_start"] >= pre_spike_start) & (df["window_start"] <= pre_spike_end),
                        "spike_label"
                    ] = 1

        # Normalize features (excluding label)
        df_selected = df[selected_columns]
        df_selected = scaler.fit_transform(df_selected)

        # Add spike label column back after scaling
        df_selected = np.hstack([df_selected, df["spike_label"].values.reshape(-1, 1)])

        # Convert to NumPy array and save as `.npy`
        npy_filename = filename.replace(".csv", ".npy")
        np.save(os.path.join(output_dir, npy_filename), df_selected)

print("✅ Deep learning preprocessing complete. All CSVs converted to .npy with spike labels.")

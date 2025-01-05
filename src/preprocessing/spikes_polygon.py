import os
import pandas as pd
from datetime import datetime

# Paths
input_data_path = "/mnt/e/projects/BullBot/data/polygon/metrics"
output_data_path = "/mnt/e/projects/BullBot/data/polygon/processed/spikes"
os.makedirs(output_data_path, exist_ok=True)

# Parameters
spike_threshold = 0.30  # 30% increase
spike_window_minutes = 120  # 120-minute window
lookback_minutes = 120  # Include 120 minutes from the previous day

# Function to load prior day's data
def load_prior_day_data(current_file_date, all_files):
    prior_file_date = current_file_date - pd.Timedelta(days=1)
    prior_file_name = f"{prior_file_date.strftime('%Y-%m-%d')}.csv"
    prior_file_path = os.path.join(input_data_path, prior_file_name)
    
    if os.path.exists(prior_file_path):
        prior_data = pd.read_csv(prior_file_path)
        prior_data = prior_data.sort_values("window_start").reset_index(drop=True)
        # Take the last `lookback_minutes` worth of rows
        return prior_data.tail(lookback_minutes)
    return pd.DataFrame()  # Return empty if no prior data

# Function to find spikes
def find_spikes_with_prior_data(file_path, all_files):
    try:
        # Load the current day's data
        df = pd.read_csv(file_path)
        if not {"close", "ticker", "window_start"}.issubset(df.columns):
            print(f"Skipping {file_path}: Missing required columns.")
            return

        df = df.sort_values("window_start").reset_index(drop=True)
        df["close"] = pd.to_numeric(df["close"], errors="coerce")
        df.dropna(subset=["close"], inplace=True)

        # Get the current file date
        current_file_date = datetime.strptime(os.path.basename(file_path).split(".")[0], "%Y-%m-%d")

        # Load the prior day's data
        prior_data = load_prior_day_data(current_file_date, all_files)

        # Combine prior day's data with current day
        if not prior_data.empty:
            df = pd.concat([prior_data, df], ignore_index=True)

        # Process by ticker
        for ticker in df["ticker"].unique():
            ticker_data = df[df["ticker"] == ticker].reset_index(drop=True)

            for i in range(len(ticker_data) - spike_window_minutes):
                price_start = ticker_data.iloc[i]["close"]

                # Search for spike
                spike_row = None
                for j in range(i + 1, i + spike_window_minutes):
                    price_max = ticker_data.iloc[j]["close"]
                    if (price_max - price_start) / price_start >= spike_threshold:
                        spike_row = j
                        break

                if spike_row:
                    # Define spike window
                    spike_window = ticker_data.iloc[max(0, spike_row - spike_window_minutes):spike_row]

                    # Save spike to file
                    spike_time = ticker_data.iloc[spike_row]["window_start"]
                    output_file = f"Spike_{ticker}_{spike_time}.csv"
                    spike_window.to_csv(os.path.join(output_data_path, output_file), index=False)
                    print(f"Saved spike: {output_file}")
                    break  # Stop after finding the first spike for this ticker

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Process all files
all_files = sorted([f for f in os.listdir(input_data_path) if f.endswith(".csv")])
for file_name in all_files:
    file_path = os.path.join(input_data_path, file_name)
    print(f"Processing file: {file_name}")
    find_spikes_with_prior_data(file_path, all_files)

print("Spike detection with prior-day data complete.")

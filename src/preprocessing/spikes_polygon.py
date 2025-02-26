import os
import pandas as pd

# Paths
input_data_path = "/mnt/e/projects/BullBot/data/polygon/continuous"
output_data_path = "/mnt/e/projects/BullBot/data/polygon/processed/spikes"
os.makedirs(output_data_path, exist_ok=True)

# Parameters
spike_threshold = 0.30  # 30% increase
spike_window_minutes = 120  # 120-minute window
lookback_minutes = 120  # Include 120 minutes before the spike

# Function to find spikes
def find_spikes(file_path):
    try:
        # Load the data
        df = pd.read_csv(file_path)
        df["window_start"] = pd.to_numeric(df["window_start"], errors="coerce")
        df["close"] = pd.to_numeric(df["close"], errors="coerce")
        df.dropna(subset=["window_start", "close"], inplace=True)

        # Sort by time to ensure chronological order
        df = df.sort_values("window_start").reset_index(drop=True)

        # Process for spikes
        for i in range(len(df) - spike_window_minutes):
            start_price = df.iloc[i]["close"]
            spike_found = False
            spike_rows = []  # Collect rows within the spike

            for j in range(i + 1, i + spike_window_minutes):
                if j >= len(df):  # Break if index exceeds data length
                    break
                max_price = df.iloc[j]["close"]
                spike_rows.append(j)
                if (max_price - start_price) / start_price >= spike_threshold:
                    spike_found = True
                    break

            if spike_found:
                # Restrict spike to `spike_window_minutes`
                spike_end = max(spike_rows[-1], i + spike_window_minutes - 1)
                spike_data = df.iloc[max(0, i - lookback_minutes):spike_end]  # Include lookback period

                # Save spike to file
                output_file = os.path.join(
                    output_data_path, f"Spike_{os.path.basename(file_path).split('.')[0]}_{i}.csv"
                )
                spike_data.to_csv(output_file, index=False)
                print(f"Saved spike: {output_file}")
                break  # Stop after finding the first spike for this ticker

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Process all files
all_files = sorted([f for f in os.listdir(input_data_path) if f.endswith(".csv")])
for file_name in all_files:
    file_path = os.path.join(input_data_path, file_name)
    print(f"Processing file: {file_name}")
    find_spikes(file_path)

print("Spike detection complete.")

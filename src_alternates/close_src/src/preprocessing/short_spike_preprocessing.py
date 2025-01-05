import os
import pandas as pd
import random

# Paths
preprocessed_data_path = "/mnt/e/projects/BullBot/data/preprocessed"
behavior_data_path = "/mnt/e/projects/BullBot/data/behaviors/Short_Spike"

# Ensure output directories exist
instances_path = os.path.join(behavior_data_path, "Instances")
non_instances_path = os.path.join(behavior_data_path, "Non_Instances")
os.makedirs(instances_path, exist_ok=True)
os.makedirs(non_instances_path, exist_ok=True)

# Parameters
short_spike_threshold = 0.70  # 70% increase over 7 days
pre_behavior_days = 30
post_behavior_days = 5
max_spikes_per_stock = 10  # Cap for spike instances per stock
max_non_spikes_per_stock = 10  # Cap for non-spike instances per stock
global_instance_cap = 10000  # Total cap for instances across all stocks
global_non_instance_cap = 100000  # Total cap for non-instances across all stocks

# Specify date range
START_DATE = "2000-01-01"
END_DATE = "2017-12-31"

# Initialize global counters
global_instance_count = 0
global_non_instance_count = 0

# Process each stock file
for file_name in os.listdir(preprocessed_data_path):
    if file_name.endswith(".csv"):
        file_path = os.path.join(preprocessed_data_path, file_name)
        df = pd.read_csv(file_path, parse_dates=["Date"], dayfirst=False, index_col="Date")

        print(f"Processing file: {file_name}")

        # Filter data by the specified date range
        df = df[(df.index >= START_DATE) & (df.index <= END_DATE)]

        # Skip files with insufficient data
        if len(df) < (pre_behavior_days + post_behavior_days):
            print(f"Skipping {file_name}: Not enough data for the required window.")
            continue

        # Ensure data is sorted by date
        df.sort_index(inplace=True)

        # Calculate percentage changes
        df["Pct_Change"] = df["Close"].pct_change(periods=7)

        # Track processed events to avoid high overlap
        processed_spike_events = []

        # Identify spikes
        spikes_found = 0
        for i in range(pre_behavior_days, len(df) - post_behavior_days):
            if global_instance_count >= global_instance_cap:
                print("Global instance cap reached. Stopping spike processing.")
                break

            if spikes_found >= max_spikes_per_stock:
                print(f"Spike cap reached for {file_name}.")
                break

            window_start = i - pre_behavior_days
            window_end = i
            future = df.iloc[i:i + post_behavior_days]

            # Spike condition
            if future["Pct_Change"].max() >= short_spike_threshold:
                # Check for overlap with existing events
                overlap = any(
                    max(start, window_start) < min(end, window_end)
                    for start, end in processed_spike_events
                )

                if not overlap:
                    # Save spike instance
                    window = df.iloc[window_start:window_end]
                    output_file = f"Short_Spike_Instance_{file_name.split('.')[0]}_{window.index[0].strftime('%Y-%m-%d')}_to_{window.index[-1].strftime('%Y-%m-%d')}.csv"
                    window.to_csv(os.path.join(instances_path, output_file))
                    print(f"Saved spike instance: {output_file}")
                    processed_spike_events.append((window_start, window_end))
                    spikes_found += 1
                    global_instance_count += 1
        #
        # Select random non-spike windows
        non_spike_dates = []
        non_spikes_found = 0
        attempts = 0  # To prevent infinite loops
        while len(non_spike_dates) < max_non_spikes_per_stock and attempts < 100 and global_non_instance_count < global_non_instance_cap:
            attempts += 1

            # Generate random start index only if the range is valid
            if len(df) > (pre_behavior_days + post_behavior_days):
                random_start_idx = random.randint(pre_behavior_days, len(df) - post_behavior_days - 1)
            else:
                print(f"Skipping {file_name}: Not enough data for random non-spike sampling.")
                break

            random_window = df.iloc[random_start_idx - pre_behavior_days:random_start_idx]

            # Ensure no spike in the random window
            if random_window["Pct_Change"].max() < short_spike_threshold:
                non_spike_dates.append(random_start_idx)

                # Save non-spike instance
                output_file = f"Short_Spike_Non_Instance_{file_name.split('.')[0]}_{random_window.index[0].strftime('%Y-%m-%d')}_to_{random_window.index[-1].strftime('%Y-%m-%d')}.csv"
                random_window.to_csv(os.path.join(non_instances_path, output_file))
                print(f"Saved non-spike instance: {output_file}")
                non_spikes_found += 1
                global_non_instance_count += 1

print("Processing complete.")

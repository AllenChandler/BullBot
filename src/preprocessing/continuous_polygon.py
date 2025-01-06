import os
import pandas as pd

# Input and output paths
metrics_path = "/mnt/e/projects/BullBot/data/polygon/metrics"
continuous_path = "/mnt/e/projects/BullBot/data/polygon/continuous"
os.makedirs(continuous_path, exist_ok=True)

# Process each daily CSV
for file_name in sorted(os.listdir(metrics_path)):
    if file_name.endswith(".csv"):
        file_path = os.path.join(metrics_path, file_name)
        print(f"Processing file: {file_name}")
        try:
            # Load the day's data
            df = pd.read_csv(file_path)
            print(f"Loaded {len(df)} rows from {file_name}")

            # Ensure required columns exist
            if not {"ticker", "window_start"}.issubset(df.columns):
                print(f"Skipping {file_name}: Missing required columns.")
                continue

            # Process each ticker symbol
            for ticker in df["ticker"].unique():
                ticker_rows = df[df["ticker"] == ticker]

                # Define the output file for the ticker
                output_file = os.path.join(continuous_path, f"{ticker}.csv")

                # Append to the existing CSV or create a new one
                if os.path.exists(output_file):
                    ticker_rows.to_csv(output_file, mode='a', header=False, index=False)
                    print(f"Appended {len(ticker_rows)} rows to {output_file}")
                else:
                    ticker_rows.to_csv(output_file, index=False)
                    print(f"Created {output_file} with {len(ticker_rows)} rows")

        except Exception as e:
            print(f"Error processing {file_name}: {e}")

print("Processing complete.")

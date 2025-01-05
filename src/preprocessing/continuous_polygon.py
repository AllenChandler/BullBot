import os
import pandas as pd

# Input and output paths
metrics_path = "E:/projects/BullBot/data/polygon/metrics"
continuous_path = "E:/projects/BullBot/data/polygon/continuous"
os.makedirs(continuous_path, exist_ok=True)

# Dictionary to store ticker data
ticker_data = {}

# Process each daily CSV
for file_name in sorted(os.listdir(metrics_path)):
    if file_name.endswith(".csv"):
        file_path = os.path.join(metrics_path, file_name)
        print(f"Processing file: {file_name}")
        try:
            # Load the day's data
            df = pd.read_csv(file_path)

            # Ensure required columns exist
            if not {"ticker", "window_start"}.issubset(df.columns):
                print(f"Skipping {file_name}: Missing required columns.")
                continue

            # Process each ticker symbol
            for ticker in df["ticker"].unique():
                ticker_rows = df[df["ticker"] == ticker]

                if ticker not in ticker_data:
                    # Initialize new DataFrame for the ticker
                    ticker_data[ticker] = ticker_rows
                else:
                    # Append rows to existing DataFrame
                    ticker_data[ticker] = pd.concat([ticker_data[ticker], ticker_rows], ignore_index=True)

        except Exception as e:
            print(f"Error processing {file_name}: {e}")

# Save each ticker's data to a separate CSV
for ticker, data in ticker_data.items():
    # Sort by window_start to ensure chronological order
    data.sort_values("window_start", inplace=True)
    output_file = os.path.join(continuous_path, f"{ticker}.csv")
    data.to_csv(output_file, index=False)
    print(f"Saved {ticker} data to {output_file}")

print("Processing complete.")

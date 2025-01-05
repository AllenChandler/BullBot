import os
import pandas as pd
import numpy as np
import joblib

# Paths for live testing
model_path = "/mnt/e/projects/BullBot/models/Short_Spike/trained/short_spike_model.pkl"
preprocessed_data_path = "/mnt/e/projects/BullBot/data/preprocessed"

# Rolling window parameters
ROLLING_WINDOW_SIZE = 180  # Last 180 days
PREDICTION_ALERT_WINDOW = 14  # Days within which a spike is expected

def simulate_live_data(model, start_date=None, end_date=None):
    """
    Simulate live testing by feeding data day-by-day using a rolling window.
    Args:
        model: Trained model for prediction.
        start_date: Start date for the simulation (optional).
        end_date: End date for the simulation (optional).
    """
    # Iterate through all files in the preprocessed data folder
    for file_name in os.listdir(preprocessed_data_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(preprocessed_data_path, file_name)

            # Load data
            df = pd.read_csv(file_path, parse_dates=['Date'], dayfirst=False)
            df.sort_values(by='Date', inplace=True)

            # Filter by date range
            if start_date:
                df = df[df['Date'] >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df['Date'] <= pd.to_datetime(end_date)]

            if len(df) < ROLLING_WINDOW_SIZE:
                print(f"Skipping {file_name}: Insufficient data for a 180-day rolling window.")
                continue

            print(f"Processing {file_name} from {df['Date'].min()} to {df['Date'].max()}.")

            # Step 1: Initialize rolling window with the first 180 days
            rolling_window = df.iloc[:ROLLING_WINDOW_SIZE]
            aggregated_feature = rolling_window['Close'].mean()  # Aggregate to a single feature

            try:
                initial_prediction = model.predict([[aggregated_feature]])
                if initial_prediction[0] == 1:  # Spike detected
                    prediction_date = rolling_window.iloc[-1]['Date']
                    print(f"Initial short spike detected in {file_name} on {prediction_date}!")
            except ValueError as e:
                print(f"Error predicting initial window for {file_name}: {e}")

            # Step 2: Start rolling window analysis day-by-day
            for i in range(ROLLING_WINDOW_SIZE, len(df)):
                # Update the rolling window
                rolling_window = pd.concat([rolling_window.iloc[1:], df.iloc[[i]]])

                # Aggregate features for the updated window
                aggregated_feature = rolling_window['Close'].mean()  # Adjust aggregation as needed

                try:
                    prediction = model.predict([[aggregated_feature]])
                    if prediction[0] == 1:  # Spike detected
                        prediction_date = df.iloc[i]['Date']
                        print(f"Short spike detected in {file_name} on {prediction_date}!")
                except ValueError as e:
                    print(f"Error predicting for {file_name} on index {i}: {e}")

if __name__ == "__main__":
    # Load the trained model
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Trained model not found at {model_path}")
    model = joblib.load(model_path)
    print(f"Loaded model from {model_path}")

    # Specify the date range
    START_DATE = "2018-01-01"
    END_DATE = "2019-12-31"

    # Simulate live data feed
    simulate_live_data(model, start_date=START_DATE, end_date=END_DATE)

import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Updated paths for spike data and models
spike_data_path = "/mnt/e/projects/BullBot/data/polygon/processed/train"
spike_model_path = "/mnt/e/projects/BullBot/models/trained"
os.makedirs(spike_model_path, exist_ok=True)

# Features and label columns
FEATURE_COLUMNS = [
    'volume', 'open', 'close', 'high', 'low', 'price_range', 'price_spread', 
    'midpoint_price', 'average_price', 'avg_trade_size', 'typical_price', 
    'VWAP', 'RSI', 'MACD', 'Signal_Line', 'Bollinger_Upper', 'Bollinger_Lower'
]
LABEL_COLUMN = 'Label'

def load_data():
    """
    Load spike and non-spike data, merge, and prepare training, validation, and testing datasets.
    """
    spike_data = []
    non_spike_data = []

    # Load spike data
    for file_name in os.listdir(f"{spike_data_path}/spikes"):
        if file_name.endswith('.csv'):
            file_path = os.path.join(spike_data_path, "spikes", file_name)
            df = pd.read_csv(file_path)
            spike_data.append(df[FEATURE_COLUMNS].assign(Label=1))

    # Load non-spike data
    for file_name in os.listdir(f"{spike_data_path}/non_spikes"):
        if file_name.endswith('.csv'):
            file_path = os.path.join(spike_data_path, "non_spikes", file_name)
            df = pd.read_csv(file_path)
            non_spike_data.append(df[FEATURE_COLUMNS].assign(Label=0))

    # Combine spike and non-spike data
    full_data = pd.concat(spike_data + non_spike_data, ignore_index=True)

    # Separate features (X) and labels (y)
    X = full_data[FEATURE_COLUMNS].values
    y = full_data[LABEL_COLUMN].values

    return X, y


def train_model(X, y):
    """
    Train a RandomForestClassifier to classify spikes vs. non-spikes.
    """
    # Split the data into training, validation, and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)

    # Train the model
    model.fit(X_train, y_train)

    # Evaluate the model on validation data
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    return model


def save_model(model):
    """
    Save the trained model to disk.
    """
    model_file = os.path.join(spike_model_path, "spike_model.pkl")
    joblib.dump(model, model_file)
    print(f"Model saved to {model_file}")


if __name__ == "__main__":
    # Load data
    print("Loading data...")
    X, y = load_data()

    # Train the model
    print("Training model...")
    model = train_model(X, y)

    # Save the trained model
    print("Saving model...")
    save_model(model)
    print("Spike detection training completed.")

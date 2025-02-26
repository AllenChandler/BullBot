import os
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib
import json

# Updated paths for spike data and models
spike_data_path = "/mnt/e/projects/BullBot/data/polygon/processed/val"
spike_model_path = "/mnt/e/projects/BullBot/models/train"
validation_results_path = "/mnt/e/projects/BullBot/models/val"
os.makedirs(validation_results_path, exist_ok=True)

# Features and label columns
FEATURE_COLUMNS = [
    'volume', 'open', 'close', 'high', 'low', 'price_range', 'price_spread', 
    'midpoint_price', 'average_price', 'avg_trade_size', 'typical_price', 
    'VWAP', 'RSI', 'MACD', 'Signal_Line', 'Bollinger_Upper', 'Bollinger_Lower'
]
LABEL_COLUMN = 'Label'

def load_validation_data():
    """
    Load spike and non-spike validation data from processed directories.
    """
    spike_data = []
    non_spike_data = []

    # Load spike validation data
    for file_name in os.listdir(f"{spike_data_path}/spikes"):
        if file_name.endswith('.csv'):
            file_path = os.path.join(spike_data_path, "spikes", file_name)
            df = pd.read_csv(file_path)
            spike_data.append(df[FEATURE_COLUMNS].assign(Label=1))

    # Load non-spike validation data
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

def validate_model(model, X, y):
    """
    Validate the model on the provided dataset.
    """
    # Predict labels
    y_pred = model.predict(X)

    # Calculate accuracy
    accuracy = accuracy_score(y, y_pred)
    print(f"Validation Accuracy: {accuracy}")

    # Generate classification report
    report = classification_report(y, y_pred, output_dict=True)
    print("Classification Report:")
    print(classification_report(y, y_pred))

    # Generate confusion matrix
    cm = confusion_matrix(y, y_pred)
    print("Confusion Matrix:")
    print(cm)

    return accuracy, report, cm

def save_validation_results(accuracy, report, cm):
    """
    Save the validation results to a JSON file.
    """
    results_file = os.path.join(validation_results_path, "validation_results.json")
    results = {
        "accuracy": accuracy,
        "classification_report": report,
        "confusion_matrix": cm.tolist(),  # Convert to list for JSON serialization
    }

    with open(results_file, 'w') as f:
        json.dump(results, f, indent=4)

    print(f"Validation results saved to {results_file}")

if __name__ == "__main__":
    # Load the trained model
    model_file = os.path.join(spike_model_path, "spike_model.pkl")
    if not os.path.exists(model_file):
        raise FileNotFoundError(f"Trained model not found at {model_file}")
    model = joblib.load(model_file)
    print(f"Loaded model from {model_file}")

    # Load validation data
    print("Loading validation data...")
    X, y = load_validation_data()

    # Validate the model
    print("Validating model...")
    accuracy, report, cm = validate_model(model, X, y)

    # Save the validation results
    print("Saving validation results...")
    save_validation_results(accuracy, report, cm)

    print("Spike validation completed.")

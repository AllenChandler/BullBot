import os
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib

# Paths for behavior data and models
short_spike_data_path = "/mnt/e/projects/BullBot/data/behaviors/Short_Spike"
short_spike_model_path = "/mnt/e/projects/BullBot/models/Short_Spike/trained"
test_results_path = "/mnt/e/projects/BullBot/models/Short_Spike/tested"
os.makedirs(test_results_path, exist_ok=True)

# Features and label columns
FEATURE_COLUMNS = ['Close_MA_10', 'Close_MA_50', 'Volume_MA_10', 'Volume_MA_50']
LABEL_COLUMN = 'Label'

def load_test_data():
    """
    Load short spike test data (instances and non-instances).
    """
    data = []
    labels = []

    # Load spike instances
    for file_name in os.listdir(f"{short_spike_data_path}/Instances"):
        if file_name.endswith('.csv'):
            file_path = os.path.join(short_spike_data_path, "Instances", file_name)
            df = pd.read_csv(file_path)

            # Ensure Moving Averages columns exist
            missing_columns = set(FEATURE_COLUMNS) - set(df.columns)
            if missing_columns:
                print(f"Skipping {file_name}: Missing columns {missing_columns}")
                continue

            data.append(df[FEATURE_COLUMNS].values)
            labels.extend([1] * len(df))  # Label as spike

    # Load non-spike instances
    for file_name in os.listdir(f"{short_spike_data_path}/Non_Instances"):
        if file_name.endswith('.csv'):
            file_path = os.path.join(short_spike_data_path, "Non_Instances", file_name)
            df = pd.read_csv(file_path)

            # Ensure Moving Averages columns exist
            missing_columns = set(FEATURE_COLUMNS) - set(df.columns)
            if missing_columns:
                print(f"Skipping {file_name}: Missing columns {missing_columns}")
                continue

            data.append(df[FEATURE_COLUMNS].values)
            labels.extend([0] * len(df))  # Label as non-spike

    # Flatten and combine data
    X = np.vstack(data)  # Combine all rows into a single numpy array
    y = np.array(labels)  # Convert labels to numpy array
    return X, y

def test_model(model, X, y):
    """
    Test the model on the provided dataset.
    """
    print(f"X shape: {X.shape}, y shape: {y.shape}")  # Debug print
    # Predict labels
    y_pred = model.predict(X)
    print(f"y_pred shape: {y_pred.shape}")  # Debug print

    # Calculate accuracy
    accuracy = accuracy_score(y, y_pred)
    print(f"Test Accuracy: {accuracy}")

    # Generate classification report
    report = classification_report(y, y_pred, output_dict=True)
    print("Classification Report:")
    print(classification_report(y, y_pred))

    # Generate confusion matrix
    cm = confusion_matrix(y, y_pred)
    print("Confusion Matrix:")
    print(cm)

    return accuracy, report, cm

def save_test_results(accuracy, report, cm):
    """
    Save the test results to a JSON file.
    """
    results_file = os.path.join(test_results_path, "test_results_with_ma.json")
    results = {
        "accuracy": accuracy,
        "classification_report": report,
        "confusion_matrix": cm.tolist(),  # Convert to list for JSON serialization
    }

    with open(results_file, 'w') as f:
        import json
        json.dump(results, f, indent=4)

    print(f"Test results saved to {results_file}")

if __name__ == "__main__":
    # Load the trained model
    model_file = os.path.join(short_spike_model_path, "short_spike_model_with_ma.pkl")
    if not os.path.exists(model_file):
        raise FileNotFoundError(f"Trained model not found at {model_file}")
    model = joblib.load(model_file)
    print(f"Loaded model from {model_file}")

    # Load test data
    print("Loading test data...")
    X, y = load_test_data()

    # Test the model
    print("Testing model...")
    accuracy, report, cm = test_model(model, X, y)

    # Save the test results
    print("Saving test results...")
    save_test_results(accuracy, report, cm)

    print("Short spike testing completed.")

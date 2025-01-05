import os
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib

# Paths for behavior data and models
short_spike_data_path = "/mnt/e/projects/BullBot/data/behaviors/Short_Spike"
short_spike_model_path = "/mnt/e/projects/BullBot/models/Short_Spike/trained"
validation_results_path = "/mnt/e/projects/BullBot/models/Short_Spike/validated"
os.makedirs(validation_results_path, exist_ok=True)

# Features and label columns
FEATURE_COLUMN = 'Close'  # Use only the Close price
LABEL_COLUMN = 'Label'

def load_validation_data():
    """
    Load short spike validation data (instances and non-instances).
    """
    data = []
    labels = []

    # Load instances
    for file_name in os.listdir(f"{short_spike_data_path}/Instances"):
        if file_name.endswith('.csv'):
            file_path = os.path.join(short_spike_data_path, "Instances", file_name)
            df = pd.read_csv(file_path)
            data.extend(df[FEATURE_COLUMN].values.tolist())
            labels.extend([1] * len(df))  # Label as spike

    # Load non-instances
    for file_name in os.listdir(f"{short_spike_data_path}/Non_Instances"):
        if file_name.endswith('.csv'):
            file_path = os.path.join(short_spike_data_path, "Non_Instances", file_name)
            df = pd.read_csv(file_path)
            data.extend(df[FEATURE_COLUMN].values.tolist())
            labels.extend([0] * len(df))  # Label as non-spike

    # Convert data to numpy arrays
    X = np.array(data).reshape(-1, 1)  # Reshape for a single feature
    y = np.array(labels)
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
        import json
        json.dump(results, f, indent=4)

    print(f"Validation results saved to {results_file}")

if __name__ == "__main__":
    # Load the trained model
    model_file = os.path.join(short_spike_model_path, "short_spike_model.pkl")
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

    print("Short spike validation completed.")

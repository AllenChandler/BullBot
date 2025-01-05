import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Paths for behavior data and models
short_spike_data_path = "/mnt/e/projects/BullBot/data/behaviors/Short_Spike"
short_spike_model_path = "/mnt/e/projects/BullBot/models/Short_Spike/trained"
os.makedirs(short_spike_model_path, exist_ok=True)

# Features and label columns
FEATURE_COLUMNS = ['Close_MA_10', 'Close_MA_50', 'Volume_MA_10', 'Volume_MA_50']
LABEL_COLUMN = 'Label'

def load_data():
    """
    Load short spike instance and non-instance data, including Moving Averages.
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
            labels.extend([1] * len(df))  # Label each row as spike (1)

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
            labels.extend([0] * len(df))  # Label each row as non-spike (0)

    # Flatten and combine all data
    X = np.vstack(data)  # Combine all rows into a single array
    y = np.array(labels)  # Convert labels to a single array
    return X, y

def train_model(X, y):
    """
    Train a RandomForestClassifier to classify short spikes vs non-spikes.
    """
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)

    # Train the model
    model.fit(X_train, y_train)

    # Evaluate the model
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
    model_file = os.path.join(short_spike_model_path, "short_spike_model_with_ma.pkl")
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
    print("Short spike training completed.")

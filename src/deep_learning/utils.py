import torch
import os
import yaml
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Load config file
CONFIG_PATH = "E:/projects/BullBot_backup/config.yaml"
with open(CONFIG_PATH, "r") as file:
    config = yaml.safe_load(file)

# Paths from config
model_path = config["dl_training"]["model_save_path"]

# ------------------------------
# ✅ Save and Load Model
# ------------------------------

def save_model(model, path=model_path):
    """Save trained model to the specified path."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    torch.save(model.state_dict(), path)
    print(f"✅ Model saved at: {path}")

def load_model(model_class, input_size, path=model_path):
    """Load a trained model from the specified path."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ Model file not found: {path}")

    model = model_class(input_size=input_size)
    model.load_state_dict(torch.load(path))
    model.eval()
    print(f"✅ Model loaded from: {path}")
    return model

# ------------------------------
# ✅ Data Scaling Helpers
# ------------------------------

def fit_scaler(data):
    """Fit and return a MinMaxScaler for dataset normalization."""
    scaler = MinMaxScaler()
    scaler.fit(data)
    return scaler

def scale_data(data, scaler):
    """Scale dataset using a given MinMaxScaler."""
    return scaler.transform(data)

def inverse_scale(data, scaler):
    """Inverse transform dataset back to original scale."""
    return scaler.inverse_transform(data)


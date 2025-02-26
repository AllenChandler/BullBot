import os
import yaml
import torch
import numpy as np
from model import StockTransformer  # Import model architecture
from preprocess import scaler  # Import the same scaler used in preprocessing

# Load config file
CONFIG_PATH = "E:/projects/BullBot_backup/config.yaml"
with open(CONFIG_PATH, "r") as file:
    config = yaml.safe_load(file)

# Paths from config
model_path = config["dl_training"]["model_save_path"]
data_dir = config["data_paths"]["processed_deep_learning"]

# Ensure model exists
if not os.path.exists(model_path):
    raise FileNotFoundError(f"❌ Model file not found: {model_path}")

# Load trained model
input_size = len(config["preprocessing"]["metrics_columns"]) - 1  # Exclude target column
model = StockTransformer(input_size=input_size)
model.load_state_dict(torch.load(model_path))
model.eval()  # Set model to evaluation mode

# Load latest processed data
file_list = sorted([f for f in os.listdir(data_dir) if f.endswith(".npy")])
if not file_list:
    raise FileNotFoundError(f"❌ No .npy files found in {data_dir}")

latest_file = os.path.join(data_dir, file_list[-1])
print(f"✅ Using latest file: {latest_file}")

# Load and normalize new data
data = np.load(latest_file)
data = torch.tensor(data, dtype=torch.float32)

# Make prediction
with torch.no_grad():
    prediction = model(data)
    predicted_price = prediction.numpy().flatten()

# Convert back to original scale
predicted_price = scaler.inverse_transform(predicted_price.reshape(-1, 1))

print(f"📈 Predicted Price: {predicted_price[-1][0]:.4f}")

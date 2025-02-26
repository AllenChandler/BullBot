import os
import yaml
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from torch.utils.data import TensorDataset, DataLoader
from model import StockTransformer  # Importing model architecture

# Load config file
CONFIG_PATH = "E:/projects/BullBot_backup/config.yaml"
with open(CONFIG_PATH, "r") as file:
    config = yaml.safe_load(file)

# Paths from config
data_dir = config["data_paths"]["processed_deep_learning"]
model_save_path = config["dl_training"]["model_save_path"]

# Training hyperparameters from config
batch_size = config["dl_training"]["batch_size"]
learning_rate = config["dl_training"]["learning_rate"]
num_epochs = config["dl_training"]["num_epochs"]

# Load all .npy files from processed deep learning data folder
file_list = [f for f in os.listdir(data_dir) if f.endswith(".npy")]
if not file_list:
    raise FileNotFoundError(f"No .npy files found in {data_dir}")

# Load data
data_list = [np.load(os.path.join(data_dir, file)) for file in file_list]
full_data = np.vstack(data_list)  # Combine all tickers into one dataset

# Convert to PyTorch tensors
X_tensor = torch.tensor(full_data[:, :-1], dtype=torch.float32)  # Features (all but last column)
y_tensor = torch.tensor(full_data[:, -1], dtype=torch.float32).unsqueeze(1)  # Labels (last column)

# Create DataLoader
dataset = TensorDataset(X_tensor, y_tensor)
data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

# Initialize model
input_size = X_tensor.shape[1]
model = StockTransformer(input_size=input_size)

# Loss function & optimizer
criterion = nn.MSELoss()
optimizer = optim.AdamW(model.parameters(), lr=learning_rate)

# Training loop
for epoch in range(num_epochs):
    model.train()
    total_loss = 0

    for batch in data_loader:
        X_batch, y_batch = batch
        optimizer.zero_grad()
        output = model(X_batch)
        loss = criterion(output, y_batch)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    print(f"Epoch [{epoch+1}/{num_epochs}] - Loss: {total_loss:.4f}")

# Save trained model
os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
torch.save(model.state_dict(), model_save_path)
print(f"✅ Model training complete. Saved to {model_save_path}.")

import torch
import torch.nn as nn

class StockTransformer(nn.Module):
    def __init__(self, input_size, num_heads=8, hidden_size=64, num_layers=4):
        super(StockTransformer, self).__init__()
        self.embedding = nn.Linear(input_size, hidden_size)  # Embed input features
        encoder_layer = nn.TransformerEncoderLayer(d_model=hidden_size, nhead=num_heads)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.fc = nn.Linear(hidden_size, 1)  # Predict next price movement

    def forward(self, x):
        x = self.embedding(x)
        x = self.transformer(x)
        x = self.fc(x[:, -1, :])  # Use last timestep for prediction
        return x

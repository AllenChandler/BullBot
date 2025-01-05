import os
import pandas as pd

cleaned_data_path = "/mnt/e/projects/BullBot/data/polygon/clean"
metrics_data_path = "/mnt/e/projects/BullBot/data/polygon/metrics"
os.makedirs(metrics_data_path, exist_ok=True)

def calculate_metrics(file_path):
    try:
        df = pd.read_csv(file_path)
        df['price_range'] = df['high'] - df['low']
        df['price_spread'] = df['close'] - df['open']
        df['midpoint_price'] = (df['high'] + df['low']) / 2
        df['average_price'] = (df['open'] + df['close'] + df['high'] + df['low']) / 4
        df['avg_trade_size'] = df['volume'] / df['transactions']
        df['typical_price'] = (df['high'] + df['low'] + df['close']) / 3
        df['VWAP'] = (df['typical_price'] * df['volume']).cumsum() / df['volume'].cumsum()
        window = 14
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        short_ema = df['close'].ewm(span=12, adjust=False).mean()
        long_ema = df['close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = short_ema - long_ema
        df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
        sma = df['close'].rolling(window=20).mean()
        std = df['close'].rolling(window=20).std()
        df['Bollinger_Upper'] = sma + (2 * std)
        df['Bollinger_Lower'] = sma - (2 * std)

        save_path = os.path.join(metrics_data_path, os.path.basename(file_path))
        df.to_csv(save_path, index=False)
        print(f"Metrics calculated and saved to {save_path}")
    except Exception as e:
        print(f"Error calculating metrics for {file_path}: {e}")

for file_name in os.listdir(cleaned_data_path):
    if file_name.endswith('.csv'):
        file_path = os.path.join(cleaned_data_path, file_name)
        calculate_metrics(file_path)

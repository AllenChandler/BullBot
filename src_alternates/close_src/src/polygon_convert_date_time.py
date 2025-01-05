import pandas as pd
import datetime

# Path to the input CSV file
input_file = "/mnt/e/projects/BullBot/data/polygon/2025-01/2025-01-02.csv"

# Path to save the updated CSV file
output_file = "/mnt/e/projects/BullBot/data/polygon/2025-01/2025-01-02_with_datetime.csv"

# Load the CSV file
data = pd.read_csv(input_file)

# Convert 'window_start' (UNIX nanoseconds) to human-readable datetime
# Assuming 'window_start' is the 7th column (index 6)
data['Converted_Time'] = data['window_start'].apply(
    lambda x: datetime.datetime.utcfromtimestamp(x / 1e9)
)

# Save the updated DataFrame with the new column
data.to_csv(output_file, index=False)

print(f"Updated file saved to: {output_file}")

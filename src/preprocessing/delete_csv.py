import os

# Specify the folder path
folder_path = "/mnt/e/projects/BullBot/data/polygon/processed/spikes"

# Delete all .csv files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith(".csv"):
        file_path = os.path.join(folder_path, file_name)
        os.remove(file_path)
        print(f"Deleted: {file_path}")

print("All .csv files deleted.")

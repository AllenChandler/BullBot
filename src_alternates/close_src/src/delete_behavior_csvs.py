import os
import glob

# Define the base path for behavior subfolders
base_path = "/mnt/e/projects/BullBot/data/behaviors/Short_Spike"

# List of subfolders to clean
subfolders = ['Instances', 'Non_Instances']

# Iterate over each subfolder and delete all CSV files
for subfolder in subfolders:
    folder_path = os.path.join(base_path, subfolder)
    csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

    for csv_file in csv_files:
        try:
            os.remove(csv_file)
            print(f"Deleted: {csv_file}")
        except Exception as e:
            print(f"Error deleting {csv_file}: {e}")

print("Cleanup completed.")

import os
import glob

# Define the directories to clean
directories = {
    "tested_json": "/mnt/e/projects/BullBot/models/Short_Spike/tested/*.json",
    "trained_pkl": "/mnt/e/projects/BullBot/models/Short_Spike/trained/*.pkl",
    "validated_json": "/mnt/e/projects/BullBot/models/Short_Spike/validated/*.json",
    "preprocessed_csvs": "/mnt/e/projects/BullBot/data/preprocessed/*.csv",
    "instances_csvs": "/mnt/e/projects/BullBot/data/behaviors/Short_Spike/Instances/*.csv",
    "non_instances_csvs": "/mnt/e/projects/BullBot/data/behaviors/Short_Spike/Non_Instances/*.csv",
}

# Function to delete files in a directory
def delete_files(file_pattern):
    files = glob.glob(file_pattern)
    for file_path in files:
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

# Perform the cleanup
for desc, path in directories.items():
    print(f"Cleaning up: {desc}")
    delete_files(path)

print("Reset completed.")

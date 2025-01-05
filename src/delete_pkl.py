import os

# Define the path to the models folder
models_path = r'J:\projects\BullBot\models'

# Iterate through all files in the models folder
for file_name in os.listdir(models_path):
    if file_name.endswith('.pkl'):
        file_path = os.path.join(models_path, file_name)
        os.remove(file_path)
        print(f"Deleted: {file_path}")

print("All .pkl files deleted from the models folder.")
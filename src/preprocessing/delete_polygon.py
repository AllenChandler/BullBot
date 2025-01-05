import os
import shutil

# Path to the directory
directory_path = "/mnt/e/projects/BullBot/data/polygon"

def delete_directory_contents(directory):
    try:
        # Iterate through all files and subdirectories in the directory
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Remove files or symbolic links
                print(f"Deleted file: {file_path}")
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Remove directories
                print(f"Deleted directory: {file_path}")
        print(f"All contents of {directory} have been deleted.")
    except Exception as e:
        print(f"Error deleting contents of {directory}: {e}")

# Delete contents
delete_directory_contents(directory_path)

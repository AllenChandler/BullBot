import os

output_file = "output.txt"
excluded_folder = "BullBot_env"
extensions = {".py", ".md", ".yaml"}

with open(output_file, "w") as f:
    for root, dirs, files in os.walk("."):
        # Skip the excluded folder
        if excluded_folder in root:
            continue

        # Write folder name
        f.write(f"Folder: {root}\n")

        # Write matching files
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                f.write(f"  {file}\n")
print(f"Results saved to {output_file}")
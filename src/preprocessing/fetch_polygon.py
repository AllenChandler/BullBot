import boto3
from botocore.config import Config
import os
import gzip
from datetime import datetime

# Initialize a session using your credentials
session = boto3.Session(
    aws_access_key_id='ce684351-10ba-4d1e-806d-5961663827ff',
    aws_secret_access_key='ye2dmLxOV9UyfNjKueksGKbcBoWWkcm_',
)

s3 = session.client(
    's3',
    endpoint_url='https://files.polygon.io',
    config=Config(signature_version='s3v4'),
)

# User-specified start and end dates (YYYY-MM-DD format)
start_date_str = "2024-03-22"  # Change as needed
end_date_str = "2024-04-30"    # Change as needed
start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

# Specify the local directory for saving files
local_directory = '/mnt/e/projects/BullBot/data/polygon/raw'
os.makedirs(local_directory, exist_ok=True)

# Prefix for US stocks SIP data
prefix = 'us_stocks_sip/'
paginator = s3.get_paginator('list_objects_v2')

# Function to decompress .gz files
def decompress_gz_to_csv(gz_file_path, csv_file_path):
    try:
        with gzip.open(gz_file_path, 'rb') as f_in:
            with open(csv_file_path, 'wb') as f_out:
                f_out.write(f_in.read())
        print(f"Decompressed: {gz_file_path} -> {csv_file_path}")
        os.remove(gz_file_path)  # Remove the .gz file
    except Exception as e:
        print(f"Error decompressing {gz_file_path}: {e}")

print(f"Fetching files for date range: {start_date_str} to {end_date_str}")
for page in paginator.paginate(Bucket='flatfiles', Prefix=prefix):
    for obj in page.get('Contents', []):
        object_key = obj['Key']
        file_date_str = object_key.split('/')[-1].split('.')[0]
        try:
            file_date = datetime.strptime(file_date_str, "%Y-%m-%d")
        except ValueError:
            continue

        if start_date <= file_date <= end_date:
            local_file_name = object_key.split('/')[-1]
            local_file_path = os.path.join(local_directory, local_file_name)
            print(f"Downloading {object_key} to {local_file_path}...")
            try:
                s3.download_file('flatfiles', object_key, local_file_path)
                csv_file_path = local_file_path[:-3]
                decompress_gz_to_csv(local_file_path, csv_file_path)
            except Exception as e:
                print(f"Error processing {object_key}: {e}")

print("Download and decompression complete.")

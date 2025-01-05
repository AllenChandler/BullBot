# Install boto3
# pip install boto3

# Fetch your S3 Access and Secret keys from
# https://polygon.io/dashboard/flat-files

# Quickstart
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html


import boto3
from botocore.config import Config
import os

# Initialize a session using your credentials
session = boto3.Session(
   aws_access_key_id='ce684351-10ba-4d1e-806d-5961663827ff',
   aws_secret_access_key='ye2dmLxOV9UyfNjKueksGKbcBoWWkcm_',
)

# Create a client with your session and specify the endpoint
s3 = session.client(
    's3',
    endpoint_url='https://files.polygon.io',
    config=Config(signature_version='s3v4'),
)

# Specify the prefix for the month (e.g., January 2025)
prefix = 'us_stocks_sip/minute_aggs_v1/2025/01/'  # Adjust to the desired year and month
bucket_name = 'flatfiles'

# Specify the local directory for saving files
local_directory = '/mnt/e/projects/BullBot/data/polygon/2025-01'
os.makedirs(local_directory, exist_ok=True)

# List and download all files for the specified prefix
paginator = s3.get_paginator('list_objects_v2')
print(f"Listing and downloading objects under prefix: {prefix}")

for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
    for obj in page.get('Contents', []):
        object_key = obj['Key']
        local_file_name = object_key.split('/')[-1]  # Extract file name from key
        local_file_path = os.path.join(local_directory, local_file_name)

        print(f"Downloading {object_key} to {local_file_path}...")
        s3.download_file(bucket_name, object_key, local_file_path)

print("All files downloaded successfully.")
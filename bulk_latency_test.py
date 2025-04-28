import boto3
import time
import requests
import csv
from datetime import datetime

# AWS setup
BUCKET_NAME = "lantency-test"
FILE_NAME = "file_example_MP3_700KB.mp3"
SOUNDTRAP_URL = "https://www.soundtrap.com"
CSV_FILE = "latency_results_bulk.csv"

# Set up AWS S3 client
s3 = boto3.client("s3")

# Function: Upload to S3
def test_s3_upload():
    start = time.time()
    s3.upload_file(FILE_NAME, BUCKET_NAME, FILE_NAME)
    return round(time.time() - start, 3)

# Function: Download from S3
def test_s3_download():
    start = time.time()
    s3.download_file(BUCKET_NAME, FILE_NAME, f"downloaded_{FILE_NAME}")
    return round(time.time() - start, 3)

# Function: Ping Soundtrap
def test_soundtrap_latency():
    start = time.time()
    requests.get(SOUNDTRAP_URL, timeout=10)
    return round((time.time() - start) * 1000, 2)

# Create or append to CSV
def log_to_csv(timestamp, upload, download, soundtrap):
    file_exists = False
    try:
        with open(CSV_FILE, "r"):
            file_exists = True
    except FileNotFoundError:
        pass

    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "File", "Upload (s)", "Download (s)", "Soundtrap (ms)"])
        writer.writerow([timestamp, FILE_NAME, upload, download, soundtrap])

# Main loop to run 1000 tests
for i in range(1000):
    print(f"\nRunning test #{i + 1}/1000")

    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        upload_latency = test_s3_upload()
        download_latency = test_s3_download()
        soundtrap_latency = test_soundtrap_latency()

        print(f"Upload: {upload_latency}s | Download: {download_latency}s | Soundtrap: {soundtrap_latency}ms")

        log_to_csv(timestamp, upload_latency, download_latency, soundtrap_latency)

        # Optional: Add delay between runs to avoid API throttling
        time.sleep(1)

    except Exception as e:
        print(f"Error on run #{i + 1}: {e}")
        time.sleep(3)

import boto3
import time
import requests
import csv
from datetime import datetime

# Configuration
BUCKET_NAME = "lantency-test"
FILE_NAME = "file_example_MP3_700KB.mp3"
SOUNDTRAP_URL = "https://www.soundtrap.com"
CSV_FILE = "latency_results.csv"

# AWS S3 client
s3 = boto3.client("s3")

# Test upload latency
def test_s3_upload():
    start = time.time()
    s3.upload_file(FILE_NAME, BUCKET_NAME, FILE_NAME)
    return round(time.time() - start, 2)

# Test download latency
def test_s3_download():
    start = time.time()
    s3.download_file(BUCKET_NAME, FILE_NAME, f"downloaded_{FILE_NAME}")
    return round(time.time() - start, 2)

# Test Soundtrap page load time
def test_soundtrap_latency():
    start = time.time()
    requests.get(SOUNDTRAP_URL, timeout=10)
    return round((time.time() - start) * 1000, 2)

# Save results to CSV
def log_to_csv(upload, download, soundtrap):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_exists = False
    try:
        with open(CSV_FILE, "r"):
            file_exists = True
    except FileNotFoundError:
        pass

    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "File", "Upload (s)", "Download (s)", "Soundtrap (ms)"])
        writer.writerow([timestamp, FILE_NAME, upload, download, soundtrap])

# Run the tests
if __name__ == "__main__":
    print("Running latency tests...\n")

    upload_latency = test_s3_upload()
    print(f"S3 Upload: {upload_latency} sec")

    download_latency = test_s3_download()
    print(f"S3 Download: {download_latency} sec")

    soundtrap_latency = test_soundtrap_latency()
    print(f"Soundtrap Page Latency: {soundtrap_latency} ms")

    log_to_csv(upload_latency, download_latency, soundtrap_latency)
    print("\nResults saved to latency_results.csv")

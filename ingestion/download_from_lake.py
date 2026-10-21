
import os
from pathlib import Path

import boto3
from botocore.client import Config
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

RAW_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_FILE = RAW_DIR / "sales_from_lake.csv"
OBJECT_KEY = "raw/sales.csv"

ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")
ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
SECRET_KEY = os.getenv("S3_SECRET_KEY")
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

if not all([ENDPOINT_URL, ACCESS_KEY, SECRET_KEY, BUCKET_NAME]):
    raise ValueError("Missing S3 configuration in the .env file.")

s3 = boto3.client(
    "s3",
    endpoint_url=ENDPOINT_URL,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name="us-east-1",
    config=Config(signature_version="s3v4"),
)


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    s3.download_file(
        BUCKET_NAME,
        OBJECT_KEY,
        str(OUTPUT_FILE),
    )

    print("Download completed successfully!")
    print(f"Downloaded object: {OBJECT_KEY}")
    print(f"Saved locally to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

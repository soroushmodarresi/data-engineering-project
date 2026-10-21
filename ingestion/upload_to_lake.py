
import os
from pathlib import Path

import boto3
from botocore.client import Config
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

RAW_DIR = PROJECT_ROOT / "data" / "raw"

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
    for filename in ["sales.csv", "sales_metadata.json"]:
        file_path = RAW_DIR / filename

        if not file_path.exists():
            raise FileNotFoundError(f"Missing file: {file_path}")

        s3.upload_file(
            str(file_path),
            BUCKET_NAME,
            f"raw/{filename}",
        )
        print(f"Uploaded {filename}")

    print("\nFiles in the data lake:")
    response = s3.list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix="raw/",
    )

    for item in response.get("Contents", []):
        print(f"{item['Key']} — {item['Size']} bytes")


if __name__ == "__main__":
    main()

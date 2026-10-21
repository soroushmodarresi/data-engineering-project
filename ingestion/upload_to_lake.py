
from pathlib import Path

import boto3
from botocore.client import Config

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:8333",
    aws_access_key_id="localaccess",
    aws_secret_access_key="localsecret",
    region_name="us-east-1",
    config=Config(signature_version="s3v4"),
)

BUCKET_NAME = "sales-data-lake"

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

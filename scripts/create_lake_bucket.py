
import boto3
from botocore.client import Config

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:8333",
    aws_access_key_id="localaccess",
    aws_secret_access_key="localsecret",
    region_name="us-east-1",
    config=Config(signature_version="s3v4"),
)

bucket_name = "sales-data-lake"

existing_buckets = s3.list_buckets()["Buckets"]

if any(bucket["Name"] == bucket_name for bucket in existing_buckets):
    print(f"Bucket already exists: {bucket_name}")
else:
    s3.create_bucket(Bucket=bucket_name)
    print(f"Bucket created: {bucket_name}")

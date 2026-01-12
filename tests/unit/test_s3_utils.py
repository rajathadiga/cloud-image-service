import boto3
from moto import mock_aws

from src.utils.s3_utils import generate_upload_url, generate_download_url
from src.config import BUCKET_NAME


@mock_aws
def test_generate_upload_url():
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=BUCKET_NAME)

    url, key = generate_upload_url("image/jpeg")

    assert url.startswith("http")
    assert key.startswith("images/")


@mock_aws
def test_generate_download_url():
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=BUCKET_NAME)

    url = generate_download_url("images/test.jpg")

    assert url.startswith("http")

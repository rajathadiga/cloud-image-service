import boto3
import os

AWS_REGION = "us-east-1"

AWS_ENDPOINT = os.getenv("AWS_ENDPOINT_URL")  # None in tests


def get_s3_client():
    return boto3.client(
        "s3",
        region_name=AWS_REGION,
        endpoint_url=AWS_ENDPOINT,
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )


def get_dynamodb_resource():
    return boto3.resource(
        "dynamodb",
        region_name=AWS_REGION,
        endpoint_url=AWS_ENDPOINT,
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )

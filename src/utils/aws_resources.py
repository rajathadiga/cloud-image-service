import boto3

AWS_ENDPOINT = "http://localhost:4566"
AWS_REGION = "us-east-1"


def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=AWS_ENDPOINT,
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name=AWS_REGION,
    )


def get_dynamodb_resource():
    return boto3.resource(
        "dynamodb",
        endpoint_url=AWS_ENDPOINT,
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name=AWS_REGION,
    )

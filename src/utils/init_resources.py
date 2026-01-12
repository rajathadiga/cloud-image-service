from .aws_resources import get_s3_client, get_dynamodb_resource

BUCKET_NAME = "images-bucket"
TABLE_NAME = "images"


def init():
    s3 = get_s3_client()
    dynamodb = get_dynamodb_resource()

    # Create S3 bucket
    s3.create_bucket(Bucket=BUCKET_NAME)

    # Create DynamoDB table
    dynamodb.create_table(
        TableName=TABLE_NAME,
        KeySchema=[
            {"AttributeName": "image_id", "KeyType": "HASH"}
        ],
        AttributeDefinitions=[
            {"AttributeName": "image_id", "AttributeType": "S"}
        ],
        BillingMode="PAY_PER_REQUEST",
    )


if __name__ == "__main__":
    init()

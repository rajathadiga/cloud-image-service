import boto3
from moto import mock_aws

from src.db.image_repository import save_image_metadata, list_images
from src.config import TABLE_NAME


@mock_aws
def test_save_and_list_image():
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    dynamodb.create_table(
        TableName=TABLE_NAME,
        KeySchema=[{"AttributeName": "image_id", "KeyType": "HASH"}],
        AttributeDefinitions=[
            {"AttributeName": "image_id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )

    save_image_metadata(
        user_id="user123",
        s3_key="images/test.jpg",
        tags=["travel"],
        description="Test image",
    )

    images = list_images(user_id="user123")

    assert len(images) == 1
    assert images[0]["user_id"] == "user123"
    assert "travel" in images[0]["tags"]


@mock_aws
def test_list_images_by_tag():
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    table = dynamodb.create_table(
        TableName=TABLE_NAME,
        KeySchema=[{"AttributeName": "image_id", "KeyType": "HASH"}],
        AttributeDefinitions=[
            {"AttributeName": "image_id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )
    table.wait_until_exists()

    # Insert test data ONCE
    save_image_metadata("user1", "img1", ["travel"], "desc1")
    save_image_metadata("user1", "img2", ["food"], "desc2")

    images = list_images(tag="travel")

    assert len(images) == 1
    assert images[0]["s3_key"] == "img1"

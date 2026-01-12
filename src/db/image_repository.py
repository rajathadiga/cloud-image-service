import uuid
from datetime import datetime
from src.config import TABLE_NAME
from src.utils.aws_resources import get_dynamodb_resource


def save_image_metadata(user_id: str, s3_key: str, tags: list, description: str):
    table = get_dynamodb_resource().Table(TABLE_NAME)

    image_id = str(uuid.uuid4())

    item = {
        "image_id": image_id,
        "user_id": user_id,
        "s3_key": s3_key,
        "tags": tags,
        "description": description,
        "upload_time": datetime.utcnow().isoformat()
    }

    table.put_item(Item=item)
    return item


def list_images(user_id: str | None = None):
    table = get_dynamodb_resource().Table(TABLE_NAME)

    response = table.scan()
    items = response.get("Items", [])

    if user_id:
        items = [item for item in items if item["user_id"] == user_id]

    return items


def get_image_by_id(image_id: str):
    table = get_dynamodb_resource().Table(TABLE_NAME)

    response = table.get_item(
        Key={"image_id": image_id}
    )

    return response.get("Item")

def delete_image_metadata(image_id: str):
    table = get_dynamodb_resource().Table(TABLE_NAME)

    table.delete_item(
        Key={"image_id": image_id}
    )

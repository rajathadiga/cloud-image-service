import uuid
from datetime import datetime
from src.utils.aws_resources import get_dynamodb_resource
from src.config import TABLE_NAME


def save_image_metadata(user_id: str, s3_key: str, tags: list, description: str):
    table = get_dynamodb_resource().Table(TABLE_NAME)

    image_id = str(uuid.uuid4())

    item = {
        "image_id": image_id,
        "user_id": user_id,
        "s3_key": s3_key,
        "tags": tags,
        "description": description,
        "upload_time": datetime.utcnow().isoformat(),
    }

    table.put_item(Item=item)
    return item


def list_images(
    user_id: str | None = None,
    tag: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
):
    table = get_dynamodb_resource().Table(TABLE_NAME)

    response = table.scan()
    items = response.get("Items", [])

    if user_id:
        items = [item for item in items if item["user_id"] == user_id]

    if tag:
        items = [item for item in items if tag in item.get("tags", [])]

    if start_date:
        from datetime import datetime
        start = datetime.fromisoformat(start_date)
        items = [
            item for item in items
            if datetime.fromisoformat(item["upload_time"]) >= start
        ]

    if end_date:
        from datetime import datetime
        end = datetime.fromisoformat(end_date)
        items = [
            item for item in items
            if datetime.fromisoformat(item["upload_time"]) <= end
        ]

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

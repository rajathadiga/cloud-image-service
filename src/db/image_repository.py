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

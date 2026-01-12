from src.utils.aws_resources import get_s3_client
from src.config import BUCKET_NAME
import uuid


def generate_upload_url(content_type: str):
    s3 = get_s3_client()
    image_key = f"images/{uuid.uuid4()}"

    url = s3.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": BUCKET_NAME,
            "Key": image_key,
            "ContentType": content_type,
        },
        ExpiresIn=300,
    )

    return url, image_key


def generate_download_url(s3_key: str):
    s3 = get_s3_client()

    url = s3.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": BUCKET_NAME,
            "Key": s3_key,
        },
        ExpiresIn=300,
    )

    return url

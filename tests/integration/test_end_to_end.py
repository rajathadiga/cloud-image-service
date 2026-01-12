import requests
import tempfile
import os

BASE_URL = "http://127.0.0.1:8000"


def test_full_image_flow():
    # 1. Health check
    r = requests.get(f"{BASE_URL}/health")
    assert r.status_code == 200

    # 2. Upload image (get presigned URL)
    payload = {
        "user_id": "integration_user",
        "content_type": "image/jpeg",
        "tags": ["integration"],
        "description": "integration test image",
    }

    r = requests.post(f"{BASE_URL}/images/upload", json=payload)
    assert r.status_code == 200

    data = r.json()
    upload_url = data["upload_url"]
    image_id = data["image_id"]

    # 3. Upload actual image to S3
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"fake-image-data")
        temp_path = f.name

    with open(temp_path, "rb") as f:
        put_resp = requests.put(
            upload_url,
            data=f,
            headers={"Content-Type": "image/jpeg"},
        )
        assert put_resp.status_code in [200, 204]

    os.remove(temp_path)

    # 4. List images
    r = requests.get(f"{BASE_URL}/images",
                     params={"user_id": "integration_user"})
    assert r.status_code == 200
    images = r.json()
    assert len(images) == 1

    # 5. Download image
    r = requests.get(f"{BASE_URL}/images/{image_id}/download")
    assert r.status_code == 200
    download_url = r.json()["download_url"]

    download_resp = requests.get(download_url)
    assert download_resp.status_code == 200

    # 6. Delete image
    r = requests.delete(f"{BASE_URL}/images/{image_id}")
    assert r.status_code == 200

    # 7. Verify delete
    r = requests.get(f"{BASE_URL}/images/{image_id}/download")
    assert r.status_code == 404

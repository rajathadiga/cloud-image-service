from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.db.image_repository import get_image_by_id
from src.utils.s3_utils import generate_download_url
from fastapi import HTTPException
from src.db.image_repository import delete_image_metadata
from src.utils.s3_utils import delete_image_from_s3


from src.utils.s3_utils import generate_upload_url
from src.db.image_repository import save_image_metadata, list_images

app = FastAPI(title="Cloud Image Service")

# CORS (needed for Swagger / browser)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UploadRequest(BaseModel):
    user_id: str
    content_type: str
    tags: list[str] = []
    description: str = ""


@app.post("/images/upload")
def upload_image(request: UploadRequest):
    upload_url, s3_key = generate_upload_url(request.content_type)

    metadata = save_image_metadata(
        user_id=request.user_id,
        s3_key=s3_key,
        tags=request.tags,
        description=request.description,
    )

    return {
        "upload_url": upload_url,
        "image_id": metadata["image_id"],
    }


# ✅ NEW: LIST IMAGES API
@app.get("/images")
def get_images(
    user_id: str | None = None,
    tag: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
):
    return list_images(
        user_id=user_id,
        tag=tag,
        start_date=start_date,
        end_date=end_date,
    )


@app.get("/images/{image_id}/download")
def download_image(image_id: str):
    image = get_image_by_id(image_id)

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    download_url = generate_download_url(image["s3_key"])

    return {
        "download_url": download_url
    }


@app.delete("/images/{image_id}")
def delete_image(image_id: str):
    image = get_image_by_id(image_id)

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    delete_image_from_s3(image["s3_key"])
    delete_image_metadata(image_id)

    return {
        "message": "Image deleted successfully"
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
def get_images(user_id: str | None = None):
    return list_images(user_id)


@app.get("/health")
def health_check():
    return {"status": "ok"}

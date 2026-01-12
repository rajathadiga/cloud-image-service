📸 Cloud Image Service

A backend service for uploading, listing, downloading, and deleting images using FastAPI, AWS S3 (Presigned URLs), and DynamoDB, with LocalStack for local AWS emulation.

This project demonstrates real-world cloud backend design, where large files are uploaded and downloaded directly via S3, keeping the backend stateless and scalable.

🚀 Features

Upload images using presigned S3 PUT URLs

Store image metadata in DynamoDB

List images with optional filtering by user_id

Download images using presigned S3 GET URLs

Delete images from S3 and DynamoDB

Fully documented APIs using Swagger UI

Local AWS environment using Docker + LocalStack

Clean, modular project structure

Incremental Git commits

🛠 Tech Stack

Backend Framework: FastAPI (Python)

Cloud Services: AWS S3, DynamoDB (via LocalStack)

AWS SDK: boto3

Infrastructure: Docker, Docker Compose

API Documentation: Swagger (OpenAPI)

Language: Python 3.11

📁 Project Structure
cloud-image-service/
├── src/
│   ├── main.py
│   ├── config.py
│   ├── utils/
│   │   ├── aws_resources.py
│   │   ├── s3_utils.py
│   │   └── init_resources.py
│   ├── db/
│   │   └── image_repository.py
├── docker-compose.yml
├── requirements.txt
└── README.md

⚙️ Setup Instructions
1️⃣ Prerequisites

Python 3.10+

Docker & Docker Desktop

Git

2️⃣ Clone the Repository
git clone <your-repository-url>
cd cloud-image-service

3️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows

4️⃣ Install Dependencies
pip install -r requirements.txt

5️⃣ Start Local AWS (LocalStack)
docker-compose up -d


Wait until logs show:

Ready.

6️⃣ Initialize AWS Resources
$env:PYTHONPATH="."
python -m src.utils.init_resources


This creates:

S3 bucket

DynamoDB table

7️⃣ Run the Application
$env:PYTHONPATH="."
uvicorn src.main:app --reload


Open Swagger UI:

http://127.0.0.1:8000/docs

🔌 API Walkthrough
1️⃣ Upload Image (Generate Presigned URL)

POST /images/upload

Request body:

{
  "user_id": "user123",
  "content_type": "image/jpeg",
  "tags": ["travel"],
  "description": "My first image"
}


Response:

{
  "upload_url": "http://localhost:4566/...",
  "image_id": "uuid"
}

2️⃣ Upload Image to S3 (Client → S3)
Invoke-WebRequest `
  -Uri "<upload_url>" `
  -Method PUT `
  -InFile "path/to/image.jpg" `
  -ContentType "image/jpeg"

3️⃣ List Images

GET /images

Optional filter:

/images?user_id=user123

4️⃣ Download Image

GET /images/{image_id}/download

Response:

{
  "download_url": "http://localhost:4566/..."
}

5️⃣ Delete Image

DELETE /images/{image_id}

Response:

{
  "message": "Image deleted successfully"
}

🧠 Design Decisions

Presigned URLs are used so large files never pass through the backend

DynamoDB stores only metadata for scalability

S3 handles all binary storage

Backend remains stateless and horizontally scalable

LocalStack enables full AWS simulation locally
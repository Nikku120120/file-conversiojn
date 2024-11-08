from fastapi import APIRouter, File, UploadFile
from app.services.image_service import process_image_service

router = APIRouter()

@router.post("/images/process")
async def process_image(
    file: UploadFile = None,
    output_format: str = "jpeg",
    download_bucket_name: str = None,
    download_s3_key: str = None,
    upload_bucket_name: str = None,
    upload_s3_key: str = None
):
    try:
        message = process_image_service(
            file=file,
            output_format=output_format,
            download_bucket_name=download_bucket_name,
            download_s3_key=download_s3_key,
            upload_bucket_name=upload_bucket_name,
            upload_s3_key=upload_s3_key
        )
        return {"message": message}
    except Exception as e:
        return {"error": str(e)}

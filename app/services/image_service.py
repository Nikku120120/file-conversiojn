from app.utils.image_utils import change_image_format
from app.utils.s3_utils import upload_to_s3, download_file_from_s3
from fastapi import UploadFile

def process_image_service(
    file: UploadFile,
    output_format: str,
    download_bucket_name: str,
    download_s3_key: str,
    upload_bucket_name: str,
    upload_s3_key: str
):
    # Step 1: Download image if no file is uploaded
    if file is None:
        if not download_bucket_name or not download_s3_key:
            raise ValueError("Must provide either a file upload or an S3 bucket and key for download.")
        image_stream = download_file_from_s3(download_bucket_name, download_s3_key)
    else:
        image_stream = file.file

    # Step 2: Convert image format
    converted_image = change_image_format(image_stream, output_format)

    # Step 3: Upload converted image to S3
    if not upload_bucket_name or not upload_s3_key:
        raise ValueError("Must provide S3 bucket and key for uploading processed image.")
    upload_to_s3(converted_image, upload_bucket_name, upload_s3_key, output_format)

    return "Image processed and uploaded successfully!"

import boto3
import io
from app.utils.secrets_manager_utils import fetch_secrets

def upload_to_s3(converted_image, bucket_name, s3_key, output_format):
    """Synchronously upload the converted image to an S3 bucket using credentials from Secrets Manager."""
    secret_name = "your-secret-name"  # The name of the secret in Secrets Manager
    secrets = fetch_secrets(secret_name)

    # Extract AWS credentials from the secret
    aws_access_key_id = secrets["AWS_ACCESS_KEY_ID"]
    aws_secret_access_key = secrets["AWS_SECRET_ACCESS_KEY"]
    aws_session_token = secrets.get("AWS_SESSION_TOKEN")  # Optional

    # Initialize the boto3 client
    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token  # Pass if available
    )
    
    content_type = f"image/{output_format.lower()}"
    try:
        s3.put_object(Bucket=bucket_name, Key=s3_key, Body=converted_image, ContentType=content_type)
    except Exception as e:
        raise Exception("Failed to upload to S3") from e

def download_file_from_s3(bucket_name: str, s3_key: str):
    """Synchronously download a file from S3 using credentials from Secrets Manager."""
    secret_name = "your-secret-name"  # The name of the secret in Secrets Manager
    secrets = fetch_secrets(secret_name)

    # Extract AWS credentials from the secret
    aws_access_key_id = secrets["AWS_ACCESS_KEY_ID"]
    aws_secret_access_key = secrets["AWS_SECRET_ACCESS_KEY"]
    aws_session_token = secrets.get("AWS_SESSION_TOKEN")  # Optional

    # Initialize the boto3 client
    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token  # Pass if available
    )
    
    file_stream = io.BytesIO()
    try:
        s3.download_fileobj(Bucket=bucket_name, Key=s3_key, Fileobj=file_stream)
        file_stream.seek(0)  # Reset the stream to the beginning
        return file_stream
    except Exception as e:
        raise Exception("Failed to download from S3") from e

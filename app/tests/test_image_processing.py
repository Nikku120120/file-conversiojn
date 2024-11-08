import pytest
from fastapi.testclient import TestClient
from moto import mock_s3
import boto3
from app.main import app

client = TestClient(app)

# Mock S3 setup
@pytest.fixture
def setup_s3():
    with mock_s3():
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket="test-bucket")
        yield s3

def test_process_image_with_upload_file(setup_s3):
    response = client.post(
        "/images/process",
        files={"file": ("test.png", open("tests/test_image.png", "rb"), "image/png")},
        data={
            "output_format": "jpeg",
            "upload_bucket_name": "test-bucket",
            "upload_s3_key": "processed-image.jpeg"
        }
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Image processed and uploaded successfully!"

def test_process_image_with_s3_download(setup_s3):
    # Upload a test image to S3 for downloading
    setup_s3.upload_file("tests/test_image.png", "test-bucket", "source-image.png")
    
    response = client.post(
        "/images/process",
        data={
            "output_format": "jpeg",
            "download_bucket_name": "test-bucket",
            "download_s3_key": "source-image.png",
            "upload_bucket_name": "test-bucket",
            "upload_s3_key": "processed-image.jpeg"
        }
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Image processed and uploaded successfully!"

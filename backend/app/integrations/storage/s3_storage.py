# s3_storage.py
import boto3
from botocore.exceptions import ClientError
from app.core.config import settings
from app.integrations.storage.base import StorageBackend
from loguru import logger

class S3Storage(StorageBackend):
    def __init__(self):
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY
        )
        self.bucket = settings.S3_BUCKET

    def save_file(self, relative_path: str, content: bytes) -> str:
        try:
            self.client.put_object(
                Bucket=self.bucket,
                Key=relative_path,
                Body=content
            )
            return relative_path
        except ClientError as e:
            logger.error(f"S3 save error: {e}")
            raise

    def delete_file(self, relative_path: str) -> None:
        try:
            self.client.delete_object(Bucket=self.bucket, Key=relative_path)
        except ClientError as e:
            logger.error(f"S3 delete error: {e}")

    def get_file_path(self, relative_path: str) -> str:
        # Для S3 возвращаем публичный URL (или префикс)
        if settings.S3_ENDPOINT_URL:
            return f"{settings.S3_ENDPOINT_URL}/{self.bucket}/{relative_path}"
        return f"https://{self.bucket}.s3.amazonaws.com/{relative_path}"
import boto3
from minio import Minio
from minio.error import S3Error
from typing import Optional, BinaryIO
import uuid
from app.config.settings import settings

class S3Helper:
    def __init__(self):
        if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
            self.bucket_name = settings.S3_BUCKET_NAME
            self.use_minio = False
        else:
            self.minio_client = Minio(
                settings.MINIO_ENDPOINT,
                access_key=settings.MINIO_ACCESS_KEY,
                secret_key=settings.MINIO_SECRET_KEY,
                secure=settings.MINIO_SECURE
            )
            self.bucket_name = settings.MINIO_BUCKET_NAME
            self.use_minio = True
            self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        """Ensure MinIO bucket exists"""
        try:
            if not self.minio_client.bucket_exists(self.bucket_name):
                self.minio_client.make_bucket(self.bucket_name)
        except S3Error as e:
            print(f"Error creating bucket: {e}")
    
    def upload_file(self, file_data: BinaryIO, file_name: str, content_type: str) -> str:
        """Upload file to S3/MinIO and return URL"""
        file_extension = file_name.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        
        if self.use_minio:
            try:
                self.minio_client.put_object(
                    self.bucket_name,
                    unique_filename,
                    file_data,
                    length=-1,
                    part_size=10*1024*1024,
                    content_type=content_type
                )
                return f"http://{settings.MINIO_ENDPOINT}/{self.bucket_name}/{unique_filename}"
            except S3Error as e:
                raise Exception(f"MinIO upload error: {e}")
        else:
            try:
                self.s3_client.put_object(
                    Bucket=self.bucket_name,
                    Key=unique_filename,
                    Body=file_data,
                    ContentType=content_type
                )
                return f"https://{self.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{unique_filename}"
            except Exception as e:
                raise Exception(f"S3 upload error: {e}")
    
    def delete_file(self, file_url: str) -> bool:
        """Delete file from S3/MinIO"""
        try:
            # Extract filename from URL
            filename = file_url.split('/')[-1]
            
            if self.use_minio:
                self.minio_client.remove_object(self.bucket_name, filename)
            else:
                self.s3_client.delete_object(Bucket=self.bucket_name, Key=filename)
            return True
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
    
    def get_presigned_url(self, file_name: str, expiration: int = 3600) -> str:
        """Generate presigned URL for file access"""
        if self.use_minio:
            return self.minio_client.presigned_get_object(self.bucket_name, file_name, expires=expiration)
        else:
            return self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': file_name},
                ExpiresIn=expiration
            )


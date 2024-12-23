"""
MinioPersistence implements IBlobPersistence
"""
from typing import Union, Dict, List
from minio import Minio
import os
from pydantic_settings import BaseSettings
from pydantic import Field
from tempfile import NamedTemporaryFile


class MinioSettings(BaseSettings):
    minio_endpoint: str = Field(..., env="MINIO_ENDPOINT")
    minio_access_key: str = Field(..., env="MINIO_ACCESS_KEY")
    minio_secret_key: str = Field(..., env="MINIO_SECRET_KEY")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"


class MinioPersistence:
    def __init__(self):
        self.settings: MinioSettings = MinioSettings()
        self.client = Minio(endpoint=self.settings.minio_endpoint, access_key=self.settings.minio_access_key,
                            secret_key=self.settings.minio_secret_key, secure=False)

    def createBucket(self: "MinioPersistence", name: str) -> None:
        if not self.client.bucket_exists(name):
            self.client.make_bucket(name)

    def uploadFile(self: "MinioPersistence", name: str, *, bucket: str, data, size, type, metadata: Dict[str, str] = None) -> None:
        """
        upload file, with the given name to the selected bucket
        """
        if self.client.bucket_exists(bucket):
            self.client.put_object(
                bucket_name=bucket,
                object_name=name,
                data=data,
                length=size,
                content_type=type,
                metadata=metadata or {}
            )

    def listObjects(self: "MinioPersistence", bucket: str) -> List[object]:
        """
        List all objects in a bucket
        """
        try:
            if not self.client.bucket_exists(bucket):
                return []

            objects = self.client.list_objects(bucket)
            return list(objects)
        except Exception as e:
            print(f"Error listing objects in bucket {bucket}: {str(e)}")
            return []

    def getObject(self, bucket: str, object_name: str) -> bytes:
        """
        Get an object from a bucket
        """
        try:
            response = self.client.get_object(bucket, object_name)
            return response.read()
        except Exception as e:
            print(
                f"Error getting object {object_name} from bucket {bucket}: {str(e)}")
            raise e

    def load_pdf_temporarily(self, bucket_name, file_name):
        pdf_data = self.getObject(bucket_name, file_name)
        print(pdf_data)
        temp_file = NamedTemporaryFile(delete=False, suffix=".pdf")
        temp_file_path = temp_file.name
        with open(temp_file_path, "wb") as f:
            f.write(pdf_data)
        print(
            f"PDF successfully loaded and saved temporarily at {temp_file_path}")
        return temp_file_path


minioClient: Union[None, MinioPersistence] = None if os.getenv(
    "ENV") != "development" else MinioPersistence()


def getMinioClient() -> MinioPersistence:
    global minioClient
    return minioClient

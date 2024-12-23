"""
MinioPersistence implements IBlobPersistence
"""
from typing import Union, Dict
from minio import Minio
import os
from pydantic_settings import BaseSettings
from pydantic import Field


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


minioClient: Union[None, MinioPersistence] = None if os.getenv(
    "ENV") != "development" else MinioPersistence()


def getMinioClient() -> MinioPersistence:
    global minioClient
    return minioClient

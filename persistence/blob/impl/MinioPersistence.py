"""
MinioPersistence implements IBlobPersistence
"""
from typing import Union
from minio import Minio
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
    _instance = None

    def __init__(self):
        if MinioPersistence._instance is not None:
            raise Exception("MinioPersistence is a singleton!")
        
        self.settings: MinioSettings = MinioSettings()
        self.client = Minio(
            endpoint=self.settings.minio_endpoint,
            access_key=self.settings.minio_access_key,
            secret_key=self.settings.minio_secret_key,
            secure=False
        )
        MinioPersistence._instance = self

    @staticmethod
    def get_instance():
        if MinioPersistence._instance is None:
            MinioPersistence()
        return MinioPersistence._instance

    def createBucket(self, name: str) -> None:
        if not self.client.bucket_exists(name):
            self.client.make_bucket(name)

    def uploadFile(self, name: str, *, bucket: str, data, size, type, metadata: dict[str, str] = None) -> None:
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

    def listObjects(self, bucket: str) -> list[object]:
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
            print(f"Error getting object {object_name} from bucket {bucket}: {str(e)}")
            raise e

def getMinioClient() -> MinioPersistence:
    return MinioPersistence.get_instance()
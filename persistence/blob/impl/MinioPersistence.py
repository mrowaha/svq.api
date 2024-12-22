"""
MinioPersistence implements IBlobPersistence
"""
from typing import Union, Dict
from minio import Minio
import os

class MinioPersistence:
    def __init__(self, *, endpoint: str, accesskey: str, secretkey: str):
        print(endpoint)
        print(accesskey)
        print(secretkey)
        self.client = Minio(endpoint, access_key=accesskey,
                            secret_key=secretkey, secure=False)

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

minioClient: Union[None, MinioPersistence] = None

def getMinioClient() -> MinioPersistence:
    global minioClient
    if os.getenv("ENV") == "development":
        if minioClient is None:
            endpoint = "localhost:9000" if os.getenv(
                "MINIO_ENDPOINT") is None else os.getenv("MINIO_ENDPOINT")
            accessKey = "admin" if os.getenv(
                "MINIO_ACCESS_KEY") is None else os.getenv("MINIO_ACCESS_KEY")
            secretKey = "password" if os.getenv(
                "MINIO_SECRET_KEY") is None else os.getenv("MINIO_SECRET_KEY")
            minioClient = MinioPersistence(
                endpoint=endpoint,
                accesskey=accessKey,
                secretkey=secretKey
            )
    return minioClient

"""
MinioPersistence implements IBlobPersistence
"""
import os
from minio import Minio
from typing import Union


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


minioClient: Union[None, MinioPersistence] = None


def getMinioClient() -> MinioPersistence:
    global minioClient
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

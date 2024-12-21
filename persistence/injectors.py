import os
from fastapi import Depends
from .blob import IBlobPersistence
from .blob.impl.MinioPersistence import getMinioClient, MinioPersistence


def getBlobStorage(minio: MinioPersistence = Depends(getMinioClient)) -> IBlobPersistence:

    if os.getenv("ENV") == "development":
        return minio

    raise "ENV should be defined"

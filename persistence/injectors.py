import os
from fastapi import Depends
from .blob import IBlobPersistence
from .blob.impl.MinioPersistence import getMinioClient, MinioPersistence
from .access import IAccessManagement
from .access.impl.KeyCloakAccessManagement import getKeyCloakClient, KeyCloakAccessManagement


def getBlobStorage(minio: MinioPersistence = Depends(getMinioClient)) -> IBlobPersistence:

    if os.getenv("ENV") == "development":
        return minio

    raise "ENV should be defined"


def getAccessManagement(keycloak: KeyCloakAccessManagement = Depends(getKeyCloakClient)) -> IAccessManagement:
    return keycloak

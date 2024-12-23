from typing import Protocol, Dict, List
import io


class IBlobPersistence(Protocol):
    def createBucket(name: str) -> None:
        """
        :name bucket to be created with this name
        """
        ...

    def uploadFile(name: str, *, bucket: str, data: io.BytesIO, size: int, type: str, metadata: Dict[str, str] = None) -> None:
        """
        upload file, with the given name to the selected bucket
        """
        ...

    def listObjects(bucket: str) -> List[object]:
        """
        List all objects in a bucket
        :param bucket: Name of the bucket
        :return: List of objects with their metadata
        """
        ...

    def getObject(bucket: str, object_name: str) -> bytes:
        """
        Get an object from a bucket
        :param bucket: Name of the bucket
        :param object_name: Name of the object
        :return: Object data as bytes
        """
        ...

    def load_pdf_temporarily(bucket_name, file_name) -> str:
        ...

from typing import Protocol, Dict
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

from typing import Protocol
import io


class IBlobPersistence(Protocol):
    def createBucket(name: str) -> None:
        """
        :name bucket to be created with this name
        """
        ...

    def uploadFile(name: str, *, bucket: str, data: io.BytesIO, size: int, type: str) -> None:
        """
        upload file, with the given name to the selected bucket
        """
        ...

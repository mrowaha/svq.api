from typing import Protocol


class IBlobPersistence(Protocol):
    def createBucket(name: str) -> None:
        """
        :name bucket to be created with this name
        """
        pass

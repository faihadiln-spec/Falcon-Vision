from abc import ABC, abstractmethod

from app.models.regulation_model import StoredFile


class StorageClient(ABC):
    @abstractmethod
    async def save_bytes(
        self,
        *,
        content: bytes,
        original_filename: str,
        mime_type: str,
        subdirectory: str,
    ) -> StoredFile:
        raise NotImplementedError

    @abstractmethod
    async def read_bytes(self, storage_path: str) -> bytes:
        raise NotImplementedError

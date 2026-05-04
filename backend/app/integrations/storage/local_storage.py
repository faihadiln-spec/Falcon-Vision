import hashlib
from pathlib import Path
from uuid import uuid4

from app.integrations.storage.storage_client import StorageClient
from app.models.regulation_model import StoredFile


class LocalStorageClient(StorageClient):
    def __init__(self, base_dir: Path) -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    async def save_bytes(
        self,
        *,
        content: bytes,
        original_filename: str,
        mime_type: str,
        subdirectory: str,
    ) -> StoredFile:
        extension = Path(original_filename).suffix.lower()
        relative_dir = self.base_dir / subdirectory
        relative_dir.mkdir(parents=True, exist_ok=True)

        filename = f"{uuid4().hex}{extension}"
        storage_path = relative_dir / filename
        storage_path.write_bytes(content)

        return StoredFile(
            original_filename=original_filename,
            storage_provider="local",
            storage_path=storage_path.as_posix(),
            mime_type=mime_type,
            size_bytes=len(content),
            sha256=hashlib.sha256(content).hexdigest(),
        )

    async def read_bytes(self, storage_path: str) -> bytes:
        return Path(storage_path).read_bytes()

    async def delete_bytes(self, storage_path: str) -> None:
        if not storage_path:
            return

        try:
            file_path = Path(storage_path)
            if file_path.exists():
                file_path.unlink()
        except OSError:
            return

    def get_access_url(self, storage_path: str | None) -> str | None:
        if not storage_path:
            return None

        return Path(storage_path).as_posix()

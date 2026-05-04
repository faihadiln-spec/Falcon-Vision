import asyncio
import hashlib
from datetime import datetime, timedelta, timezone
from pathlib import Path, PurePosixPath
from uuid import uuid4

from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from azure.storage.blob import BlobSasPermissions, BlobServiceClient, ContentSettings, generate_blob_sas

from app.integrations.storage.storage_client import StorageClient
from app.models.regulation_model import StoredFile


class AzureBlobStorageClient(StorageClient):
    def __init__(
        self,
        connection_string: str,
        container_name: str,
        *,
        url_expiry_minutes: int = 60,
    ) -> None:
        self.connection_string = connection_string
        self.container_name = container_name
        self.url_expiry_minutes = url_expiry_minutes
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_client = self.blob_service_client.get_container_client(container_name)
        self._container_ready = False
        self._container_lock = asyncio.Lock()

        connection_parts = self._parse_connection_string(connection_string)
        self.account_name = connection_parts.get("AccountName", "")
        self.account_key = connection_parts.get("AccountKey", "")

    async def save_bytes(
        self,
        *,
        content: bytes,
        original_filename: str,
        mime_type: str,
        subdirectory: str,
    ) -> StoredFile:
        await self._ensure_container()

        extension = Path(original_filename).suffix.lower()
        filename = f"{uuid4().hex}{extension}"
        blob_name = str(PurePosixPath(subdirectory) / filename)

        await asyncio.to_thread(
            self._upload_blob,
            blob_name,
            content,
            mime_type,
        )

        return StoredFile(
            original_filename=original_filename,
            storage_provider="azure_blob",
            storage_path=blob_name,
            mime_type=mime_type,
            size_bytes=len(content),
            sha256=hashlib.sha256(content).hexdigest(),
        )

    async def read_bytes(self, storage_path: str) -> bytes:
        try:
            return await asyncio.to_thread(self._download_blob, storage_path)
        except ResourceNotFoundError as exc:
            raise OSError(f"Stored blob not found: {storage_path}") from exc

    async def delete_bytes(self, storage_path: str) -> None:
        if not storage_path:
            return

        try:
            await asyncio.to_thread(
                self.container_client.delete_blob,
                storage_path,
                delete_snapshots="include",
            )
        except ResourceNotFoundError:
            return

    def get_access_url(self, storage_path: str | None) -> str | None:
        if not storage_path:
            return None

        blob_client = self.container_client.get_blob_client(storage_path)
        base_url = blob_client.url

        if not self.account_name or not self.account_key:
            return base_url

        expires_at = datetime.now(timezone.utc) + timedelta(minutes=self.url_expiry_minutes)
        sas_token = generate_blob_sas(
            account_name=self.account_name,
            container_name=self.container_name,
            blob_name=storage_path,
            account_key=self.account_key,
            permission=BlobSasPermissions(read=True),
            expiry=expires_at,
        )
        return f"{base_url}?{sas_token}"

    async def _ensure_container(self) -> None:
        if self._container_ready:
            return

        async with self._container_lock:
            if self._container_ready:
                return

            try:
                await asyncio.to_thread(self.container_client.create_container)
            except ResourceExistsError:
                pass

            self._container_ready = True

    def _upload_blob(self, blob_name: str, content: bytes, mime_type: str) -> None:
        blob_client = self.container_client.get_blob_client(blob_name)
        blob_client.upload_blob(
            content,
            overwrite=True,
            content_settings=ContentSettings(content_type=mime_type),
        )

    def _download_blob(self, storage_path: str) -> bytes:
        blob_client = self.container_client.get_blob_client(storage_path)
        return blob_client.download_blob().readall()

    @staticmethod
    def _parse_connection_string(connection_string: str) -> dict[str, str]:
        parts: dict[str, str] = {}
        for part in connection_string.split(";"):
            if "=" not in part:
                continue
            key, value = part.split("=", 1)
            parts[key] = value
        return parts

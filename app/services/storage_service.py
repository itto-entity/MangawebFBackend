from __future__ import annotations

from typing import Optional

from supabase import Client

from app.core.config import settings
from app.core.supabase import supabase_admin


class StorageService:
    def __init__(self, client: Client = supabase_admin, bucket_name: str = settings.storage_bucket):
        self.client = client
        self.bucket_name = bucket_name

    def create_signed_url(self, object_path: str, expires_in: Optional[int] = None) -> str:
        ttl = expires_in or settings.storage_signed_url_expires_in
        response = self.client.storage.from_(self.bucket_name).create_signed_url(object_path, ttl)

        data = getattr(response, "data", response)
        if isinstance(data, dict):
            signed_url = data.get("signedUrl") or data.get("signed_url")
        else:
            signed_url = getattr(data, "signedUrl", None) or getattr(data, "signed_url", None)

        if not signed_url:
            error = getattr(response, "error", None)
            raise RuntimeError(error or "Failed to create signed URL")

        return signed_url

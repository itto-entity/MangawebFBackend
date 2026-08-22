from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BookmarkBase(BaseModel):
    manga_id: UUID
    last_chapter_id: Optional[UUID] = None


class BookmarkCreate(BookmarkBase):
    pass


class BookmarkUpdate(BaseModel):
    last_chapter_id: UUID


class BookmarkResponse(BookmarkBase):
    id: UUID
    user_id: UUID
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BookmarkDetailResponse(BookmarkResponse):
    manga_slug: Optional[str] = None
    manga_title: Optional[str] = None
    cover_image_url: Optional[str] = None
    last_chapter_number: Optional[Decimal] = None


class BookmarkListResponse(BaseModel):
    total: int
    items: List[BookmarkDetailResponse]

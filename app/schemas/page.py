from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ChapterPageBase(BaseModel):
    page_number: int = Field(..., ge=1, description="Page number within the chapter")
    image_path: str = Field(..., description="Path in Supabase Storage")


class ChapterPageCreate(ChapterPageBase):
    chapter_id: UUID


class ChapterPageResponse(ChapterPageBase):
    id: UUID
    chapter_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChapterPageSignedUrl(BaseModel):
    page_number: int
    signed_url: str
    expires_at: Optional[datetime] = None


class ChapterPagesResponse(BaseModel):
    chapter_id: UUID
    manga_id: Optional[UUID] = None
    pages: List[ChapterPageSignedUrl]

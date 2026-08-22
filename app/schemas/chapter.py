from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ChapterBase(BaseModel):
    chapter_number: Decimal = Field(..., description="Chapter number, e.g. 1 or 1.5")
    title: Optional[str] = Field(None, max_length=255, description="Chapter title")


class ChapterCreate(ChapterBase):
    manga_id: UUID


class ChapterUpdate(BaseModel):
    chapter_number: Optional[Decimal] = None
    title: Optional[str] = None


class ChapterResponse(ChapterBase):
    id: UUID
    manga_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChapterListResponse(BaseModel):
    total: int
    items: List[ChapterResponse]

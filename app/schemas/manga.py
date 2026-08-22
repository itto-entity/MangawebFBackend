from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class MangaBase(BaseModel):
    slug: str = Field(..., min_length=1, max_length=255, description="Unique URL slug")
    title: str = Field(..., min_length=1, max_length=255, description="Manga title")
    creator: Optional[str] = Field(None, max_length=255, description="Author / Artist")
    genre: Optional[List[str]] = Field(default_factory=list, description="List of genres")
    description: Optional[str] = Field(None, description="Synopsis / description")
    cover_image_url: Optional[str] = Field(None, description="URL/path to cover image")
    is_published: bool = True


class MangaCreate(MangaBase):
    pass


class MangaUpdate(BaseModel):
    slug: Optional[str] = Field(None, min_length=1, max_length=255)
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    creator: Optional[str] = None
    genre: Optional[List[str]] = None
    description: Optional[str] = None
    cover_image_url: Optional[str] = None
    is_published: Optional[bool] = None


class MangaResponse(MangaBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MangaListResponse(BaseModel):
    total: int
    items: List[MangaResponse]

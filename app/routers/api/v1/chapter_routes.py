from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.connection_db import get_db
from app.repository.catalog_repo import ChapterPageRepository, ChapterRepository
from app.schemas.page import ChapterPageCreate, ChapterPageResponse, ChapterPagesResponse, ChapterPageSignedUrl
from app.services.storage_service import StorageService

router = APIRouter(prefix="/api/v1/chapters", tags=["Chapters"])


def get_chapter_repo(db: Session = Depends(get_db)) -> ChapterRepository:
    return ChapterRepository(db)


def get_page_repo(db: Session = Depends(get_db)) -> ChapterPageRepository:
    return ChapterPageRepository(db)


def get_storage_service() -> StorageService:
    return StorageService()


@router.get("/{chapter_id}/pages", response_model=ChapterPagesResponse)
def list_chapter_pages(
    chapter_id: UUID,
    chapter_repo: ChapterRepository = Depends(get_chapter_repo),
    page_repo: ChapterPageRepository = Depends(get_page_repo),
    storage_service: StorageService = Depends(get_storage_service),
):
    chapter = chapter_repo.get_by_id(chapter_id)
    if not chapter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chapter not found")

    pages = page_repo.list_by_chapter_id(chapter_id)
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=settings.storage_signed_url_expires_in)
    response_pages = []

    for page in pages:
        if page.image_path.startswith("http://") or page.image_path.startswith("https://"):
            signed_url = page.image_path
        else:
            signed_url = storage_service.create_signed_url(page.image_path)

        response_pages.append(
            ChapterPageSignedUrl(
                page_number=page.page_number,
                signed_url=signed_url,
                expires_at=expires_at,
            )
        )

    return ChapterPagesResponse(
        chapter_id=chapter.id,
        manga_id=chapter.manga_id,
        pages=response_pages,
    )


@router.post("/{chapter_id}/pages", response_model=ChapterPageResponse, status_code=status.HTTP_201_CREATED)
def create_chapter_page(
    chapter_id: UUID,
    payload: ChapterPageCreate,
    chapter_repo: ChapterRepository = Depends(get_chapter_repo),
    page_repo: ChapterPageRepository = Depends(get_page_repo),
):
    chapter = chapter_repo.get_by_id(chapter_id)
    if not chapter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chapter not found")

    if payload.chapter_id != chapter_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="chapter_id in body must match chapter_id in path",
        )

    return page_repo.create(payload.model_dump())

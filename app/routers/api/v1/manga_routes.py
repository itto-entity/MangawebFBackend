from __future__ import annotations

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.connection_db import get_db
from app.repository.catalog_repo import ChapterRepository, MangaRepository
from app.schemas.chapter import ChapterCreate, ChapterListResponse, ChapterResponse, ChapterUpdate
from app.schemas.manga import MangaCreate, MangaListResponse, MangaResponse, MangaUpdate

router = APIRouter(prefix="/api/v1/mangas", tags=["Mangas"])


def get_manga_repo(db: Session = Depends(get_db)) -> MangaRepository:
    return MangaRepository(db)


def get_chapter_repo(db: Session = Depends(get_db)) -> ChapterRepository:
    return ChapterRepository(db)


@router.get("", response_model=MangaListResponse)
def list_mangas(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None, min_length=1),
    repo: MangaRepository = Depends(get_manga_repo),
):
    return repo.list_mangas(skip=skip, limit=limit, search=search)


@router.post("", response_model=MangaResponse, status_code=status.HTTP_201_CREATED)
def create_manga(
    payload: MangaCreate,
    repo: MangaRepository = Depends(get_manga_repo),
):
    return repo.create(payload.model_dump())


@router.get("/{slug}", response_model=MangaResponse)
def get_manga(
    slug: str,
    repo: MangaRepository = Depends(get_manga_repo),
):
    manga = repo.get_by_slug(slug)
    if not manga:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Manga not found")
    return manga


@router.patch("/{manga_id}", response_model=MangaResponse)
def update_manga(
    manga_id: UUID,
    payload: MangaUpdate,
    repo: MangaRepository = Depends(get_manga_repo),
):
    manga = repo.get_by_id(manga_id)
    if not manga:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Manga not found")
    return repo.update(manga, payload.model_dump(exclude_unset=True))


@router.delete("/{manga_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_manga(
    manga_id: UUID,
    repo: MangaRepository = Depends(get_manga_repo),
):
    manga = repo.get_by_id(manga_id)
    if not manga:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Manga not found")
    repo.delete(manga)


@router.get("/{slug}/chapters", response_model=ChapterListResponse)
def list_manga_chapters(
    slug: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    manga_repo: MangaRepository = Depends(get_manga_repo),
    chapter_repo: ChapterRepository = Depends(get_chapter_repo),
):
    manga = manga_repo.get_by_slug(slug)
    if not manga:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Manga not found")
    return chapter_repo.list_by_manga_id(manga.id, skip=skip, limit=limit)


@router.post("/{manga_id}/chapters", response_model=ChapterResponse, status_code=status.HTTP_201_CREATED)
def create_chapter(
    manga_id: UUID,
    payload: ChapterCreate,
    manga_repo: MangaRepository = Depends(get_manga_repo),
    chapter_repo: ChapterRepository = Depends(get_chapter_repo),
):
    manga = manga_repo.get_by_id(manga_id)
    if not manga:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Manga not found")
    if payload.manga_id != manga_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="manga_id in body must match manga_id in path",
        )

    chapter_data = payload.model_dump(exclude={"manga_id"})
    chapter_data["manga_id"] = manga_id
    return chapter_repo.create(chapter_data)


@router.patch("/chapters/{chapter_id}", response_model=ChapterResponse)
def update_chapter(
    chapter_id: UUID,
    payload: ChapterUpdate,
    chapter_repo: ChapterRepository = Depends(get_chapter_repo),
):
    chapter = chapter_repo.get_by_id(chapter_id)
    if not chapter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chapter not found")
    return chapter_repo.update(chapter, payload.model_dump(exclude_unset=True))


@router.delete("/chapters/{chapter_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chapter(
    chapter_id: UUID,
    chapter_repo: ChapterRepository = Depends(get_chapter_repo),
):
    chapter = chapter_repo.get_by_id(chapter_id)
    if not chapter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chapter not found")
    chapter_repo.delete(chapter)

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID

from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import Session

from app.db.models import Chapter, ChapterPage, Manga


class MangaRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_mangas(self, skip: int = 0, limit: int = 20, search: Optional[str] = None) -> Dict[str, Any]:
        stmt = select(Manga)
        count_stmt = select(func.count()).select_from(Manga)

        if search:
            pattern = f"%{search.strip()}%"
            filters = or_(
                Manga.slug.ilike(pattern),
                Manga.title.ilike(pattern),
                Manga.creator.ilike(pattern),
                Manga.description.ilike(pattern),
            )
            stmt = stmt.where(filters)
            count_stmt = count_stmt.where(filters)

        total = self.db.execute(count_stmt).scalar_one()
        items = (
            self.db.execute(
                stmt.order_by(Manga.created_at.desc()).offset(skip).limit(limit)
            )
            .scalars()
            .all()
        )

        return {"total": total, "items": items}

    def get_by_id(self, manga_id: UUID) -> Optional[Manga]:
        return self.db.get(Manga, manga_id)

    def get_by_slug(self, slug: str) -> Optional[Manga]:
        stmt = select(Manga).where(Manga.slug == slug)
        return self.db.execute(stmt).scalar_one_or_none()

    def create(self, payload: Dict[str, Any]) -> Manga:
        manga = Manga(**payload)
        self.db.add(manga)
        self.db.commit()
        self.db.refresh(manga)
        return manga

    def update(self, manga: Manga, payload: Dict[str, Any]) -> Manga:
        for key, value in payload.items():
            if value is not None:
                setattr(manga, key, value)
        manga.updated_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(manga)
        return manga

    def delete(self, manga: Manga) -> None:
        self.db.delete(manga)
        self.db.commit()


class ChapterRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_by_manga_id(self, manga_id: UUID, skip: int = 0, limit: int = 50) -> Dict[str, Any]:
        stmt = select(Chapter).where(Chapter.manga_id == manga_id)
        count_stmt = select(func.count()).select_from(Chapter).where(Chapter.manga_id == manga_id)
        total = self.db.execute(count_stmt).scalar_one()
        items = (
            self.db.execute(
                stmt.order_by(Chapter.chapter_number.asc(), Chapter.created_at.asc())
                .offset(skip)
                .limit(limit)
            )
            .scalars()
            .all()
        )
        return {"total": total, "items": items}

    def get_by_id(self, chapter_id: UUID) -> Optional[Chapter]:
        return self.db.get(Chapter, chapter_id)

    def create(self, payload: Dict[str, Any]) -> Chapter:
        chapter = Chapter(**payload)
        self.db.add(chapter)
        self.db.commit()
        self.db.refresh(chapter)
        return chapter

    def update(self, chapter: Chapter, payload: Dict[str, Any]) -> Chapter:
        for key, value in payload.items():
            if value is not None:
                setattr(chapter, key, value)
        self.db.commit()
        self.db.refresh(chapter)
        return chapter

    def delete(self, chapter: Chapter) -> None:
        self.db.delete(chapter)
        self.db.commit()


class ChapterPageRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_by_chapter_id(self, chapter_id: UUID) -> List[ChapterPage]:
        stmt = (
            select(ChapterPage)
            .where(ChapterPage.chapter_id == chapter_id)
            .order_by(ChapterPage.page_number.asc())
        )
        return self.db.execute(stmt).scalars().all()

    def create(self, payload: Dict[str, Any]) -> ChapterPage:
        page = ChapterPage(**payload)
        self.db.add(page)
        self.db.commit()
        self.db.refresh(page)
        return page

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Table,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import ARRAY, UUID

from app.db.connection_db import Base


UTC_NOW = text("timezone('utc'::text, now())")
UUID_DEFAULT = text("gen_random_uuid()")


auth_users = Table(
    "users",
    Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    schema="auth",
    # Managed by Supabase Auth, not by this application's migrations.
    info={"skip_autogenerate": True},
)


class Profile(Base):
    __tablename__ = "profiles"
    __table_args__ = (CheckConstraint("role IN ('admin', 'vip', 'member')"),)

    id = Column(UUID(as_uuid=True), ForeignKey("auth.users.id", ondelete="CASCADE"), primary_key=True)
    username = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False, server_default=text("'member'"))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=UTC_NOW)


class Manga(Base):
    __tablename__ = "mangas"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=UUID_DEFAULT)
    slug = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    creator = Column(String)
    genre = Column(ARRAY(String))
    description = Column(String)
    cover_image_url = Column(String)
    is_published = Column(Boolean, server_default=text("true"))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=UTC_NOW)
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=UTC_NOW)


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=UUID_DEFAULT)
    manga_id = Column(UUID(as_uuid=True), ForeignKey("mangas.id", ondelete="CASCADE"), nullable=False)
    chapter_number = Column(Numeric, nullable=False)
    title = Column(String)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=UTC_NOW)


class ChapterPage(Base):
    __tablename__ = "chapter_pages"
    __table_args__ = (UniqueConstraint("chapter_id", "page_number"),)

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=UUID_DEFAULT)
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False)
    page_number = Column(Integer, nullable=False)
    image_path = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=UTC_NOW)


class UserBookmark(Base):
    __tablename__ = "user_bookmarks"
    __table_args__ = (UniqueConstraint("user_id", "manga_id"),)

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=UUID_DEFAULT)
    user_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    manga_id = Column(UUID(as_uuid=True), ForeignKey("mangas.id", ondelete="CASCADE"), nullable=False)
    last_chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id"))
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=UTC_NOW)

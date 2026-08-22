from app.schemas.auth import (
    ProfileBase,
    ProfileCreate,
    ProfileResponse,
    ProfileUpdate,
    TokenResponse,
    UserDetailResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserRole,
)
from app.schemas.bookmark import (
    BookmarkBase,
    BookmarkCreate,
    BookmarkDetailResponse,
    BookmarkListResponse,
    BookmarkResponse,
    BookmarkUpdate,
)
from app.schemas.chapter import (
    ChapterBase,
    ChapterCreate,
    ChapterListResponse,
    ChapterResponse,
    ChapterUpdate,
)
from app.schemas.manga import (
    MangaBase,
    MangaCreate,
    MangaListResponse,
    MangaResponse,
    MangaUpdate,
)
from app.schemas.page import (
    ChapterPageBase,
    ChapterPageCreate,
    ChapterPageResponse,
    ChapterPagesResponse,
    ChapterPageSignedUrl,
)

__all__ = [
    # Auth & Profile
    "UserRole",
    "UserRegisterRequest",
    "UserLoginRequest",
    "TokenResponse",
    "ProfileBase",
    "ProfileCreate",
    "ProfileUpdate",
    "ProfileResponse",
    "UserDetailResponse",
    # Manga
    "MangaBase",
    "MangaCreate",
    "MangaUpdate",
    "MangaResponse",
    "MangaListResponse",
    # Chapter
    "ChapterBase",
    "ChapterCreate",
    "ChapterUpdate",
    "ChapterResponse",
    "ChapterListResponse",
    # Chapter Page
    "ChapterPageBase",
    "ChapterPageCreate",
    "ChapterPageResponse",
    "ChapterPageSignedUrl",
    "ChapterPagesResponse",
    # Bookmark
    "BookmarkBase",
    "BookmarkCreate",
    "BookmarkUpdate",
    "BookmarkResponse",
    "BookmarkDetailResponse",
    "BookmarkListResponse",
]

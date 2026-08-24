# Manga asset migration CLI

`scripts.migrate_assets` uploads local images to the private `manga-assets` bucket. The category is mandatory and always becomes the first segment of every Storage object path:

```text
<category>/<optional-prefix>/<original-relative-folder>/<image-file>
```

For example, this source structure:

```text
E:\manga\one-piece\chapter-001\page-001.jpg
```

with category `action` and prefix `originals` becomes:

```text
action/originals/one-piece/chapter-001/page-001.jpg
```

Preview first (this does not call Supabase):

```powershell
.\.venv\Scripts\python.exe -m scripts.migrate_assets E:\manga --category action --prefix originals --manifest .\migration-manifest.json
```

Upload after confirming the preview. The CLI reads `SUPABASE_URL` and `SUPABASE_ROLE_KEY` from `.env`; keep the service-role key private.

```powershell
.\.venv\Scripts\python.exe -m scripts.migrate_assets E:\manga --category action --prefix originals --manifest .\migration-manifest.json --execute
```

Existing objects are protected by default. Add `--upsert` only when intentionally replacing files. Supported formats: AVIF, GIF, JPEG, PNG, and WebP.

## Import manga, chapters, and pages together

Use `scripts.import_manga` when the source folder has one child folder per chapter. It calls the backend API to create (or reuse) the manga, link each chapter through `manga_id`, and link every uploaded image through `chapter_id`.

```text
images/one-piece/
├── chapter-001/
│   ├── page-001.jpg
│   └── page-002.jpg
└── chapter-002/
    └── page-001.jpg
```

Preview the inferred import:

```powershell
.\.venv\Scripts\python.exe -m scripts.import_manga .\images\one-piece --slug one-piece --title "One Piece" --category action --genre action
```

Run the import after FastAPI is running at `http://localhost:8000`:

```powershell
.\.venv\Scripts\python.exe -m scripts.import_manga .\images\one-piece --slug one-piece --title "One Piece" --category action --genre action --execute
```

The example creates `action/one-piece/chapter-001/page-001.jpg` in Storage, then creates matching `mangas`, `chapters`, and `chapter_pages` records through `/api/v1/mangas` and `/api/v1/chapters`. Existing manga slugs, chapter numbers, and page numbers are skipped. If an earlier run uploaded a file but stopped before its database record was created, rerun with `--upsert`.

from fastapi import FastAPI, Request
import time
import logging
from app.routers.api.v1 import auth_routes as auth
from app.routers.api.v1 import chapter_routes as chapters
from app.routers.api.v1 import manga_routes as mangas
app = FastAPI(description="Ini adalah backend server dari mangaweb")
app.include_router(auth.router)
app.include_router(mangas.router)
app.include_router(chapters.router)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("http_logger")

@app.middleware("http")
async def log(request: Request, call_next):
    start_time = time.perf_counter()
    client_ip = request.client.host if request.client else "Unknown"
    logger.info("Incoming: %s | %s | IP: %s", request.method, request.url.path, client_ip)

    response = None
    try:
        response = await call_next(request)
    except Exception:
        logger.exception("Failed: %s | %s", request.method, request.url.path)
        raise
    finally:
        process_time = (time.perf_counter() - start_time) * 1000
        if response is not None:
            response.headers["X-Process-Time"] = f"{process_time:.2f}"
    return response


@app.get("/")
def read_root():
    return {"Server" : "Active"}

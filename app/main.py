"""AIKIVAVIORA FastAPI entry point."""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

try:
    from .routes.analytics import router as analytics_router
    from .routes.chat import router as chat_router
    from .routes.system import router as system_router
    from .routes.web import router as web_router
except ImportError:
    from routes.analytics import router as analytics_router
    from routes.chat import router as chat_router
    from routes.system import router as system_router
    from routes.web import router as web_router

# ============================================
# FASTAPI APP
# ============================================
app = FastAPI(title="AIKIVAVIORA Core Analytics MVP", version="0.3")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.include_router(web_router)
app.include_router(system_router)
app.include_router(chat_router)
app.include_router(analytics_router)

# ============================================
# RUN
# ============================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
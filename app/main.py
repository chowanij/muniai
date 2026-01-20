"""
Główna aplikacja FastAPI.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.database import close_db, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup i shutdown aplikacji."""
    # STARTUP
    print(f"🚀 Starting {settings.app_name}")
    print(f"📍 Environment: {settings.environment}")
    
    if settings.environment == "development":
        await init_db()
        print("📦 Database tables created")
    
    yield  # Aplikacja działa
    
    # SHUTDOWN
    print("🛑 Shutting down...")
    await close_db()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="RAG System dla gospodarki odpadami - Gmina Nowy Targ",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.debug else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
    }


@app.get("/health")
async def health():
    return {"status": "ok"}
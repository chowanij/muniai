"""
Health API endpoints
"""

import time
import redis
from typing import Annotated

from sqlalchemy import text
from fastapi import APIRouter, Depends

from app.db.database import async_session_factory
from app.core.config import  Settings

router = APIRouter(tags=["health"])

def get_settings() -> Settings:
    return Settings()


@router.get("/")
async def health():
    """Health check"""
    return {"status": "ok"}

@router.get("/ready")
async def readiness(settings: Annotated[Settings, Depends(get_settings)]):
    """Readiness check"""
    checks = {}
    try:
        start = time.perf_counter()
        async with async_session_factory() as session:
            await session.execute(text("SELECT 1"))
        latency = (time.perf_counter() - start) * 1000 #latency in ms
    except Exception as e:
        checks["database"] = {"status": "error", "message": str(e)}
    else:
        checks["database"] = {"status": "ok", "latency_ms": round(latency, 2)}

    try:
        start = time.perf_counter()
        redis_client = redis.Redis.from_url(settings.redis_url)
        re = redis_client.ping()
        latency = (time.perf_counter() - start) * 1000  # latency in ms
    except Exception as e:
        checks["redis"] = {"status": "error", "message": str(e)}
    else:
        checks["redis"] = {"status": f"is redis ok: {re}", "latency_ms": round(latency, 2)}

    overall = "platform status: ok" if all([c["status"] == "ok" for c in checks.values()]) else "platform status: error"

    return {"status": overall, "checks": checks}
from datetime import datetime
from typing import Literal

from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get("/health", summary="Health check", tags=["health"])  # Mounted under /api/v1
async def health_check() -> dict[str, str | int | float | Literal["ok"]]:
    """
    Lightweight service health endpoint.
    Returns basic info for uptime checks and simple diagnostics.
    """
    now = datetime.utcnow().isoformat() + "Z"
    return {
        "status": "ok",
        "service": settings.PROJECT_NAME,
        "version": settings.API_V1_STR,
        "time": now,
    }

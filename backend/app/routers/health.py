from datetime import datetime, timezone
from fastapi import APIRouter
from app.config import settings
from app.models.schemas import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(version=settings.version, timestamp=datetime.now(timezone.utc).isoformat())

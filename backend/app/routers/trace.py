"""AI pipeline trace panel backend (Issue #10). Stub until real call logging lands."""
from fastapi import APIRouter
from app.models.schemas import TraceInfo

router = APIRouter()


@router.get("/api/trace/{request_id}", response_model=TraceInfo)
def get_trace(request_id: str) -> TraceInfo:
    return TraceInfo(cnn_confidence=None, routed_to_gemini=False, cache_hit=False)

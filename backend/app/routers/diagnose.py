"""Module A stub. Real CNN + Gemini confidence-gated fallback lands in Issues #2-4."""
import uuid
from fastapi import APIRouter, File, Form, UploadFile
from app.models.schemas import DiagnoseResponse, TraceInfo

router = APIRouter()


@router.post("/api/diagnose", response_model=DiagnoseResponse)
async def diagnose(
    image: UploadFile = File(...),
    district_code: str = Form(...),
    crop: str | None = Form(None),
    lang: str = Form("en"),
) -> DiagnoseResponse:
    await image.read()  # consume the upload; real inference happens in Issue #2-4
    return DiagnoseResponse(
        request_id=str(uuid.uuid4()),
        disease="Tomato___Late_blight",
        disease_display="Late Blight (stub)",
        confidence=0.0,
        source="unclear",
        severity="low",
        treatment_steps=["Stub response — classifier not yet trained (Issue #2)."],
        organic_alternatives=["Stub response."],
        caveat="This is placeholder data for Phase 1 infrastructure testing.",
        synthetic=True,
        trace=TraceInfo(routed_to_gemini=False, cache_hit=False),
    )

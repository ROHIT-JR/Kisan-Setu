"""Module B stub. Real rules engine + NDVI + Gemini narration lands in Issues #5-7."""
import uuid
from fastapi import APIRouter
from pydantic import BaseModel
from app.models.schemas import (
    AdvisoryResponse, District, SoilStatus, NDVISeries, NDVIPoint,
    WeatherForecast, Recommendation,
)

router = APIRouter()


class AdvisoryRequest(BaseModel):
    district_code: str
    crop: str
    season: str
    lang: str = "en"


@router.post("/api/advisory", response_model=AdvisoryResponse)
async def advisory(req: AdvisoryRequest) -> AdvisoryResponse:
    return AdvisoryResponse(
        request_id=str(uuid.uuid4()),
        district=District(
            lgd_code=req.district_code, name="Stub District", state="Stub State",
            lat=0.0, lon=0.0, agro_climatic_zone="unspecified",
        ),
        soil=SoilStatus(
            ph=6.8, ec=0.3, organic_carbon=0.4, n="low", p="medium", k="high",
            micronutrients={"zn": "deficient", "fe": "sufficient"},
            synthetic=True, source="Phase 1 stub — real SHC ingestion is Issue #6",
        ),
        ndvi=NDVISeries(
            series=[NDVIPoint(date="2026-01-15", value=0.42)],
            trend="stable", cache_age_days=0,
        ),
        weather=WeatherForecast(rainfall_forecast_mm=0.0),
        recommendations=[
            Recommendation(
                practice="stub_practice",
                title="Stub recommendation",
                rationale="Rules engine not yet implemented (Issue #7).",
                evidence=["stub"],
                expected_benefit="N/A",
            )
        ],
        narrative="This is a stub advisory. The deterministic rules engine and Gemini narration ship in Issue #7.",
        engine="deterministic_rules + llm_narration",
    )

"""Pydantic schemas matching the API contracts in docs/prompt.md §12."""
from typing import Literal
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str
    timestamp: str


class TraceInfo(BaseModel):
    cnn_confidence: float | None = None
    routed_to_gemini: bool = False
    cnn_ms: int | None = None
    gemini_ms: int | None = None
    cache_hit: bool = False


class DiagnoseResponse(BaseModel):
    request_id: str
    disease: str
    disease_display: str
    confidence: float
    source: Literal["cnn", "gemini_fallback", "unclear"]
    severity: Literal["low", "moderate", "severe"]
    treatment_steps: list[str]
    organic_alternatives: list[str]
    caveat: str
    synthetic: bool = False
    trace: TraceInfo


class District(BaseModel):
    lgd_code: str
    name: str
    state: str
    lat: float
    lon: float
    agro_climatic_zone: str


class SoilStatus(BaseModel):
    ph: float
    ec: float
    organic_carbon: float
    n: Literal["low", "medium", "high"]
    p: Literal["low", "medium", "high"]
    k: Literal["low", "medium", "high"]
    micronutrients: dict[str, str]
    synthetic: bool = False
    source: str


class NDVIPoint(BaseModel):
    date: str
    value: float


class NDVISeries(BaseModel):
    series: list[NDVIPoint]
    trend: Literal["improving", "stable", "declining"]
    cache_age_days: int


class WeatherForecast(BaseModel):
    rainfall_forecast_mm: float
    source: str = "Open-Meteo"


class Recommendation(BaseModel):
    practice: str
    title: str
    rationale: str
    evidence: list[str]
    expected_benefit: str


class AdvisoryResponse(BaseModel):
    request_id: str
    district: District
    soil: SoilStatus
    ndvi: NDVISeries
    weather: WeatherForecast
    recommendations: list[Recommendation]
    narrative: str
    engine: str = "deterministic_rules + llm_narration"


class AddDistrictRequest(BaseModel):
    lgd_code: str
    name: str
    state: str
    block_code: str = ""
    lat: float
    lon: float
    agro_climatic_zone: str = "unspecified"

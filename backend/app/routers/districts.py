"""Module C support. Serves the seeded LGD district list and the add-district demo flow (Issue #8)."""
import csv
from pathlib import Path
from fastapi import APIRouter
from app.models.schemas import District, AddDistrictRequest

router = APIRouter()

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "lgd_districts.csv"

_districts: list[District] = []


def _load() -> list[District]:
    global _districts
    if _districts:
        return _districts
    with DATA_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=",")
        _districts = [
            District(
                lgd_code=row["lgd_code"],
                name=row["name"],
                state=row["state"],
                lat=float(row["lat"]),
                lon=float(row["lon"]),
                agro_climatic_zone=row["agro_climatic_zone"],
            )
            for row in reader
        ]
    return _districts


@router.get("/api/districts", response_model=list[District])
def list_districts() -> list[District]:
    return _load()


@router.post("/api/districts", response_model=District)
def add_district(req: AddDistrictRequest) -> District:
    """Demo-only in-memory add. A config/data change, never a code change — proves onboarding needs no redeploy."""
    district = District(
        lgd_code=req.lgd_code, name=req.name, state=req.state,
        lat=req.lat, lon=req.lon, agro_climatic_zone=req.agro_climatic_zone,
    )
    _load().append(district)
    return district

# Architecture

Full detail: [`prompt.md` §5](./prompt.md) and [`prompt.md` §7](./prompt.md).

## Three modules

- **Module A — Field Diagnostic**: ONNX-served CNN with a 0.70 confidence gate;
  below that, or on an out-of-distribution image, Gemini Flash multimodal
  handles it. See `backend/app/services/classifier.py`, `gemini.py` (Issues #2-4).
- **Module B — Regenerative Soil Advisory**: a deterministic rules engine
  (`backend/app/data/crop_rotation_rules.yaml` + `rotation_engine.py`) combining
  Soil Health Card data, cloud-masked Sentinel-2 NDVI, and Open-Meteo forecasts.
  Gemini narrates the structured output — it does not predict anything (Issues #5-7).
- **Module C — District Officer Dashboard**: the ministry-pilot artifact. Map,
  hotspots, stats, CSV export, live "Add a District" flow (Issue #8).

## Data model

Every record carries `state_code` / `district_code` / `block_code` using LGD
(Local Government Directory) codes. Onboarding a new district is a data change,
not a code change — proved live via the Add District flow.

## Tech stack

See [`prompt.md` §7](./prompt.md) for the full stack table.

## Diagram

```
Farmer (browser)                Officer (browser)
      │                                │
      ▼                                ▼
   FarmerApp.jsx                OfficerDashboard.jsx
      │                                │
      └───────────────┬────────────────┘
                       ▼
              FastAPI (Cloud Run)
      ┌────────────────┼─────────────────┐
      ▼                ▼                 ▼
 classifier.py    rotation_engine.py   districts.py
      │                │                 │
      ▼                ▼                 ▼
 gemini.py       earth_engine.py    Firestore
 (Flash, cached)  (NDVI, cached)    (cache + records)
```

# Scale — from 3 districts to a state rollout

## Current coverage

3 pilot districts, chosen for distinct agro-climatic profiles (see
`backend/app/data/lgd_districts.csv`):

| District | State | LGD code | Why chosen |
|---|---|---|---|
| Nashik | Maharashtra | 581 | Semi-arid Western Plateau, onion/grape cash-crop belt |
| Ludhiana | Punjab | 174 | Irrigated Trans-Gangetic Plains, high-input wheat-paddy rotation |
| Warangal | Telangana | 602 | Rainfed Southern Plateau, cotton/paddy, groundwater stress |

Chosen to stress-test the rules engine and NDVI pipeline across irrigated,
semi-arid, and rainfed conditions before claiming broader coverage.

## What onboarding a new district requires

Because every record is keyed by LGD (`state_code` / `district_code` /
`block_code`), adding a district is a **data change, not a code change**:

1. Add a row to `backend/app/data/lgd_districts.csv` (or use the live
   "Add a District" form in the Officer Dashboard — Issue #8).
2. Seed Soil Health Card data for that district (Issue #6 ingestion pipeline).
3. Trigger one Earth Engine NDVI pull for that district polygon; it caches
   per-district per-week in Firestore from then on (Issue #5).
4. No frontend or backend redeploy is required.

## Cost per 10,000 farmers

See [`docs/cost-analysis.md`](docs/cost-analysis.md) for the full free-tier
breakdown. At current architecture, Cloud Run's free tier (2M requests/month)
comfortably covers a district-scale rollout; the binding constraint is the
Gemini API's ~1000 requests/day free allowance, mitigated by aggressive
Firestore caching of both Gemini and Earth Engine responses.

## Integration path

**Integration-ready via published Soil Health Card data formats** and LGD
administrative codes — the same identifiers used by Indian government systems
(Soil Health Card portal, PM-KISAN beneficiary data, Kisan Call Centre). This
repository does not claim an existing integration with any of these systems;
it claims that its data model does not need to change to accept one.

## Limitations of this claim

This is an architectural readiness argument, not a validated deployment. It has
not been piloted with any state agriculture department. Language here should
stay in the "integration-ready" register — see `AGENTS.md` §5 (Language
discipline).

# Cost analysis — the ₹0 architecture

Full detail and quota traps: see [`track4-execution-package.md` Part 2.5](./track4-execution-package.md).

## Summary

Kisan Setu runs entirely within Google Cloud's Always Free tier. The one service
that would have charged us — **Vertex AI** — is not used anywhere in this repo.
Training happens on Google Colab's free T4 GPU; inference runs as ONNX Runtime
inside the Cloud Run container.

| Service | Used for | Free allowance | Guardrail in this repo |
|---|---|---|---|
| Cloud Run | API + frontend hosting | 2M req, 180k vCPU-sec/mo | `--min-instances=0 --max-instances=2 --memory=512Mi`, `us-central1` |
| Cloud Build | CI/CD | 120 build-min/day | `.github/workflows/deploy.yml` |
| Firestore | Cache + records | 1 GiB storage | Cache-first on every external call |
| Gemini API (AI Studio) | Fallback diagnosis + narration | Flash-class, ~1000 req/day | `MOCK_GEMINI`, `MAX_GEMINI_CALLS_PER_DAY`, Firestore cache keyed by input hash |
| Earth Engine | NDVI | 150 EECU-hrs/mo, Community Tier | Pre-computed + cached per district per week, never called live in the demo |
| Open-Meteo, OSM/Leaflet | Weather, maps | Free, no key | — |

## Estimated cost per 10,000 farmers

At Cloud Run's free-tier ceiling (2M requests/month) a district of ~10,000 farmers
generating a handful of requests per farmer per month stays comfortably inside the
free allowance. See [`SCALE.md`](../SCALE.md) for the full onboarding-cost argument.

**Estimated cost today: ₹0.** This will be revisited once real usage data exists —
this document should not be quoted with more precision than that.

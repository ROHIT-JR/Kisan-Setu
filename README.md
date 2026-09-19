# Kisan Setu

AI-powered regenerative agriculture advisory for Indian smallholder farmers.
Combines Soil Health Card data, Sentinel-2 NDVI via Google Earth Engine, and
Gemini multimodal crop diagnostics into a multilingual advisory platform with
district-level dashboards.

Built for Google Cloud's **"Build with AI: Code for Communities — Second
Edition"** hackathon (Hack2Skill), Track 4: AgriN & Regenerative Agricultural
Intelligence.

**Read [`AGENTS.md`](AGENTS.md) before contributing — it holds the project's
hard constraints (₹0 budget, language discipline, synthetic-data labeling) that
every human and AI agent working on this repo must follow.**

## Status

🚧 **Phase 1 — deployable skeleton.** Stub API + placeholder UI. See
[`docs/prompt.md`](docs/prompt.md) for the full build plan and phase breakdown.

Live URL: _pending first deploy — see Issue #1_.

## Architecture

Three modules — see [`docs/architecture.md`](docs/architecture.md) for detail:

1. **Field Diagnostic** — ONNX crop-disease classifier with a confidence-gated
   Gemini multimodal fallback.
2. **Regenerative Soil Advisory** *(the differentiator)* — a deterministic
   rules engine over Soil Health Card + NDVI + weather data, narrated by
   Gemini. Not a trained predictive model.
3. **District Officer Dashboard** — the ministry-pilot artifact: map,
   hotspots, stats, CSV export, live district onboarding.

## Honesty benchmark

The single biggest differentiator in this project is measuring, not hiding,
the PlantVillage-to-field domain gap. Once Issue #2/#3 land, this section will
show:

| PlantVillage (lab) accuracy | Cropped-PlantDoc (field) accuracy | PlantDoc + Gemini fallback |
|---|---|---|
| TBD | TBD | TBD |

**No accuracy number is ever quoted alone in this repo — see `AGENTS.md`.**

## Local development

```bash
cp .env.example .env
docker compose up --build
# backend: http://localhost:8080
# frontend: http://localhost:5173
```

## Repository structure

See [`docs/prompt.md` §10](docs/prompt.md) for the full target layout.

## Limitations

- Phase 1 endpoints return stub/synthetic data, clearly flagged `synthetic: true`.
- Voice input (Web Speech API) is Chrome/Edge only.
- Model accuracy numbers are not yet measured — do not quote any until Issue #3 lands.

## Licence

Apache License 2.0 — see [`LICENSE`](LICENSE).

## Team & AI tooling

4-person team building with AI coding agents (Claude Code + Google
Antigravity). See [`AGENTS.md`](AGENTS.md) for the rules every agent session
must follow, and [`docs/antigravity-guide.md`](docs/antigravity-guide.md) for
the Antigravity setup guide.

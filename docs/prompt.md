# BUILD PROMPT — Kisan Setu

> **Which model should run this?** See §0.5. Short version: **heavy reasoning** (Claude Opus via `opusplan`, or Gemini 3 Pro in Antigravity) for Phases 2, 3 and 5; **fast** (Sonnet / Gemini Flash) for Phases 1 and 4. Team setup: 3 members on Claude Code, 1 on Antigravity — see `antigravity-guide.md`.

> **How to use this file:** give Claude Code both `prompt.md` and `track4-execution-package.md`. Say: *"Read track4-execution-package.md for background context, then follow prompt.md. Start at PHASE 1 only."*

---

## 0. WHO YOU ARE AND WHAT WE'RE DOING

You are the lead engineer on a 4-person team building **Kisan Setu**, a regenerative agriculture advisory platform for Indian smallholder farmers.

This is a competition submission for the **Google Cloud "Build with AI: Code for Communities — Second Edition"** hackathon on Hack2Skill, **Track 4: AgriN & Regenerative Agricultural Intelligence**.

- **Repository:** `https://github.com/ROHIT-JR/Kisan-Setu`
- **Deadline:** 30 September 2026 (11 days from start)
- **Team:** 4 members
- **Budget: ₹0.** Everything must run on permanent free tiers. This is a hard constraint, not a preference.

---

## 0.5 MODEL SELECTION — WHICH MODEL RUNS WHICH PHASE

Match the model to the **kind of thinking** the phase needs, not to its importance.

| Phase | Thinking | Model class | Reason |
|---|---|---|---|
| **1** Skeleton | Execution | **FAST** — Sonnet / Gemini Flash | Fully-specified boilerplate. Reasoning models burn quota for nothing. |
| **2** Module A | Mixed | **HEAVY** for the class mapping and split strategy, **FAST** for notebooks | PlantDoc↔PlantVillage class mapping is a genuine judgment call that silently corrupts the differentiator if wrong |
| **3** Module B | **HEAVY** | Opus / **Gemini 3 Pro preferred** | Earth Engine's API is idiosyncratic and cloud-masking is easy to get subtly wrong; the rules engine encodes agronomy domain logic |
| **4** Module C + polish | Execution | **FAST** | React, Leaflet, i18n, logging |
| **5** Submission docs | **HEAVY** | Opus / Gemini 3 Pro | Language discipline and the honesty/persuasion balance are exactly what a fast model gets wrong |

**This team's setup: 3 × Claude Code + 1 × Google Antigravity.**
- **Claude Code members:** use `/model opusplan` — Opus for planning, Sonnet for execution, automatically.
- **Antigravity member:** Gemini 3 Pro by default, free during public preview. Agent requests run on a **weekly** allowance, so front-load reasoning-heavy work early in the week. See `antigravity-guide.md`.
- **Anyone who'd rather not use their Claude subscription** can fall back to Antigravity (free for everyone), or Cursor Pro (free with student verification). ⚠️ GitHub Copilot Student sign-ups were paused from 20 April 2026.

**Two operating rules:**
1. **Start a fresh session for each phase** and re-attach this file. A session running since Phase 1 will have drifted on the ₹0 constraint and the language discipline by Phase 3 — the two rules where a lapse is silent and expensive.
2. **Cross-model review before submission.** Whatever built the code must not be the thing that reviews it. Run §13 through a different vendor's model — a model reviewing its own output shares its own blind spots.

> Model lineups and free tiers shift monthly. Check what's actually available on your account rather than trusting any fixed model name in this file.

---

## 1. THE FIVE HARD REQUIREMENTS

Failing any one of these disqualifies the submission entirely:

1. **A LIVE DEPLOYED PUBLIC URL must exist and work.** This is checked by a human. It must be live by end of Phase 1.
2. **Google AI integration is mandatory.** Submissions without it are not considered at all.
3. **Public GitHub repository** with all reused open-source components cited.
4. **Demo video (3–5 min)** showing a working end-to-end flow.
5. **Pitch deck (10–12 slides).**

---

## 2. THE SCORING RUBRIC — OPTIMIZE FOR THIS

| Weight | Criterion | What it means |
|---|---|---|
| 25% | AI/Technical Execution | Is Google AI doing **meaningful** work? Does it function end-to-end? |
| 20% | Problem-Solution Fit | Does it directly address the stated challenge? |
| 20% | Depth & Reach Across India | Can it scale from one district to many states? |
| 20% | Deployability & Scalability | Could a ministry pilot this **within weeks**? |
| 15% | Impact Potential | How many people, across how many states? |

**Read this carefully: only 25% is technical.** Do not over-invest in model accuracy at the expense of the district dashboard, the scale story, or deployment reliability. A beautiful model behind a broken URL scores zero.

---

## 3. THE CORE INSIGHT THAT DRIVES THE ARCHITECTURE

PlantVillage-trained crop disease models report **99%+ accuracy in-distribution but collapse to ~31% on real field images** (Mohanty et al. 2016, arXiv:1604.03169). Independent replication puts in-the-wild performance below 40%. The dataset is 54,306 lab images on uniform backgrounds — single leaves, facing up, perfectly lit.

Every competing team will train on PlantVillage and put a fake-high number on their slide.

**Our differentiator is that we measure and mitigate this gap:**
1. Train on PlantVillage, **benchmark on Cropped-PlantDoc** (real field imagery) from `https://github.com/pratikkayal/PlantDoc-Dataset`
2. Publish a **three-column honesty table** in the README, the UI, and the deck: `PlantVillage acc | PlantDoc (field) acc | PlantDoc + Gemini fallback acc`
3. A **confidence gate** routes low-confidence images to Gemini multimodal instead of returning a wrong answer confidently

> **Absolute rule:** never generate code, docs, UI copy, or comments quoting a single accuracy number without both the lab and field columns. This applies everywhere, including variable names and log messages.

---

## 4. ZERO-COST ARCHITECTURE — NON-NEGOTIABLE

### Never use these (they will charge us)
- ❌ **Vertex AI** — no ongoing free tier; endpoints bill per node-hour even when idle
- ❌ **Gemini Pro models** — left the free tier in April 2026; Flash/Flash-Lite only
- ❌ **Cloud SQL** — charges from the moment an instance is created
- ❌ **Cloud Load Balancer** — never free
- ❌ **Cloud Translation API at runtime** — use pre-translated static JSON instead
- ❌ **Cloud Speech-to-Text / Text-to-Speech** — use the browser Web Speech API instead
- ❌ **Balanced or SSD persistent disks**

### Use these (permanent free tiers)
| Purpose | Service | Free allowance |
|---|---|---|
| API + frontend hosting | **Cloud Run** (`us-central1`) | 2M req, 180k vCPU-sec, 360k GiB-sec/mo |
| CI/CD | **Cloud Build** | 120 build-min/day |
| Database + cache | **Firestore** | 1 GiB storage |
| Model/image storage | **Cloud Storage** | 5 GB-months |
| Auth | **Firebase Auth** | 50K MAU |
| LLM | **Gemini API via AI Studio**, Flash-class only | ~10–15 RPM, ~1000 req/day |
| Satellite | **Earth Engine**, noncommercial Community Tier | 150 EECU-hours/mo |
| Model training | **Google Colab** free T4 GPU | Free |
| Model serving | **ONNX Runtime inside the Cloud Run container** | Free |
| Weather | **Open-Meteo** | Free, no key needed |
| Maps | **OpenStreetMap + Leaflet** | Free |

### Mandatory cost guardrails in code
```
Cloud Run deploy flags:  --min-instances=0 --max-instances=2 --memory=512Mi --region=us-central1
Env vars:                MOCK_GEMINI, MAX_GEMINI_CALLS_PER_DAY, GEMINI_MODEL
```
- Cache-first on **every** external call (Gemini, GEE, weather). No exceptions.
- Gemini cache key: `sha256(image_bytes + prompt_version)`
- GEE cache: per district, per week
- Hard daily call counter that **fails closed** when the limit is hit
- `MOCK_GEMINI=true` returns canned responses so teammates develop without burning quota

---

## 5. SYSTEM ARCHITECTURE — THREE MODULES

### MODULE A — Field Diagnostic
```
Farmer uploads crop photo
  → CNN (MobileNetV2 / DenseNet121, fine-tuned on PlantVillage, heavy augmentation,
    SPECIMEN-LEVEL train/test split, exported to ONNX, served in-container)
  → if max softmax < 0.70 OR out-of-distribution check fires
      → route to Gemini multimodal (Flash) with image + top-3 CNN predictions + crop context
  → return: disease, confidence, treatment steps, organic alternatives, severity
    — in the farmer's language
```

### MODULE B — Regenerative Soil Advisory (PRIMARY DIFFERENTIATOR)
```
Soil Health Card data (pH, EC, organic carbon, N/P/K, S, Zn/Cu/Fe/Mn/B)
  + Sentinel-2 NDVI 12-month time series (Google Earth Engine, cloud-masked)
  + Open-Meteo forecast
  → deterministic rules engine (crop rotation, cover crops, green manure,
    salinity management) defined in crop_rotation_rules.yaml
  → Gemini generates the farmer-facing narrative from the structured rules output
  → always surface WHY: "your organic carbon is 0.4% (low) and declined over two seasons"
```

> **This is a rules engine with LLM narration. Never describe it as a trained predictive model in code, comments, docs, or UI copy.** Accurate description beats impressive description.

### MODULE C — District Officer Dashboard (CARRIES 40% OF THE RUBRIC)
```
Map of disease report clusters by block, colour-coded by crop
  + soil degradation hotspots (organic carbon below threshold)
  + NDVI anomaly alerts (district below its own historical baseline)
  + summary stats: farmers served, advisories issued, top 3 diseases this month
  + CSV export
  + live "Add a District" onboarding flow
```

---

## 6. GOOGLE AI INTEGRATIONS — ALL MUST BE LOAD-BEARING

| # | Integration | Why it's not decorative |
|---|---|---|
| 1 | Gemini multimodal (Flash) | Handles images the CNN can't — fixes a **measured** failure mode |
| 2 | Gemini text | Generates the regenerative advisory narrative — the advisory *is* the product |
| 3 | Google Earth Engine | Sentinel-2 NDVI trends no other source provides |
| 4 | Google Colab | Model training infrastructure |
| 5 | Firebase / Cloud Run / Firestore | The deployment and data substrate |

Also build an **"AI pipeline trace"** UI panel showing which service handled each step, with latency and the routing decision (e.g. *"CNN confidence 0.42 → routed to Gemini → final answer"*). Make the integration **visible** to a judge rather than merely claimed.

---

## 7. TECH STACK

```
Backend    Python 3.11, FastAPI, Pydantic v2, uvicorn
ML         PyTorch (train on Colab) → ONNX → onnxruntime (serve on Cloud Run)
Frontend   React 18 + Vite + TailwindCSS
Maps       Leaflet + OpenStreetMap tiles
Data       Firestore (records + cache), Cloud Storage (model artifacts)
Deploy     Docker → Cloud Run (us-central1), GitHub Actions CI/CD
Geospatial earthengine-api, COPERNICUS/S2_SR_HARMONIZED
Weather    Open-Meteo (no key)
i18n       Static JSON files, en/hi/ta/mr
Voice      Browser Web Speech API + SpeechSynthesis (client-side, free)
```

---

## 8. ENGINEERING RULES — NON-NEGOTIABLE

1. **DEPLOY FIRST.** Before any model work, ship a live Cloud Run URL with stub endpoints. Everything else builds against a running system.
2. **MULTI-TENANT FROM DAY 1.** Every record carries `state_code`, `district_code`, `block_code` using **LGD (Local Government Directory)** codes. Adding a district must be a config/data change, never a code change.
3. **LABEL SYNTHETIC DATA.** Any generated record carries `synthetic: true` in the API response **and** is visibly flagged in the UI. Never present synthetic data as real.
4. **CACHE AGGRESSIVELY.** Cache-first on every external call.
5. **CLOUD-MASK NDVI.** Unmasked Sentinel-2 NDVI is invalid. Mask clouds and shadows before computing; gap-fill occluded dates. Use `COPERNICUS/S2_SR_HARMONIZED`, not `S2_SR`.
6. **SPECIMEN-LEVEL SPLITS.** Never split PlantVillage at image level — it leaks near-duplicates and inflates accuracy.
7. **PER-CLASS METRICS.** Report precision/recall/F1 per class, not just accuracy. PlantVillage has known class imbalance.
8. **GRACEFUL DEGRADATION.** Every external call needs a timeout and a fallback. The demo must never hard-fail live.
9. **CITE EVERYTHING.** Submission rules require citing reused open-source components.
10. **NO SECRETS IN THE REPO.** `.env.example` only. The repo is public.

---

## 9. LANGUAGE DISCIPLINE

Applies to code comments, docstrings, README, UI copy, and commit messages.

| ❌ Never write | ✅ Write instead |
|---|---|
| "AI predicts soil health" | "rules engine with LLM narration" |
| "integrated with government systems" | "integration-ready via published SHC data formats" |
| "deployed across BRICS nations" | "designed to extend to other BRICS contexts" |
| "99% accuracy" | "96% lab (PlantVillage) / 61% field (PlantDoc)" |
| "real-time national coverage" | "3 pilot districts, architecture supports N districts" |

**Prefer underclaiming.** A judge who catches one inflated claim discounts everything else in the submission.

---

## 10. REPOSITORY STRUCTURE

```
Kisan-Setu/
├── README.md                      # honesty table + architecture + LIMITATIONS
├── SCALE.md                       # ministry/state onboarding argument + cost table
├── LICENSE                        # Apache 2.0
├── .gitignore
├── .env.example
├── docker-compose.yml
├── docs/
│   ├── architecture.md
│   ├── data-sources.md            # provenance for every dataset, real vs synthetic
│   ├── model-card.md              # benchmarks, limitations, intended use
│   ├── cost-analysis.md           # the ₹0 free-tier breakdown
│   └── demo-script.md             # the 3-5 min video run sheet
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── config.py              # env vars, quota limits, feature flags
│       ├── routers/
│       │   ├── health.py
│       │   ├── diagnose.py        # Module A
│       │   ├── advisory.py        # Module B
│       │   ├── districts.py       # Module C
│       │   └── trace.py           # AI pipeline trace
│       ├── services/
│       │   ├── classifier.py      # ONNX inference + confidence gate
│       │   ├── gemini.py          # Flash-only, cached, quota-capped
│       │   ├── earth_engine.py    # cloud-masked NDVI, cached
│       │   ├── soil_health.py     # SHC ingestion
│       │   ├── weather.py         # Open-Meteo
│       │   ├── rotation_engine.py # deterministic rules
│       │   ├── cache.py           # Firestore cache-first helper
│       │   └── quota.py           # daily counter, fails closed
│       ├── models/                # Pydantic schemas
│       └── data/
│           ├── lgd_districts.csv
│           ├── shc_sample.csv
│           └── crop_rotation_rules.yaml
├── ml/
│   ├── notebooks/
│   │   ├── 01_train_plantvillage.ipynb   # Colab-ready
│   │   ├── 02_benchmark_plantdoc.ipynb
│   │   └── 03_export_onnx.ipynb
│   ├── train.py
│   ├── evaluate.py                # regenerates the 3-column table
│   └── results/
├── frontend/
│   ├── Dockerfile
│   └── src/
│       ├── pages/
│       │   ├── FarmerApp.jsx
│       │   ├── OfficerDashboard.jsx
│       │   └── AddDistrict.jsx
│       ├── components/
│       │   ├── AITracePanel.jsx
│       │   └── SyntheticBadge.jsx
│       └── i18n/
│           ├── en.json
│           ├── hi.json
│           ├── ta.json
│           └── mr.json
└── .github/workflows/deploy.yml
```

---

## 11. BUILD PHASES

### ⚙️ PHASE 1 — DEPLOYABLE SKELETON (Days 1–2) ← **START HERE, STOP HERE**
> 🤖 **Run this phase on a FAST model** (Sonnet-class / Gemini Flash). It is boilerplate.

**Goal: a live public URL exists by the end of this phase. Nothing else matters until it does.**

**1.1 Scaffold**
- Create the full directory structure above
- `.gitignore` (Python + Node + `.env` + model artifacts)
- Apache 2.0 `LICENSE`
- `.env.example` listing every variable with an explanatory comment

**1.2 Backend**
- FastAPI app with CORS configured
- `GET /health` → `{status, version, timestamp}`
- `POST /api/diagnose` → accepts multipart image, returns **stub** response matching the final schema, `synthetic: true`
- `POST /api/advisory` → accepts `{district_code, crop, season}`, returns **stub** advisory, `synthetic: true`
- `GET /api/districts` → returns seeded LGD districts
- `POST /api/districts` → add-district endpoint
- `GET /api/trace/{request_id}` → stub trace
- Full Pydantic schemas now — the real implementations fill them in later
- `config.py` reading all env vars with safe defaults

**1.3 Frontend**
- React + Vite + Tailwind
- `/` → FarmerApp: image upload, language selector, result card, AI trace panel (collapsed)
- `/officer` → OfficerDashboard: Leaflet map + stats cards + CSV export button
- `/officer/add-district` → AddDistrict form
- `SyntheticBadge` component rendering wherever `synthetic: true`
- i18n scaffold with `en.json` populated, others stubbed

**1.4 Containers + deploy**
- Multi-stage Dockerfiles for both services (keep images small)
- `docker-compose.yml` for local dev
- `.github/workflows/deploy.yml` — on push to `main`, build with Cloud Build and deploy to Cloud Run with the free-tier flags from §4
- `docs/cost-analysis.md` documenting the ₹0 architecture

**1.5 Seed data**
- `lgd_districts.csv` with at least 3 real Indian districts (include LGD codes, state, lat/lon)
- Choose districts with distinct agro-climatic profiles and justify the choice in a comment

**✅ Phase 1 acceptance:** a public URL loads both pages with placeholder data; pushing to `main` redeploys automatically; the AI trace panel renders with stub content.

**⛔ STOP after Phase 1. Report the live URL and wait for the go-ahead before Phase 2.**

---

### 🧠 PHASE 2 — MODULE A (Days 3–6)
> 🤖 **HEAVY model for the PlantDoc class mapping and split strategy** (Opus / Gemini 3 Pro); FAST model for the notebook code.
- `01_train_plantvillage.ipynb` — Colab-ready, specimen-level split, heavy augmentation (random backgrounds, lighting jitter, blur, rotation, occlusion), trains MobileNetV2 and DenseNet121
- `02_benchmark_plantdoc.ipynb` — class mapping onto the PlantVillage label space, zero-shot eval, confusion matrix, documents unmapped classes honestly
- `03_export_onnx.ipynb` — export, verify size under ~50 MB and CPU inference under 1s
- `evaluate.py` regenerating the three-column table from scratch
- `classifier.py` — ONNX inference + confidence gate at 0.70 + OOD check
- `gemini.py` — Flash-only, strict JSON output schema, Firestore cache, quota counter, `MOCK_GEMINI` flag, graceful "not a plant / unclear image" handling
- `docs/model-card.md`

---

### 🌱 PHASE 3 — MODULE B (Days 5–8)
> 🤖 **HEAVY model throughout — Gemini 3 Pro preferred** for the Earth Engine work. This phase contains the differentiator and the most silent-failure surface in the project.
- `earth_engine.py` — service-account auth, `COPERNICUS/S2_SR_HARMONIZED`, cloud/shadow masking, `normalizedDifference(['B8','B4'])`, 12-month series, gap-filling, per-district weekly cache, EECU usage logging
- `soil_health.py` — ingest SHC data (evaluate `https://github.com/google-research-datasets/india-soil-health-card`; also `data.gov.in`), normalize to an LGD-keyed schema, seed 3 districts with real cited data, flag any synthetic records
- `weather.py` — Open-Meteo, cached
- `crop_rotation_rules.yaml` + `rotation_engine.py` — low organic carbon → cover crop + FYM; low N + cereal history → legume rotation; high EC → salinity management
- Gemini narration layer over the structured rules output
- `docs/data-sources.md` with provenance for every dataset

---

### 📊 PHASE 4 — MODULE C + POLISH (Days 7–9)
> 🤖 **FAST model** for the code; use Gemini to generate the i18n JSON files.
- Officer dashboard fully wired: clusters, hotspots, NDVI anomalies, stats, CSV export
- "Add a District" flow working end-to-end and demoable live
- i18n files completed for hi/ta/mr (generate with Gemini during development, then commit)
- Web Speech API voice input + SpeechSynthesis playback
- AI trace panel wired to real logging
- README with the honesty table, architecture diagram, Limitations section
- `SCALE.md` with onboarding steps and the ₹0 cost table
- Low-literacy affordances: icon-driven nav, large tap targets

---

### 🎬 PHASE 5 — SUBMISSION (Days 10–11)
> 🤖 **HEAVY model**, and run the adversarial self-check on a **different model family** than the one that wrote the code.
- `docs/demo-script.md`: 30s problem → 45s the domain-gap insight → 90s live walkthrough → 45s scale → 30s close
- Verify the live URL from a phone on mobile data, not just a laptop
- Final adversarial review (see §13)
- Submit a full day early — portals fail at deadline

---

## 12. API CONTRACTS (implement these exact shapes in Phase 1)

```jsonc
// POST /api/diagnose  (multipart: image, district_code, crop?, lang?)
{
  "request_id": "uuid",
  "disease": "Tomato___Late_blight",
  "disease_display": "Late Blight",
  "confidence": 0.42,
  "source": "gemini_fallback",        // "cnn" | "gemini_fallback" | "unclear"
  "severity": "moderate",             // "low" | "moderate" | "severe"
  "treatment_steps": ["..."],
  "organic_alternatives": ["..."],
  "caveat": "Field accuracy for this crop is 61%. Confirm with your local KVK.",
  "synthetic": false,
  "trace": {
    "cnn_confidence": 0.42,
    "routed_to_gemini": true,
    "cnn_ms": 180,
    "gemini_ms": 1240,
    "cache_hit": false
  }
}

// POST /api/advisory  { district_code, crop, season, lang }
{
  "request_id": "uuid",
  "district": { "name": "...", "lgd_code": "...", "state": "..." },
  "soil": {
    "ph": 6.8, "ec": 0.3, "organic_carbon": 0.4,
    "n": "low", "p": "medium", "k": "high",
    "micronutrients": { "zn": "deficient", "fe": "sufficient" },
    "synthetic": false,
    "source": "Soil Health Card portal, 2024-25 cycle"
  },
  "ndvi": { "series": [{ "date": "2026-01-15", "value": 0.42 }], "trend": "declining", "cache_age_days": 3 },
  "weather": { "rainfall_forecast_mm": 45, "source": "Open-Meteo" },
  "recommendations": [
    {
      "practice": "legume_rotation",
      "title": "Rotate to green gram next season",
      "rationale": "Organic carbon at 0.4% is low and has declined across two seasons.",
      "evidence": ["soil.organic_carbon", "ndvi.trend"],
      "expected_benefit": "..."
    }
  ],
  "narrative": "<Gemini-generated, in requested language>",
  "engine": "deterministic_rules + llm_narration"
}
```

---

## 13. ADVERSARIAL SELF-CHECK — RUN BEFORE EVERY PHASE HANDOFF

Answer these honestly. Any hesitation is a bug to fix that day.

1. Is the live URL up right now?
2. Does any code, doc, or UI string quote an accuracy number without both columns?
3. Is any synthetic data presented as real, anywhere?
4. Have I called a Gemini Pro model or touched Vertex AI anywhere?
5. Is NDVI cloud-masked?
6. Does every external call have a timeout and a fallback?
7. Could a new district be onboarded without a code change?
8. What happens when a farmer photographs a crop we never trained on?
9. Is there a secret committed to this public repo?
10. Would the demo survive the Gemini daily quota being exhausted?

---

## 14. WHAT I WANT FROM YOU RIGHT NOW

**Execute PHASE 1 only.** Deliver the deployable skeleton.

**Before you start, ask me for:**
- GCP project ID and region confirmation
- Cloud Run service names
- Which 3 districts to seed (or propose 3 with agro-climatic justification and I'll confirm)

**While you work:**
- Flag every assumption you make explicitly
- Do not invent data, API responses, or citations
- Do not start model training — Phase 1 is infrastructure only
- Commit in logical chunks with clear messages
- If something in this prompt conflicts with the ₹0 constraint, **stop and tell me** rather than proceeding

When Phase 1 is complete, report the live URL and wait for my go-ahead before Phase 2.

# Track 4 Execution Package — AgriN / Regenerative Agricultural Intelligence
**Google Cloud "Build with AI: Code for Communities — Second Edition"**
Deadline: 30 Sept 2026 · Days remaining: 11 · Team size: 4

---

## PART 0 — DO THIS IN THE NEXT HOUR (blockers)

| # | Action | Owner | Why it's urgent |
|---|---|---|---|
| 0.1 | Register for Google Earth Engine at `https://earthengine.google.com/signup/`. **Register the project as NONCOMMERCIAL, Community Tier.** | M2 (Geospatial) | Approval **can take a day or two**. Hard dependency for Module B. Noncommercial registration is what keeps it free. |
| 0.2 | Confirm repo URL is `https://github.com/ROHIT-JR/Kisan-Setu` (Kisan = farmer) | You | Already correct. Verify the URL in the browser before pasting it into any submission form. |
| 0.3 | **Project A** — Google Cloud project with billing linked. Enable ONLY: Cloud Run, Cloud Build, Firestore, Cloud Storage, Earth Engine. **Do NOT enable Vertex AI.** | M3 (Deploy) | Vertex AI has no ongoing free tier. See Part 2.5. |
| 0.4 | **Project B** — separate Google AI Studio API key at `aistudio.google.com`, on a project with **NO billing linked** | M1 (ML) | Enabling billing can remove the Gemini free allowance rather than add to it. Keep them separate. |
| 0.5 | **Set a budget alert of ₹0 / $1 with email notification** on Project A (Billing → Budgets & alerts) | M3 | Your safety net. If anything starts charging, you know within hours. |
| 0.6 | Add all 4 members as repo collaborators | You | Claude Code needs a repo to work in |
| 0.7 | Register the team on Hack2Skill if not already done | You | Registration closes 30 Sept, same day as submission |

**If 0.1 stalls beyond 48 hours**, fall back to Sentinel-2 via the Copernicus Data Space (free, no approval) or use SoilGrids + static NDVI snapshots. Do not let a pending approval block Module B entirely — have M2 build against mock NDVI data from day 1 so the swap is a one-line change.

> **Note on billing:** since 3 Feb 2026 some GCP services require billing to be enabled. Linking a card does not mean being charged — the Always Free quotas still apply. The budget alert in 0.5 is what protects you.

---

## PART 1 — GITHUB REPO FORM (fill exactly as below)

**Owner:** ROHIT-JR

**Repository name:**
```
Kisan-Setu
```
*("Kisan" = farmer, "Setu" = bridge. Confirmed in use. Note the namespace is crowded — Kisan Suvidha, Kisan Sarathi, Kisan Rath and mKisan are all existing Indian government agri apps — so don't rely on the name to differentiate you. Lead the pitch with the regenerative advisory angle instead.)*

**Description (copy-paste, 254 chars):**
```
AI-powered regenerative agriculture advisory for Indian smallholder farmers. Combines Soil Health Card data, Sentinel-2 NDVI via Google Earth Engine, and Gemini multimodal crop diagnostics into a multilingual advisory platform with district-level dashboards.
```

**Configuration:**
- **Visibility:** `Public` ← required, submission rules demand a public or access-granted repo
- **Template:** `No template`
- **Add README:** `ON` ← turn this on, Claude Code will rewrite it
- **Add .gitignore:** `Python`
- **Add license:** `Apache License 2.0`

> Why Apache 2.0, not MIT: it includes an explicit patent grant, which reads as more deployment-ready to an evaluator assessing "could this be piloted within a ministry." Minor signal, zero cost.

---

## PART 2 — IDEA HARDENING (three adversarial review passes)

This is the "loop" you asked for. Each pass attacks the previous version. This is what a senior evaluator would do to your submission in a Q&A.

### Pass 1 — Attack: "This is just another PlantVillage classifier"

**The hit:** PlantVillage is the most tutorial-saturated dataset in applied agri-ML. Models trained on it report 99%+ in-distribution but collapse to ~31% on images captured under different conditions, and independent replication puts in-the-wild performance below 40%. Every team on this track will show a high accuracy number that means nothing.

**Hardening applied:**
1. Train on PlantVillage, **benchmark on Cropped-PlantDoc** (`github.com/pratikkayal/PlantDoc-Dataset`), which is real-field imagery specifically built because PlantVillage's lab setups make real-world efficacy poor.
2. Publish a **three-column honesty table** in the README, the app UI, and slide 6 of the deck:
   `PlantVillage test acc | PlantDoc (field) acc | PlantDoc + Gemini fallback acc`
3. Build a **confidence gate**: if softmax confidence < 0.70 OR the image fails a "is this even a leaf?" check, route to Gemini multimodal instead of returning a wrong label confidently.
4. Ship an explicit **"Model Limitations"** section in the README. Naming your own weakness before a judge finds it converts a vulnerability into evidence of rigor.

**Residual risk:** a judge may not care about methodology and just wants a working demo. Mitigated by the fact that the demo still works — this costs you nothing in demo quality.

---

### Pass 2 — Attack: "Nice app, but this doesn't scale to a ministry"

**The hit:** 20% of the rubric is *Depth & Reach Across India* and 20% is *Deployability & Scalability* — "could this be piloted within a ministry or across states in weeks?" A single-farmer chat app scores badly on both, no matter how good the model is. That's 40% of your score on the line.

**Hardening applied:**
1. **Module C is non-negotiable.** A district agriculture officer dashboard: disease report clusters on a map, soil organic-carbon decline hotspots, advisory adoption counts. This is the artifact a ministry pilots — not the farmer app.
2. **Multi-tenant data model from day 1.** Every record carries `state_code`, `district_code`, `block_code` (use LGD — Local Government Directory codes, the official Indian administrative hierarchy). Adding a new district becomes a config row, not a code change. Say this explicitly in the deck.
3. **Build an "Add a District" admin flow** in the demo, even if crude. Showing a judge you can onboard a new district live is worth more than ten slides claiming scalability.
4. **Ship a `SCALE.md`** in the repo: current coverage, what onboarding a new state requires, cost per 10k farmers on Cloud Run, and the integration path to existing government systems (Soil Health Card portal, Kisan Call Centre, PM-KISAN beneficiary data).

**Residual risk:** you're claiming a ministry integration path you haven't validated. Mitigation: phrase as "integration-ready via published SHC data formats," never "integrated with."

---

### Pass 3 — Attack: "Where is Google AI actually doing work?"

**The hit:** 25% of the rubric, the single heaviest weight, is *AI/Technical Execution — is Google AI doing meaningful work?* A TensorFlow CNN you trained yourself is **not Google AI integration** in the sense they mean. Teams fail this by bolting on one Gemini call for text generation and calling it done. Rules also state submissions without Google AI integration will not be considered at all.

**Hardening applied — five load-bearing Google AI integrations:**

| # | Integration | What it does | Why it's load-bearing (not decorative) |
|---|---|---|---|
| 1 | **Gemini multimodal** | Handles low-confidence / out-of-distribution crop images the CNN can't | Without it the system returns confidently wrong answers — it fixes a measured failure |
| 2 | **Gemini text** | Turns raw soil numbers (pH, EC, OC, N/P/K, Zn/Fe/B) + NDVI trend into a plain-language regenerative plan in the farmer's language | The advisory *is* the product; this generates it |
| 3 | **Google Earth Engine** | Sentinel-2 NDVI time-series per field polygon | Provides the crop-health trend no other data source gives you |
| 4 | **Cloud Translation + Speech-to-Text/TTS** | Voice-first multilingual interface | SHC cards are issued in 22 languages and 5 dialects — matching that is a scale argument, not a nice-to-have |
| 5 | **Google Colab (free T4 GPU)** for training + **Cloud Run** for serving | Model trained on Google infrastructure, served in-container via ONNX Runtime | ~~Vertex AI~~ **REMOVED — it has no ongoing free tier and would charge you per node-hour.** Colab is Google infrastructure and is free; say "trained on Google Colab, served on Cloud Run" in the deck. The rubric asks whether Google AI is doing meaningful work, not whether you paid for Vertex. |

5. **Instrument it.** Log every Gemini/GEE call with latency and outcome, and surface a small "AI pipeline trace" panel in the demo. Let the judge *see* Google AI working rather than take your word for it.

**Residual risk:** cost. Mitigate with aggressive caching (Firestore) of Gemini responses keyed by input hash, and GEE results cached per district per week.

---

### What the three passes changed

| Before hardening | After hardening |
|---|---|
| Crop disease app with soil advice bolted on | Regenerative advisory platform with diagnostics as one input |
| "97% accuracy" | Honest 3-column benchmark + confidence-gated fallback |
| One city/demo scope | LGD-coded multi-tenant model + live district onboarding |
| Gemini as a text wrapper | Five load-bearing Google AI integrations with visible tracing |
| Farmer-facing only | Farmer app + district officer dashboard (the pilot artifact) |

**Honest confidence assessment:** [Likely] this puts you in contention for the top 20. [Guessing] anything beyond that depends on execution quality, competitor strength you can't observe, and judge preference. Anyone promising a 99% win rate is selling you something.

---

## PART 2.5 — ZERO-COST ARCHITECTURE (verified Sept 2026)

**Verdict: the entire prototype can be built and deployed for ₹0, with one mandatory substitution and several quota disciplines.**

### ❌ The one thing that would have charged you

**Vertex AI has no ongoing free tier.** New GCP accounts get $300 in credits valid 90 days, and after that you pay standard rates — there is no permanent free allowance. A Vertex AI model-serving endpoint bills per node-hour whether or not anyone calls it. If you deployed the model there and left it running for 11 days, you would get a bill.

Also note: **the $300 Google Cloud trial credit no longer applies to Gemini API usage as of March 2026**, so don't plan around it.

**Substitution — and it's arguably a better story anyway:**

| Instead of | Use | Cost |
|---|---|---|
| Vertex AI training | **Google Colab** free tier (T4 GPU) or Kaggle Notebooks (30 GPU-hrs/week) | ₹0 |
| Vertex AI endpoint | **ONNX Runtime inside the Cloud Run container** | ₹0 within Cloud Run free tier |
| Vertex AI Gemini | **Gemini API via AI Studio** free tier | ₹0 |

MobileNetV2 exported to ONNX is ~14 MB and runs CPU inference in well under a second. It fits in a Cloud Run container with room to spare, has no cold-start penalty worth worrying about, and removes an entire external dependency that could fail live during your demo. Fewer moving parts on demo day is a feature.

### ✅ Free-tier budget for every service

| Service | Free allowance | Your expected use | Headroom |
|---|---|---|---|
| **Cloud Run** | 2M requests, 180,000 vCPU-sec, 360,000 GiB-sec/month | A few thousand requests | Enormous |
| **Cloud Build** | 120 build-minutes/day | ~20 builds/day × 3 min = 60 min | Comfortable |
| **Firestore** | 1 GiB storage; daily read/write operation caps | Cached advisories, district records | Fine **if you cache** |
| **Cloud Storage** | 5 GB-months Standard | Model artifacts, sample images | Fine |
| **Gemini API (AI Studio)** | **Flash / Flash-Lite only**, ~10–15 RPM, ~1,000 requests/day | Fallback diagnoses + advisory narration | **Tightest constraint — see below** |
| **Earth Engine** | Community Tier: **150 EECU-hours/month**, noncommercial | District NDVI pulls | Fine if cached |
| **Firebase Auth** | 50K monthly active users | A handful of demo accounts | Enormous |
| **Firebase Hosting** | 10 GB storage, 360 MB/day transfer | Frontend | Fine |
| **Network egress** | ~1 GB/month free | JSON responses, small images | **Watch this** |

### ⚠️ Four quota traps, with mitigations

**1. Gemini free tier is Flash-only.** Since April 2026, Pro models are no longer available on the free tier — only Flash and Flash-Lite. This is fine: Flash models are multimodal, so your image-fallback path works. **Hardcode a Flash model. Never call a Pro model.** A single accidental Pro call on a billing-enabled project starts charging.

**2. ~1,000 requests/day is easy to burn during testing.** Four developers hammering the diagnose endpoint will exhaust it by afternoon.
- Cache every Gemini response in Firestore keyed by `sha256(image_bytes + prompt_version)`
- Add a `MOCK_GEMINI=true` env flag returning canned responses for UI development
- Only M1 develops against the live key; everyone else uses mock mode
- **Record the demo video early in the day**, before the daily quota is touched

**3. Earth Engine now has quotas.** Since 27 April 2026 all noncommercial projects have a recurring monthly EECU quota, applied per project and resetting on the 1st. Community Tier gives 150 EECU-hours; the Contributor Tier raises it to 1,000. Exceeding it puts the account into **Restricted mode, which slows computation rather than billing you** — so there's no surprise-charge risk, but there is a demo-day-slowdown risk.
- Pre-compute NDVI for your 3 demo districts and store the results in Firestore
- Never call GEE live during the demo — serve from cache
- Register as noncommercial (students/academic qualify); reverification is annual

**4. Free-tier quotas are per *account*, not per project.** If your teammates each spin up their own Cloud Run projects, you all share the same free quota — this is the most common cause of confused billing alerts. One shared project, one owner.

### 💰 Free substitutions for the remaining services

| Planned | Free alternative | Trade-off |
|---|---|---|
| Cloud Translation API | **Pre-translated static JSON i18n files** (`en/hi/ta/mr.json`), translated once during development | None for a demo — arguably more reliable, no latency, no quota. Use Gemini once during dev to generate the translation files, commit them. |
| Cloud Speech-to-Text | **Browser Web Speech API** (`webkitSpeechRecognition`) — runs client-side, supports `hi-IN`, `ta-IN`, `mr-IN` | Chrome/Edge only. Acceptable for a demo; note it in Limitations. Zero backend cost, zero quota. |
| Cloud Text-to-Speech | **Browser `SpeechSynthesis` API** | Voice quality is lower than Cloud TTS. Free and instant. |
| IMD weather (paid/restricted) | **Open-Meteo** — free, no API key, no registration | None |
| Paid map tiles | **OpenStreetMap + Leaflet** or **MapLibre** | Google Maps JS API has a monthly free credit but requires billing; OSM avoids the question entirely |

> **Deck framing:** don't hide the free-tier architecture — lead with it. "Runs entirely within Google Cloud's Always Free tier: ₹0 infrastructure cost per district onboarded" is a *powerful* answer to the 20% Deployability criterion. A ministry official hearing "this costs nothing to pilot in ten more districts" is exactly the reaction you want. Put the cost table on slide 10.

### 🛡️ Cost guardrails to implement in code

- [ ] Budget alert at $1 with email to all four members
- [ ] `MAX_GEMINI_CALLS_PER_DAY` env var with a hard in-app counter that fails closed
- [ ] Firestore cache-first on every external call, no exceptions
- [ ] Cloud Run: `--min-instances=0` (scale to zero) and `--max-instances=2` (caps runaway cost)
- [ ] Cloud Run memory 512 MiB, not 2 GiB — free-tier GiB-seconds burn 4× faster at 2 GiB
- [ ] Deploy to `us-central1` (Tier 1 region, where free-tier compute applies)
- [ ] No Cloud Load Balancer — **load balancers are never free**
- [ ] No Cloud SQL — **it charges from the moment an instance is created**. Firestore only.

---

## PART 3 — REPOSITORY STRUCTURE

```
kisan-setu/
├── README.md                  # honest benchmarks + architecture + limitations
├── SCALE.md                   # the ministry/state onboarding argument
├── LICENSE
├── .gitignore
├── .env.example
├── docker-compose.yml         # local dev
├── docs/
│   ├── architecture.md
│   ├── data-sources.md        # provenance for every dataset
│   ├── model-card.md          # benchmarks, limitations, intended use
│   └── demo-script.md         # the 3-5 min video run sheet
├── backend/                   # FastAPI
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── routers/
│   │   │   ├── diagnose.py    # Module A
│   │   │   ├── advisory.py    # Module B
│   │   │   ├── districts.py   # Module C
│   │   │   └── health.py
│   │   ├── services/
│   │   │   ├── classifier.py
│   │   │   ├── gemini.py
│   │   │   ├── earth_engine.py
│   │   │   ├── soil_health.py
│   │   │   ├── weather.py
│   │   │   ├── rotation_engine.py
│   │   │   └── i18n.py
│   │   ├── models/            # pydantic schemas
│   │   └── data/
│   │       ├── lgd_districts.csv
│   │       ├── shc_sample.csv
│   │       └── crop_rotation_rules.yaml
├── ml/
│   ├── notebooks/
│   │   ├── 01_train_plantvillage.ipynb
│   │   ├── 02_benchmark_plantdoc.ipynb
│   │   └── 03_confidence_calibration.ipynb
│   ├── train.py
│   ├── evaluate.py            # produces the 3-column table
│   └── export_model.py
├── frontend/                  # React + Vite + Tailwind
│   ├── Dockerfile
│   └── src/
│       ├── pages/
│       │   ├── FarmerApp.jsx
│       │   ├── OfficerDashboard.jsx
│       │   └── AddDistrict.jsx
│       └── i18n/
└── .github/
    └── workflows/
        └── deploy.yml         # auto-deploy to Cloud Run on push to main
```

---

## PART 3.5 — MODEL STRATEGY (read before opening any issue)

> **Rule: match the model to the *kind of thinking* the issue needs, not to the issue's importance.** Scaffolding and boilerplate want a fast execution model. Ambiguous judgment calls — class mappings, agronomy rules, claim framing — want a heavy reasoning model. Using Opus-class reasoning on boilerplate burns your quota; using a fast model on the rules engine bakes in errors you won't catch until demo day.

### Your team's actual setup: 3 × Claude subscription + 1 × Antigravity

| Member | Tool | Notes |
|---|---|---|
| 3 members | **Claude Code** with `opusplan` | `/model opusplan` uses Opus for planning, Sonnet for execution — the right split automatically |
| 1 member | **Google Antigravity** | Free during public preview, includes **Gemini 3 Pro**. See `antigravity-guide.md`. |

**Who should be the Antigravity member?** Ranked by risk:

1. ✅ **Best: M4 (Product/Evaluation).** Docs, deck and adversarial review are heavy-reasoning but low-volume — a weekly quota comfortably covers them, and Antigravity's browser integration helps with research.
2. ✅ **Also good: M3 (Full-Stack/Deployment).** Mostly boilerplate, and Antigravity's built-in Chrome integration is genuinely useful for testing the deployed UI.
3. ⚠️ **Riskiest: M2 (Geospatial).** Gemini 3 Pro is the *better* model for Earth Engine — Google's own model knows its own platform — but issues #5 and #7 are your two heaviest, and Antigravity's free allowance is **weekly**, not daily. A quota wall mid-week stalls your differentiator.
   - **If M2 must be the Antigravity member:** front-load the reasoning. Spend Monday getting the GEE cloud-masking logic and the rules-engine structure settled while quota is fresh, then implement from those decisions manually for the rest of the week.

> **The bigger risk than quota:** cross-model review. If all four members build on Claude, nobody catches Claude's blind spots. Having one member on Gemini 3 Pro is an asset — use them for Issue #13 regardless of which role they hold.

### If a subscription holder doesn't want to use their subscription

Antigravity is free for everyone, so any member can fall back to it. `antigravity-guide.md` is written for a complete beginner and assumes no prior setup. Other free routes:

| Route | Cost | Catch |
|---|---|---|
| **Cursor Pro** — free for students via SheerID | Free | Verification can reject online-only programs |
| **GitHub Copilot Student** | Free | ⚠️ New student sign-ups paused from 20 April 2026 |

### Model class per issue

| Issue | Thinking required | Model class | Why |
|---|---|---|---|
| **#1** Cloud Run skeleton | Execution | **Fast** (Sonnet / Gemini Flash) | High-volume, fully-specified boilerplate. Reasoning models add nothing here. |
| **#2** Train classifier | Mixed | **Heavy for design, fast for code** | The specimen-level split strategy and augmentation design need judgment; the notebook code doesn't. |
| **#3** PlantDoc benchmark | **Heavy** | **Opus / Gemini 3 Pro** | Class mapping between two label spaces is genuinely ambiguous. A wrong mapping silently corrupts your headline differentiator. |
| **#4** Gemini fallback | Mixed | **Heavy for prompt + schema design, fast for wiring** | The JSON contract and the "unclear image" handling are where this breaks. |
| **#5** Earth Engine NDVI | **Heavy** | **Gemini 3 Pro preferred** | GEE's API is idiosyncratic and cloud-masking is easy to get subtly wrong. Google's own model tends to know its own platform best. |
| **#6** SHC ingestion | Mixed | **Fast, heavy for schema** | Scraping and normalization are mechanical; the LGD-keyed schema design is not. |
| **#7** Regenerative rules engine | **Heavy — highest stakes** | **Opus / Gemini 3 Pro** | This is your differentiator and it encodes agronomy domain logic. Errors here are invisible until a judge with agri knowledge asks a question. |
| **#8** District dashboard | Execution | **Fast** | Standard React + Leaflet work. |
| **#9** Multilingual + voice | Execution | **Fast**; use **Gemini** to generate the i18n JSON | Translation quality is the model's job, not the architecture's. |
| **#10** AI trace panel | Execution | **Fast / Haiku-class** | Logging and a collapsible panel. |
| **#11** README, SCALE, model card | **Heavy** | **Opus / Gemini 3 Pro** | This is where the language discipline lives. One inflated claim discounts the whole submission. |
| **#12** Deck + demo video | **Heavy** | **Opus / Gemini 3 Pro** | Balancing persuasion against honesty is exactly the judgment a fast model gets wrong. |
| **#13** Adversarial review | **Heavy** | **Opus / Gemini 3 Pro — and deliberately a *different* model family than the one that wrote the code** | A model reviewing its own output shares its own blind spots. Cross-family review catches what same-family review misses. |
| **#14** Submission | None | — | Humans only. Check the URL from a phone. |

### Three operating rules

1. **`opusplan` for the three Claude Code members.** It uses Opus during plan mode, then switches to Sonnet for execution. Set it with `/model opusplan` in-session or `claude --model opusplan` at startup. The Antigravity member gets Gemini 3 Pro by default — no configuration needed.
2. **Fresh session per phase.** Re-attach `prompt.md` each time. A session running since Phase 1 will have drifted on the ₹0 constraint and the language discipline by Phase 3 — the two rules where a lapse is silent and expensive.
3. **Cross-model review before submission.** Whatever built the code should not be the thing that reviews it. **This is exactly why having one member on Antigravity is an advantage** — have them run Issue #13 against the Claude-built code, and have a Claude member review whatever Gemini built.

---

## PART 4 — GITHUB ISSUES (create these, assign as marked)

Create labels first: `module-a`, `module-b`, `module-c`, `infra`, `docs`, `P0`, `P1`, `P2`, `blocker`.

Milestones: `M1: Skeleton Live (Day 2)`, `M2: Modules Working (Day 6)`, `M3: Integrated (Day 9)`, `M4: Submitted (Day 11)`.

---

### 🔴 #1 — [P0][blocker][infra] Deploy a live Cloud Run skeleton with stub data
**Assignee:** M3 (Full-Stack/Deployment) · **Milestone:** M1 · **Due: Day 2**
> 🤖 **Model: FAST** — Sonnet-class or Gemini Flash. Fully-specified boilerplate; reasoning models waste quota here.

A live deployed link is a hard submission requirement. If this isn't done on Day 2, the project is at risk regardless of everything else.

**Tasks**
- [ ] FastAPI backend with `/health`, `/api/diagnose` (returns stub), `/api/advisory` (returns stub), `/api/districts` (returns stub)
- [ ] React+Vite frontend, three routes: farmer, officer dashboard, add-district
- [ ] Dockerfile for both; deploy backend + frontend to Cloud Run in `us-central1`
- [ ] Deploy flags: `--min-instances=0 --max-instances=2 --memory=512Mi` (free-tier discipline)
- [ ] GitHub Actions workflow auto-deploying `main` to Cloud Run
- [ ] Post the live URL in this issue and pin it

**Acceptance:** a public URL loads the farmer page and the officer dashboard with placeholder data, and a push to `main` redeploys automatically.

**References**
- Cloud Run deploy: `https://cloud.google.com/run/docs/deploying`
- Cloud Run + GitHub Actions: `https://cloud.google.com/run/docs/continuous-deployment-with-cloud-build`

---

### 🔴 #2 — [P0][module-a] Train disease classifier on PlantVillage
**Assignee:** M1 (ML/Vision) · **Milestone:** M2 · **Due: Day 5**
> 🤖 **Model: HEAVY for design → FAST for code.** Use Opus / Gemini 3 Pro to settle the specimen-level split and augmentation strategy, then drop to a fast model for the notebook itself.

**Context:** PlantVillage contains 54,306 images across 14 crops and 38 disease classes, but is almost entirely lab-captured with uniform backgrounds. Benchmark literature shows DenseNet121 holds up better than lightweight models in field conditions, while MobileNetV2 performs well in controlled setups. Train both; pick on PlantDoc performance, not PlantVillage performance.

**Tasks**
- [ ] Download PlantVillage; **split at specimen/leaf level, not image level** (image-level splits leak near-duplicates and inflate accuracy)
- [ ] Fine-tune MobileNetV2 and DenseNet121 (ImageNet init)
- [ ] Heavy augmentation: random backgrounds, lighting jitter, blur, rotation, occlusion — this is domain-gap mitigation, not decoration
- [ ] Report **per-class precision/recall/F1**, not just accuracy (class imbalance is a known PlantVillage problem)
- [ ] **Train on Google Colab free tier (T4 GPU) or Kaggle (30 GPU-hrs/week) — NOT Vertex AI, which has no free tier**
- [ ] Export to **ONNX** (`torch.onnx.export` / `tf2onnx`) for in-container CPU serving
- [ ] Verify ONNX model is under ~50 MB and CPU inference is under 1s
- [ ] Push artifact to GCS (5 GB free) or commit via Git LFS

**Acceptance:** two trained models, per-class metrics committed to `ml/results/`.

**References**
- PlantVillage paper (the 99% → 31.4% finding): `https://arxiv.org/pdf/1604.03169`
- Architecture trade-offs survey: `https://arxiv.org/pdf/2009.04365`

---

### 🔴 #3 — [P0][module-a] Benchmark on PlantDoc and publish the honesty table
**Assignee:** M1 · **Milestone:** M2 · **Due: Day 6** · **Depends on #2**
> 🤖 **Model: HEAVY — Opus / Gemini 3 Pro.** Mapping PlantDoc classes onto the PlantVillage label space is a genuine judgment call. A wrong mapping silently corrupts your headline differentiator and you won't notice until a judge asks.

**This issue is the single biggest differentiator in the whole project.**

PlantDoc is real-field imagery created precisely because PlantVillage's controlled conditions don't transfer. Expect a large drop — that is the finding, not a failure.

**Tasks**
- [ ] Clone `https://github.com/pratikkayal/PlantDoc-Dataset` (Cropped-PlantDoc)
- [ ] Map PlantDoc classes onto your PlantVillage label space (document unmapped classes honestly)
- [ ] Run zero-shot evaluation of both models
- [ ] Produce the three-column table: PlantVillage acc / PlantDoc acc / PlantDoc+Gemini acc
- [ ] Write `docs/model-card.md` with intended use, limitations, and the domain-gap discussion
- [ ] Add a confusion matrix image to the README

**Acceptance:** `evaluate.py` regenerates the table from scratch; README shows it prominently.

**⚠️ Rule for the whole team: nobody quotes a single accuracy number anywhere — deck, video, README, or verbally — without both columns.**

---

### 🔴 #4 — [P0][module-a] Gemini multimodal fallback + confidence gate
**Assignee:** M1 · **Milestone:** M2 · **Due: Day 6**
> 🤖 **Model: HEAVY for the prompt + JSON schema → FAST for wiring.** The "unclear image" and "not a plant" handling is where this breaks in a live demo.

**Tasks**
- [ ] `services/gemini.py` — send image + top-3 CNN predictions + crop context to Gemini multimodal
- [ ] **Use a Flash-class model only. Pro models left the free tier in April 2026 and will charge you.**
- [ ] Implement `MOCK_GEMINI=true` env flag so teammates develop without burning the ~1000/day quota
- [ ] Hard daily call counter that fails closed at the configured limit
- [ ] Confidence gate: route to Gemini when max softmax < 0.70, or when an out-of-distribution check fires
- [ ] Prompt Gemini to return strict JSON: `{disease, confidence, reasoning, treatment_steps[], organic_alternatives[], severity}`
- [ ] Handle "not a plant" / "unclear image" gracefully — ask for a retake rather than guessing
- [ ] Cache responses in Firestore keyed by image hash (cost control)
- [ ] Log every call for the AI-trace panel

**Acceptance:** a deliberately blurry or non-leaf image produces a sensible Gemini-routed answer, visible in the trace panel.

**References**
- Gemini API image understanding: `https://ai.google.dev/gemini-api/docs/vision`

---

### 🟠 #5 — [P0][module-b] Earth Engine NDVI service
**Assignee:** M2 (Geospatial/Data) · **Milestone:** M2 · **Due: Day 6**
> 🤖 **Model: HEAVY — Gemini 3 Pro preferred.** The Earth Engine API is idiosyncratic and cloud-masking is easy to get subtly wrong. Google's own model tends to know its own platform best. Free via Antigravity.

**Blocked by GEE approval (Part 0.1). Build against mock data until approved — do not idle.**

**Tasks**
- [ ] Service-account auth for GEE in Cloud Run
- [ ] Use `COPERNICUS/S2_SR_HARMONIZED` (Google recommends the harmonized collections over `S2_SR` for consistent time series)
- [ ] Cloud/shadow masking before NDVI — unmasked NDVI is garbage and a judge may spot it
- [ ] NDVI = `normalizedDifference(['B8','B4'])`; return a 12-month time series per district/polygon
- [ ] Gap-fill cloud-occluded dates
- [ ] Cache per district per week in Firestore
- [ ] **Pre-compute and cache NDVI for the 3 demo districts. Never call GEE live during the demo** — Community Tier gives 150 EECU-hours/month and exceeding it triggers Restricted (slowed) mode
- [ ] Log EECU usage so you can see how close you are to the quota

**Acceptance:** `GET /api/ndvi?district=<lgd_code>` returns a 12-month series in under 3s (cached).

**References**
- Sentinel-2 catalog + harmonized guidance: `https://developers.google.com/earth-engine/datasets/catalog/sentinel-2`
- Cloud-masked NDVI time series example: `https://pypi.org/project/geeagri`

---

### 🟠 #6 — [P0][module-b] Soil Health Card ingestion
**Assignee:** M2 · **Milestone:** M2 · **Due: Day 6**
> 🤖 **Model: FAST for scraping/normalization → HEAVY for the LGD-keyed schema design.**

SHC records real parameters: pH, electrical conductivity, organic carbon, available N/P/K, sulphur, and micronutrients (Zn, Cu, Fe, Mn, B), with sampling points geo-coded via GPS and QR-coded. Cards are issued in 22 languages and 5 dialects — cite this in the deck as multilingual justification.

**Tasks**
- [ ] Evaluate Google's own scraper: `https://github.com/google-research-datasets/india-soil-health-card`
- [ ] Also pull district aggregates from `data.gov.in` (search "Soil Health Card")
- [ ] Normalize into a schema keyed by LGD district code
- [ ] Seed 3 districts with real data; document provenance in `docs/data-sources.md`
- [ ] Where real per-field data is unavailable, generate realistic samples **clearly labelled `synthetic: true`** in both the API response and the UI

**Acceptance:** three districts with real, cited SHC data; every synthetic record visibly flagged.

**⚠️ Never present synthetic data as real. A prior team on this exact hackathon circuit had to retroactively patch their repo to label simulated nodes. Label it from the start.**

---

### 🟠 #7 — [P1][module-b] Regenerative advisory engine
**Assignee:** M2 · **Milestone:** M3 · **Due: Day 8** · **Depends on #5, #6**
> 🤖 **Model: HEAVY — Opus / Gemini 3 Pro. Highest-stakes issue in the repo.** This encodes agronomy domain logic and it is your differentiator. Errors here are invisible until someone with agricultural knowledge questions them.

This is your differentiator. Most teams skip it despite the PS explicitly asking for regenerative crop recommendations.

**Tasks**
- [ ] `crop_rotation_rules.yaml` — legume/cereal rotation, green manure, cover crops, mapped to soil deficiency patterns
- [ ] Rules engine: low organic carbon → cover crop + FYM; low N + cereal history → legume rotation; high EC → salinity management
- [ ] Combine soil status + NDVI trend + upcoming weather into a seasonal plan
- [ ] Gemini generates the farmer-facing narrative from the structured rules output
- [ ] Surface *why*: "your organic carbon is 0.4% (low) and has declined over two seasons"

**Acceptance:** `POST /api/advisory` returns a structured plan plus natural-language text in the chosen language.

**⚠️ Language discipline: this is a rules engine with LLM narration. Say exactly that. Do not call it "an AI model that predicts soil regeneration" — you didn't train one.**

---

### 🟠 #8 — [P1][module-c] District officer dashboard
**Assignee:** M3 + M4 · **Milestone:** M3 · **Due: Day 8**
> 🤖 **Model: FAST.** Standard React + Leaflet work.

This is the artifact a ministry would pilot. It carries the Depth & Reach (20%) and Deployability (20%) scores.

**Tasks**
- [ ] Map view: disease reports clustered by block, colour-coded by crop
- [ ] Soil degradation hotspots (organic carbon below threshold)
- [ ] NDVI anomaly alerts (district trending below its own historical baseline)
- [ ] Summary stats: farmers served, advisories issued, top three diseases this month
- [ ] Export to CSV (officials live in spreadsheets — this small touch reads as real-world awareness)
- [ ] "Add a District" flow demonstrating onboarding in the live demo

**Acceptance:** a judge can watch a new district get added and populated during the demo.

---

### 🟡 #9 — [P1][infra] Multilingual + voice interface
**Assignee:** M3 · **Milestone:** M3 · **Due: Day 8**
> 🤖 **Model: FAST for the code; use Gemini to generate the i18n JSON files.** Translation quality is the model's job, not the architecture's.

**Tasks**
- [ ] **Pre-translated static JSON i18n files** (`en/hi/ta/mr.json`) — generate once with Gemini during development, commit them. Zero runtime cost, zero quota, no latency.
- [ ] Minimum: English, Hindi, Tamil, Marathi (justify choices by crop geography, don't pick randomly)
- [ ] **Browser Web Speech API** for voice input (`webkitSpeechRecognition`, locales `hi-IN`/`ta-IN`/`mr-IN`) and **browser SpeechSynthesis** for playback — both free, client-side, no backend quota
- [ ] Note the Chrome/Edge-only limitation in the README Limitations section
- [ ] Low-literacy affordances: icon-driven nav, large tap targets
- [ ] Graceful degradation when offline/slow

**Acceptance:** full farmer flow completable in Hindi by voice.

---

### 🟡 #10 — [P1][infra] AI pipeline trace panel
**Assignee:** M3 + M1 · **Milestone:** M3 · **Due: Day 9**
> 🤖 **Model: FAST / Haiku-class.** Logging plus a collapsible panel.

Makes the 25% Google AI weight *visible* instead of claimed.

**Tasks**
- [ ] Log each AI call: service, latency, tokens/cost estimate, outcome
- [ ] Collapsible "How this answer was produced" panel in the UI
- [ ] Show the routing decision: CNN confidence 0.42 → routed to Gemini → final answer

**Acceptance:** a judge can see which Google service handled each step.

---

### 🟡 #11 — [P1][docs] README, SCALE.md, model card, data provenance
**Assignee:** M4 (Product/Evaluation) · **Milestone:** M3 · **Due: Day 9**
> 🤖 **Model: HEAVY — Opus / Gemini 3 Pro.** This is where the language discipline lives. One inflated claim discounts everything else in the submission.

**Tasks**
- [ ] README: problem, architecture diagram, the honesty benchmark table, setup instructions, **Limitations section**
- [ ] `SCALE.md`: onboarding a new district/state, Cloud Run cost per 10k farmers, ministry integration path
- [ ] `docs/data-sources.md`: every dataset with URL, licence, and real-vs-synthetic status
- [ ] `docs/model-card.md`: intended use, out-of-scope use, measured limitations
- [ ] Cite every reused open-source component — submission rules require it

---

### 🟡 #12 — [P0][docs] Demo video + pitch deck
**Assignee:** M4 · **Milestone:** M4 · **Due: Day 10**
> 🤖 **Model: HEAVY — Opus / Gemini 3 Pro.** Balancing persuasion against honesty is exactly the judgment a fast model gets wrong.

**Record on Day 10, not Day 11. Systems break on the last day.**

**Deck structure (10–12 slides):**
1. Problem — Indian smallholder context, with a cited statistic
2. Why existing solutions fail — **lead with the PlantVillage domain gap; this is your hook**
3. Solution overview — three modules
4. Module B (regenerative advisory) — *your differentiator, give it the most space*
5. Module A (diagnostics) — with the honest benchmark table
6. Module C (district dashboard) — the ministry pilot artifact
7. Google AI architecture — the five load-bearing integrations
8. Scale across India — LGD model, onboarding cost, state rollout path
9. Impact — farmers reachable, districts, quantified where honest
10. Deployability — live URL, Cloud Run, pilot-in-weeks argument
11. Limitations & roadmap — *include this; it raises credibility, it doesn't lower it*
12. Team + ask

**Video (3–5 min):** 30s problem → 45s the domain-gap insight → 90s live end-to-end walkthrough (farmer photo → diagnosis → advisory → officer dashboard) → 45s scale → 30s close. Show the live URL on screen.

---

### 🟢 #13 — [P2] Adversarial review session
**Assignee:** M4 leads, whole team · **Milestone:** M4 · **Due: Day 10**
> 🤖 **Model: HEAVY — and deliberately a DIFFERENT model family than the one that wrote the code.** A model reviewing its own output shares its own blind spots. If Claude built it, have Gemini 3 Pro attack it, and vice versa.

M4 plays hostile judge for 60 minutes. Mandatory questions:
- "What's your accuracy?" (correct answer cites both columns unprompted)
- "How is this different from the other agri submissions?"
- "Which parts of your data are synthetic?"
- "What does Gemini actually do that a local model couldn't?"
- "How long to onboard Maharashtra?"
- "What happens when a farmer photographs a crop you never trained on?"
- "Is your NDVI cloud-masked?"

Any question that produces hesitation becomes a same-day fix.

---

### 🟢 #14 — [P0] Final submission
**Assignee:** You · **Milestone:** M4 · **Due: Day 11 (submit early)**
> 🤖 **Model: none.** Humans only. Check the live URL from a phone on mobile data.

- [ ] Repo public, README complete, all components cited
- [ ] Live URL verified from a phone on mobile data, not just your laptop
- [ ] Demo video uploaded and link tested in incognito
- [ ] Deck exported to PDF
- [ ] 2–3 line description written
- [ ] Submit on Hack2Skill **a full day early** — portals fail at deadline

---

## PART 5 — THE CLAUDE CODE PROMPT

**Moved to a separate file: `prompt.md`.**

Give Claude Code **both files together**:
1. `prompt.md` — the full step-by-step build instructions
2. `track4-execution-package.md` — this file, as background context

Tell it: *"Read track4-execution-package.md for context, then follow prompt.md."*

---

## PART 6 — DAILY CADENCE

15-minute standup, same time daily. Three questions only:
1. Is the live URL still up? *(if no, that's the day's only priority)*
2. What did you finish yesterday?
3. What's blocking you?

Post the live URL in your group chat every single day. The day it's missing is the day the project is in trouble.

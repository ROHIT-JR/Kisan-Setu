# AGENTS.md — read this before touching this repo

This file is standing instructions for **any AI agent** working in this repository —
Claude Code, Google Antigravity (Gemini 3 Pro), Cursor, Copilot, or anything else.
It is read automatically by Antigravity on every task and should be pasted into the
system/context of any other tool that doesn't auto-load it.

Full background lives in `docs/track4-execution-package.md` and `docs/prompt.md`
(the original planning docs — read them for the "why" behind every rule below).

---

## 0. What this project is

**Kisan Setu** — a regenerative agriculture advisory platform for Indian smallholder
farmers. Submission for Google Cloud "Build with AI: Code for Communities — Second
Edition", Track 4 (AgriN & Regenerative Agricultural Intelligence), Hack2Skill.

- Repo: `https://github.com/ROHIT-JR/Kisan-Setu`
- Deadline: **30 Sept 2026**. Team: 4 people, all using AI coding agents.
- **Budget: ₹0.** This is a hard constraint, checked in every review pass.

---

## 1. Hard constraints — never violate these

1. **Never use Vertex AI.** No ongoing free tier; endpoints bill per node-hour even idle.
2. **Never call a Gemini Pro model.** Pro left the free tier in April 2026. Hardcode a
   **Flash** or **Flash-Lite** model only, everywhere `GEMINI_MODEL` is used.
3. **Never use Cloud SQL** (bills from instance creation) or **Cloud Load Balancer**
   (never free). Firestore only for data + cache.
4. **Never call Cloud Translation or Cloud Speech/TTS APIs at runtime.** Use
   pre-translated static JSON (`frontend/src/i18n/*.json`) and the browser's
   Web Speech API / SpeechSynthesis instead.
5. **Never quote a single accuracy number** in code, docs, UI copy, commit messages,
   or logs. Always pair the lab number (PlantVillage) with the field number
   (PlantDoc): e.g. `"96% lab (PlantVillage) / 61% field (PlantDoc)"`.
6. **Never present synthetic data as real.** Any generated/mock record must carry
   `"synthetic": true` in the API response AND render a visible badge in the UI
   (`frontend/src/components/SyntheticBadge.jsx`).
7. **Never describe Module B (the advisory engine) as a trained predictive model.**
   It is a **deterministic rules engine with LLM narration**. Say exactly that in
   code comments, docstrings, README, and UI copy.
8. **Never commit secrets.** This repo is public. Only `.env.example` is committed;
   real values live in `.env` (gitignored) or Cloud Run env vars / Secret Manager.
9. **Every record is multi-tenant from day 1** — carries `state_code`,
   `district_code`, `block_code` using **LGD (Local Government Directory)** codes.
   Onboarding a new district must be a data/config change, never a code change.
10. **Cache-first on every external call** (Gemini, Earth Engine, weather). No
    exceptions. Gemini cache key: `sha256(image_bytes + prompt_version)`. Earth
    Engine cache: per district, per week.

Cloud Run deploy flags (never deviate without asking):
```
--min-instances=0 --max-instances=2 --memory=512Mi --region=us-central1
```

---

## 2. Model selection — match the model to the kind of thinking, not the issue's importance

| Kind of work | Model class | Examples |
|---|---|---|
| Fully-specified boilerplate, wiring, React/Leaflet UI, logging | **Fast** (Sonnet / Gemini Flash) | Issues #1, #8, #9, #10 |
| Judgment calls, class mappings, schema/prompt design, agronomy rules | **Heavy** (Opus via `opusplan` / Gemini 3 Pro) | Issues #3, #5, #7, #11, #12, #13 |
| Mixed: design needs judgment, implementation doesn't | **Heavy for the decision, fast for the code** | Issues #2, #4, #6 |

- Claude Code members: run `/model opusplan` (Opus plans, Sonnet executes).
- The Antigravity member gets Gemini 3 Pro by default. Antigravity's agent quota is
  **weekly, not daily** — front-load heavy-reasoning issues early in the week.
- **Cross-model review before submission is mandatory.** Whatever model wrote a
  piece of code must not be the one that reviews it (see Issue #13). If Claude built
  it, have Gemini attack it, and vice versa — same-family review shares blind spots.
- Start a **fresh session per phase**. A session running since Phase 1 drifts on the
  ₹0 constraint and the language discipline by Phase 3 — check this file again at
  the start of every new phase/session.

---

## 3. The three modules (see `docs/prompt.md` §5 for full detail)

- **Module A — Field Diagnostic**: CNN (ONNX, in-container) with a confidence gate
  at 0.70; below that, or on an out-of-distribution image, route to Gemini Flash
  multimodal. `backend/app/services/classifier.py`, `gemini.py`.
- **Module B — Regenerative Soil Advisory (the differentiator)**: Soil Health Card
  data + Earth Engine NDVI + Open-Meteo → **deterministic rules engine**
  (`crop_rotation_rules.yaml` + `rotation_engine.py`) → Gemini narrates the output
  in the farmer's language. Never call this "AI-predicted."
- **Module C — District Officer Dashboard**: the ministry-pilot artifact. Carries
  40% of the scoring rubric (Depth & Reach + Deployability). Map, hotspots, stats,
  CSV export, live "Add a District" flow.

---

## 4. Engineering rules

1. Deploy first — a live Cloud Run URL with stub endpoints beats any amount of
   offline model work. Nothing else matters until it's live.
2. Specimen-level train/test splits for PlantVillage — image-level splits leak
   near-duplicates and inflate accuracy.
3. Report per-class precision/recall/F1, not just accuracy.
4. Cloud-mask Sentinel-2 NDVI before computing it (`COPERNICUS/S2_SR_HARMONIZED`,
   not `S2_SR`); gap-fill occluded dates. Unmasked NDVI is invalid and a judge may
   notice.
5. Every external call needs a timeout and a fallback. The live demo must never
   hard-fail.
6. Cite every reused open-source component (submission rules require it).

---

## 5. Language discipline (applies to code, docs, UI copy, commit messages)

| Never write | Write instead |
|---|---|
| "AI predicts soil health" | "rules engine with LLM narration" |
| "integrated with government systems" | "integration-ready via published SHC data formats" |
| "99% accuracy" | "96% lab (PlantVillage) / 61% field (PlantDoc)" |
| "real-time national coverage" | "3 pilot districts, architecture supports N districts" |

Prefer underclaiming. One inflated claim a judge catches discounts the whole
submission.

---

## 6. Working conventions for every agent/member

- **Pull before you start, push when you finish.** Four people, one repo:
  `git pull origin main` → one task → review the diff → commit → `git push`.
- **Commit after every working task**, with a message referencing the issue
  (`feat: advisory rules engine (#7)`). Never use `--no-verify`.
- **One task/agent at a time per person.** Don't run parallel agents against the
  same shared repo — merge conflicts near the deadline are how teams miss it.
- **Review every diff an agent produces before accepting it.** Agents write
  plausible-looking code that is subtly wrong, especially in Earth Engine masking
  logic and the rules-engine thresholds.
- **State assumptions explicitly, ask rather than guess** on agronomy thresholds,
  GCP project IDs, or anything else not pinned down in this file or the linked docs.
- Run the **adversarial self-check** (`docs/prompt.md` §13) before every phase
  handoff — ten questions, any hesitation is a same-day bug.

---

## 7. Reference docs in this repo

- `docs/track4-execution-package.md` — full competition context, rubric, issue list, model routing per issue.
- `docs/prompt.md` — the phase-by-phase build spec, API contracts, architecture.
- `docs/antigravity-guide.md` — setup + usage guide for the Antigravity team member.
- `SCALE.md` — the ministry/state onboarding argument (Phase 4).
- `docs/data-sources.md`, `docs/model-card.md`, `docs/cost-analysis.md` — provenance,
  benchmarks, and the ₹0 cost breakdown.

If anything in a task conflicts with a rule in this file, **stop and ask** rather
than silently choosing one over the other.

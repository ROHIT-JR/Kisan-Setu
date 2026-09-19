# Model card — crop disease classifier

To be filled in by Issue #2 (training) and Issue #3 (PlantDoc benchmark).
Placeholder structure only — do not fill in numbers until they are measured.

## Intended use
Assistive crop disease triage for Indian smallholder farmers, routed through a
confidence gate to Gemini multimodal fallback for low-confidence or
out-of-distribution images. Not a substitute for local agricultural extension
advice — every response should carry that caveat.

## Training data
PlantVillage (lab-captured, 14 crops, 38 classes). Specimen-level train/test
split (never image-level — see `AGENTS.md` rule 2).

## Evaluation

| Metric | PlantVillage (lab) | Cropped-PlantDoc (field) | PlantDoc + Gemini fallback |
|---|---|---|---|
| Accuracy | TBD (Issue #2) | TBD (Issue #3) | TBD (Issue #3/#4) |
| Per-class F1 | see `ml/results/` | see `ml/results/` | see `ml/results/` |

**Never quote one column without the others — see `AGENTS.md` rule 5.**

## Known limitations
- PlantVillage is lab-captured; field accuracy is expected to be substantially
  lower. This gap is the reason the confidence gate + Gemini fallback exist.
- Coverage is limited to the crops/diseases present in PlantVillage's 38 classes.
- Confidence gate threshold (0.70) and out-of-distribution check are heuristics,
  not calibrated against a held-out field-conditions dataset larger than PlantDoc.

## Out-of-scope use
Not validated for crops outside the training label space; not a diagnostic tool
for human/animal health; not validated against Indian-specific PlantDoc-style
field imagery beyond the benchmark set.

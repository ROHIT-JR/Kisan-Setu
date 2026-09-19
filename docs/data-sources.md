# Data sources

Every dataset used in this project, with provenance and licence. Updated as each
module lands (Issues #2, #3, #6).

| Dataset | Source | Licence | Real / Synthetic |
|---|---|---|---|
| PlantVillage | `https://github.com/spMohanty/PlantVillage-Dataset` | CC0 / research use | Real (lab-captured) |
| Cropped-PlantDoc | `https://github.com/pratikkayal/PlantDoc-Dataset` | CC BY 4.0 | Real (field-captured) |
| Soil Health Card | `https://github.com/google-research-datasets/india-soil-health-card`, `data.gov.in` | Open Government Data (India) | Real where available; synthetic samples explicitly flagged `synthetic: true` |
| LGD district codes | Local Government Directory, Government of India | Public | Real |
| Sentinel-2 NDVI | `COPERNICUS/S2_SR_HARMONIZED` via Google Earth Engine | Open (Copernicus) | Real |
| Weather forecast | Open-Meteo | Open, no key required | Real |
| Map tiles | OpenStreetMap | ODbL | Real |

**Rule (see `AGENTS.md`): any record without a verified real source must carry
`"synthetic": true"` in both the API response and the UI. Never present synthetic
data as real.**

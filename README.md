# Sharpz Analytics

Monorepo del producto Sharpz — synthetic buyer panels for pre-launch decision testing.

## Qué contiene este repo

```
sharpzanalytics/
├── backend/          # FastAPI + pipeline V2 (in progress)
├── dna/              # YAMLs de test_types (15 test_types, en progreso)
├── venues/           # YAMLs de interaction surfaces (13 venues, en progreso)
├── prompts/          # Prompts YAML por test_type + shared (port de MiroFish)
├── docs/             # Documentación arquitectónica
│   └── dna-spec.md   # ← contrato declarativo central, leer primero
└── scripts/          # Scripts de dev / deploy / maintenance
```

## Qué NO contiene

Las webs del producto (landing, intake, admin) viven en sus deploys propios:

- **Landing** — `sharpzanalytics.com` (Netlify, HTML estático)
- **Intake form** — `intake.sharpzanalytics.com` (Vercel, Vue + Python serverless)
- **Admin panel** — (offline, Vue — pendiente de re-deploy)

El backend V2 de este repo es **API-compatible** con el intake form existente.

## Status

- Doc arquitectónico: `docs/dna-spec.md` v0.2 — open questions resueltas
- Backend engine: **no iniciado**
- Next: venues catalog + skeleton FastAPI + Stage 1

## Estado de milestones

| Milestone | Target | Status |
|---|---|---|
| m0: DNA spec + venues catalog + repo structure | semana 1 | 🟡 in progress |
| m1: investor_pitch end-to-end vs MiroFish (caso Invernea) | semana 3 | pending |
| m2: los 15 test_types + 4 tiers + cross-test learning básico | mes 2-3 | pending |
| m3: multi-tenant + self-serve + billing | mes 4-6 | pending |

Ver `docs/dna-spec.md` para el contrato declarativo y cómo se define un test_type.

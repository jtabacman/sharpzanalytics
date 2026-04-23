# Sharpz Analytics

Monorepo del producto Sharpz — synthetic buyer panels for pre-launch decision testing.

## Qué contiene este repo

```
sharpzanalytics/
├── backend/              # FastAPI + pipeline V2 (in progress)
├── frontends/            # 4 superficies del producto
│   ├── landing/          # sharpzanalytics.com
│   ├── intake/           # sharpzanalytics.com/intake/{id}
│   ├── control/          # control.sharpzanalytics.com
│   └── deliverable-template/  # sharpzanalytics.com/report/{project_id}
├── dna/                  # YAMLs de los 15 test_types
├── venues/               # YAMLs de los 13 interaction surfaces
├── prompts/              # Prompts YAML por test_type + shared (port de MiroFish)
├── docs/                 # Documentación arquitectónica (leer `dna-spec.md` primero)
└── scripts/              # Dev tooling, data migrations, ops helpers
```

## Los 4 frontends

| URL | Propósito | Stack |
|---|---|---|
| `sharpzanalytics.com` | Landing marketing + operator login | HTML + Three.js (Netlify) |
| `sharpzanalytics.com/intake/{intake_id}` | Cliente completa brief + estímulo + paga | Vue 3 SPA (servida por backend) |
| `control.sharpzanalytics.com` | Operador: queue, approvals, monitoring | Vue SPA (Vercel) |
| `sharpzanalytics.com/report/{project_id}` | Cliente ve deliverable interactivo | Jinja2 serif (backend render) |

Ver `docs/frontend-architecture.md` para DNS + routing.

## Docs clave

| Doc | Qué es |
|---|---|
| `docs/dna-spec.md` | Contrato declarativo central — cada test_type es un YAML structured |
| `docs/frontend-architecture.md` | URLs unificadas + DNS Hostinger + deploy strategy |
| `docs/intake-api-contract.md` | Shape del payload intake ↔ backend (fuente de verdad) |
| `docs/landing-design.md` | Referencia del landing actual (HTML + CSS + Three.js) |
| `docs/intake-design.md` | Referencia del intake actual (tokens + Vue + componentes) |
| `docs/repo-structure.md` | Convenciones de repo, commits, naming |

## Status

- `docs/dna-spec.md` v0.2 — decisiones resueltas
- `docs/frontend-architecture.md` v0.1 — pendiente confirmar prefijo `/report/`
- `docs/intake-api-contract.md` v0.1 — listo para implementar
- Backend engine: **no iniciado**
- Frontends: **pendientes de port** desde Mac (landing Netlify + intake Vercel + admin Vue offline)
- Next: venues catalog + 3 DNA YAMLs concretos + skeleton FastAPI + Stage 1

## Estado de milestones

| Milestone | Target | Status |
|---|---|---|
| m0: DNA spec + venues + frontends arch + repo structure | semana 1 | 🟡 in progress |
| m1: investor_pitch end-to-end vs MiroFish (caso Invernea) | semana 3 | pending |
| m2: los 15 test_types + 4 tiers + cross-test learning básico | mes 2-3 | pending |
| m3: multi-tenant + self-serve + billing | mes 4-6 | pending |

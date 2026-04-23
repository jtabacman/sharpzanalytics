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
| `docs/deliverable-design.md` | Referencia del deliverable (8 Jinja2 templates + sharpz.css + manifest schema) |
| `docs/roadmap.md` | Milestones m0-m5+ con deliverables y criterios de done |
| `docs/repo-structure.md` | Convenciones de repo, commits, naming |

## Status

- **m0 docs arquitectónicos:** ✓ completos (7 docs)
- **venues/:** ✓ 13/13 YAMLs
- **dna/:** ✓ 3/15 activos (investor_pitch, pricing_test, crisis_response). 12 pending m2.
- **backend/:** skeleton runnable — `/health` endpoint OK. Stage 1 en curso.
- **frontends/:** READMEs + import plans. Código pendiente port desde Mac.
- **Next:** Alembic init + shared prompts placeholders + Stage 1 (Intake API)

## Estado de milestones

| Milestone | Target | Status |
|---|---|---|
| m0: docs arquitectónicos + venues + 3 DNAs activos + backend skeleton | semana 1 | ✓ **done** |
| m1: investor_pitch end-to-end vs MiroFish (caso Invernea) | semana 3 | 🟡 in progress |
| m2: los 15 test_types + 4 tiers + cross-test learning básico | mes 2-3 | pending |
| m3: multi-tenant + self-serve + billing | mes 4-6 | pending |

# Frontends — Sharpz V2

Los 4 superficies del producto, unificadas bajo `sharpzanalytics.com`.

| Dir | URL | Stack |
|---|---|---|
| `landing/` | `sharpzanalytics.com` | HTML static + Three.js hero |
| `intake/` | `sharpzanalytics.com/intake/{id}` | Vue 3 SPA (port del existente) |
| `control/` | `control.sharpzanalytics.com` | Vue SPA operator (port del admin Vue) |
| `deliverable-template/` | `sharpzanalytics.com/report/{project_id}` | Jinja2 template serif + interactive JS |

Ver `docs/frontend-architecture.md` para DNS routing + deploy strategy.

## Estado actual

- Landing → existente en Netlify, **pendiente import a este repo**
- Intake → existente en Vercel (`intake.sharpzanalytics.com`), **pendiente port desde Mac + migración a `/intake/{id}`**
- Control → código Vue existe en Mac (`/MiroFish/frontend/`), **pendiente port + re-deploy**
- Deliverable → **pendiente build** (nuevo en V2)

## Design system

Ver `docs/landing-design.md` (theme A: operator-tech dark) y `docs/intake-design.md` (tokens duales).

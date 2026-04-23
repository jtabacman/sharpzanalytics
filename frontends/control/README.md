# Control panel — `control.sharpzanalytics.com`

Operator admin. Queue de intakes, approvals, pipeline monitoring, cost tracking, alerts.

- Stack: Vue SPA (del admin Vue existente en Mac) o rebuild en algo más moderno si ameritara
- Deploy: **Vercel** (recomendado) o backend como sub-SPA
- Status: **offline** — el droplet anterior se decomisionó. Código existe en `/Users/juliantabacman/MiroFish/frontend/` en la Mac.

## Funcionalidades core (v0)

- **Queue de intakes** con filtros por status + test_type
- **Detail view** de cada intake: ver lo que llenó el cliente, editar archetypes, ajustar tier
- **Approve / Reject** con reason message al cliente
- **Pipeline monitoring**: ver tests en ejecución con progress bar + cost + warnings
- **Alert feed**: HALT_ALERT requieren override con justificación del operador
- **Cost dashboard**: gasto vs budget del mes + por cliente
- **Test history**: completed tests con link al deliverable

## Import plan

1. Copiar `/Users/juliantabacman/MiroFish/frontend/src/` a `frontends/control/src/`
2. Update API endpoints para apuntar al backend V2 (operator endpoints)
3. Agregar auth flow con `OPERATOR_API_KEY` + session cookie
4. Build + deploy a Vercel apuntando CNAME `control.sharpzanalytics.com`

## Funcionalidades que NO tenía el admin anterior (agregar en v0 o v1)

- QA review interventions (ver issues flagged + approve/override auto-fixes)
- Real-time streaming de sim en progreso (v1+ feature — stage 14 del brief)
- Inject mid-sim (v1+)

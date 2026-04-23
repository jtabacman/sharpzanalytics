# Intake form — `sharpzanalytics.com/intake/{intake_id}`

Vue 3 SPA. 9 secciones numeradas con auto-save. Polimórfico según DNA del test_type seleccionado.

- Stack: Vue 3 + Vite (build static output)
- Deploy: **backend sirve el HTML base + monta SPA con intake_id en URL**, SPA llama al backend via `/api/intakes/:id`
- Status: **pendiente port** desde `/Users/juliantabacman/MiroFish/intake-public/` en la Mac

## Componentes (del design existente)

- `views/ClientIntake.vue` — vista principal con 9 secciones
- `components/ArchetypeCard.vue` — editor collapsable per archetype
- `components/ListBuilder.vue` — editor row-by-row de `string[]`
- `components/KeyValueBuilder.vue` — editor de `Record<string, string>`
- `components/SchemaField.vue` — router de tipos dinámicos (string/text/select/number/list/kv)

Design reference: `docs/intake-design.md`.
API contract: `docs/intake-api-contract.md` (fuente de verdad).

## Import plan

1. Copiar `/Users/juliantabacman/MiroFish/intake-public/src/` a `frontends/intake/src/`
2. Copiar `public/tokens.css` (design tokens globales)
3. Reemplazar `VITE_API_URL` en `.env` del build:
   - Old: `https://intake.sharpzanalytics.com/api/sharpz` (Vercel serverless)
   - New: `/api` (mismo dominio, backend sirve todo)
4. Update routing: la SPA lee `intake_id` de URL (`/intake/:id`) en lugar de query string
5. Build: `vite build` → `dist/` es lo que sirve el backend
6. Backend tiene un route `/intake/:id` que hace render del HTML base con intake_id injected

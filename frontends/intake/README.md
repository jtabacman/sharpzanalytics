# Intake Vue SPA — `sharpzanalytics.com/intake/{intake_id}`

Vue 3 + Vite single-page app. 9 secciones con auto-save. Consume el Intake API del backend (`docs/intake-api-contract.md`).

## Quick start

```bash
cd frontends/intake
npm install
npm run dev
# → http://localhost:5173/intake/new
```

Asume backend corriendo en `http://localhost:8000`. Vite proxy del dev server ruteará `/api/*` al backend. En prod el mismo dominio sirve todo.

## Build

```bash
npm run build
# → dist/ listo para servir desde el backend bajo la ruta /intake/
```

## Structure

```
frontends/intake/
├── package.json
├── vite.config.js
├── index.html                   # Vite entry HTML
└── src/
    ├── main.js                  # Vue app bootstrap
    ├── App.vue                  # Shell (solo router-view)
    ├── router.js                # Rutas: /new, /:intakeId
    ├── styles/global.css        # Base reset + body bg
    ├── api/intake.js            # Axios wrapper del Intake API
    ├── data/test_types.js       # Catálogo de los 15 test_types (UI)
    ├── views/
    │   ├── IntakeNew.vue        # POST /api/intakes → redirect
    │   ├── ClientIntake.vue     # La vista principal (9 secciones)
    │   └── IntakeSubmitted.vue  # Confirmación post-submit
    └── components/
        ├── ArchetypeCard.vue    # Editor collapsable de 1 archetype
        ├── ListBuilder.vue      # list<string> con phantom row
        ├── KeyValueBuilder.vue  # dict<string,string>
        └── SchemaField.vue      # Router de tipos dinámicos por schema
```

## Flujo

1. Cliente entra a `/intake/new` (del CTA del landing)
2. `IntakeNew.vue` POSTea a `/api/intakes`, recibe `{id}`, redirige a `/intake/{id}`
3. `ClientIntake.vue`:
   - GETs el intake por id
   - Completa las 9 secciones con auto-save (debounce 1.5s, watch deep)
   - "Enviar intake" → POST `/api/intakes/{id}/submit`
   - Si 400 con errores: los muestra en la caja roja
   - Si OK: re-fetch + muestra `IntakeSubmitted.vue`

## Design language

Dark theme heredado del landing (`#0a0a0a` + Space Grotesk + JetBrains Mono + acentos `#e0e0e0`). Ver `docs/intake-design.md` para tokens completos.

## Deploy

En producción el backend sirve `dist/index.html` con Vite base `/intake/` y las rutas dinámicas pasan por el backend (que provee la info del intake). Los assets (`/intake/assets/...`) salen de `dist/assets/`.

Alternativa temprana: Netlify con `_redirects` que proxyea `/intake/*` al backend tunnel.

## Status

- ✓ UI funcional con las 9 secciones
- ✓ Auto-save + submit + validation errors
- ✓ ArchetypeCard collapsable con 5 sub-secciones
- ✓ ListBuilder + KeyValueBuilder + SchemaField reusables
- ⏳ `test_type_specific` fields dinámicos: pendiente que el backend emita el schema por test_type (en m2). Por ahora la sección 03 usa solo `test_objective` + `decision_context` genéricos.
- ⏳ File upload del stimulus (PDF/imagen/video): pendiente endpoint de upload a R2 en backend (m1c).

# Deliverable template — `sharpzanalytics.com/report/{project_id}`

HTML render del reporte final + one-pager interactivo. Servido por el backend con data del test completado.

- Stack: Jinja2 (backend rendering) + CSS tokens light/serif + vanilla JS para interacciones
- Deploy: **backend sirve directo** (dynamic rendering por `project_id`)
- Design: theme B — "Report serif authority" (FT × McKinsey × Stratechery)
- Status: **pendiente build** (nuevo en V2)

## Design reference

Tokens completos en `docs/intake-design.md` sección 1 (`tokens.css`). Resumen:

- Paleta: `#FAF9F6` canvas, `#0A0E27` ink, `#B85C38` terracotta accent
- Fonts: `Inter` UI + `GT Sectra`/Georgia serif body + `JetBrains Mono` meta
- Signature: section headers tipo "01 / Executive Summary" + gradient title + terracotta blockquote borders
- Width: `720px` reading width para body

## Secciones del template

1. **Hero** — título del test + client branding (logo + primary_color) + metadata (tier, date, agents count)
2. **One-pager** (arriba, destacado) — 5 secciones fijas del brief (Decisión / Top 3 insights / 3 acciones / Qué mirar / Caveats)
3. **Reporte completo** (scroll down) — 10 secciones estándar + unique_sections del test_type
4. **Appendices interactivos:**
   - Personas del panel (grid clickable → modal con bio full + actions timeline)
   - Quotes extendidas (filtradas por archetype)
   - Métricas raw por variante
   - Methodology

## Interactividad

- Click en agent name en el reporte → modal con persona full + todas sus sim actions
- Click en quote → highlight del momento en el sim timeline
- Click en métrica → breakdown detallado + chart
- Export: PDF button (print-friendly CSS) + Notion/GDocs button (markdown copy)

## Security

- URL `/report/{project_id}` requiere signed token (JWT embebido en URL o cookie)
- Signed URL expira en 90 días
- Cliente puede generar links adicionales para su equipo con scope limitado
- NUNCA public

## Build plan

1. Definir template base `base.html.j2` con slots (one_pager, report_sections, appendices)
2. Import tokens.css desde `docs/intake-design.md` sección 1
3. Escribir `interactive.js` vanilla para modales + highlights
4. Backend Stage 8 hace render con data del test + uploads a blob storage O sirve on-demand

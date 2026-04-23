# Deliverable template — `sharpzanalytics.com/report/{project_id}`

Paquete multi-página HTML (+ PDF) que el cliente recibe. Jinja2 server-side rendering.

- Stack: Jinja2 + sharpz.css único + Cytoscape.js 3.26.0 (CDN, único JS externo) + WeasyPrint para PDF export
- Deploy: **backend sirve directo** (dynamic rendering por `project_id`, con cache)
- Design: theme B — "Quiet authority" (FT × McKinsey × Stratechery)
- Status: **spec completa en `docs/deliverable-design.md`**, pendiente implementación

## Spec completa

Ver `docs/deliverable-design.md` — tiene el código Jinja2 completo de los 8 templates + sharpz.css (~620 líneas) + manifest.json schema + QA checklist + anti-patterns explícitos.

## Design tokens resumidos

- Canvas: `#FAF9F6` (warm paper, no pure white)
- Ink: `#0A0E27` / ink-soft: `#1F2441`
- Accent warm (terracotta): `#B85C38` — brand tag, blockquote rule
- Accent cool (deep blue): `#1E40AF` — links
- Fonts: Inter (UI) + **Source Serif 4** (body) + JetBrains Mono (meta)
- Layout: sidebar 280px fixed + main con reading width 720px

## Los 8 templates

```
base.html                    # Shell: sidebar + main + branding injection
├── executive.html           # Landing page del deliverable (cover + one-pager + report)
├── variant.html             # Una por variante (key facts + SVG timeline + narrative)
├── interviews.html          # Apéndice B · Q&A por variante × archetype
├── audience.html            # Grafo Cytoscape + agent cards + composition table
├── forecast.html            # Opcional — pricing/campaign tests con proyección cuantitativa
├── appendix_metrics.html    # Apéndice A · raw data + CSV download + JSON colapsable
└── appendix_methodology.html # Apéndice D · 5 limitaciones conocidas explícitas
```

## Manifest.json structure

Cada deliverable publicado genera un `manifest.json` con:
- `deliverable_id`, `test_id`, `client_display_name`, `test_display_title`
- `assets[]` con `asset_id`, `kind`, `title`, `html_path`, `pdf_path`, `order`
- `base_path`, `access_token`, `expires_at` (null = sin expiración)
- `views`, `view_log[]` (audit trail)
- Timestamps: `created_at`, `published_at`, `updated_at`

Convención de `order`:
- 1-9: páginas obligatorias (executive, audience)
- 10-19: variantes individuales
- 20-29: secciones opcionales (forecast)
- 30-39: apéndices "voces" (interviews)
- 40-49: apéndices "data cruda" (metrics, CSV)
- 50-59: apéndices metodología

## Branding hooks por cliente

2 variables inyectables via Jinja context:

| Hook | Efecto |
|---|---|
| `branding.primary_color` (hex) | Brand tag + border-left del nav activo + chip "winner" + color de links |
| `branding.logo_url` | Logo del cliente arriba de todo en sidebar (max 140px × 48px, object-fit: contain) |

El body del reporte preserva su identidad Sharpz (terracotta blockquote, serif body). El branding vive solo en zonas periféricas.

## Print / PDF

- `@media print` crítico en sharpz.css
- WeasyPrint server-side on first request, cached after
- Sidebar desaparece, page-break entre variantes, URL annotations en links externos
- Font-size baja a 11pt, reading width ocupa toda la página
- Botón "Descargar deliverable completo (PDF)" arriba-derecha del executive

## Security

- URL: `sharpzanalytics.com/report/{project_id}?token={jwt}` (JWT embedded)
- Signed URL expira en 90 días (configurable per tier)
- Cliente puede generar links adicionales con scope limitado
- NUNCA public — `noindex,nofollow` en meta tags

## Build plan

1. Copiar los 8 templates + sharpz.css literal desde `docs/deliverable-design.md` a `frontends/deliverable-template/`
2. Backend Stage 8 renderiza con data del test (variants, metrics, interviews, narrative, forecast opcional, graph data)
3. Publish: upload a R2 bucket + generate signed URL + email al cliente
4. WeasyPrint PDF: trigger on-demand, cache por project_id
5. CSV download: endpoint `/api/tests/{test_id}/metrics.csv` protegido por mismo JWT

## Anti-patterns explícitos (ver `docs/deliverable-design.md` sección 11)

- No emojis en títulos
- No gradients / glass morphism
- No dark mode (serif sobre negro = feo)
- No "Powered by Sharpz" en footer
- No botones share social (confidencial)
- No popups / autoplay / chat bubbles
- No esconder limitaciones — el Apéndice D es feature, no bug
